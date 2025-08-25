"""
Optimierter Datenlade-Modul für MokiG Dashboard
===============================================
Verwendet Parquet-Format, Caching und Lazy Loading für maximale Performance.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from functools import lru_cache
import pyarrow.parquet as pq
import pickle
import hashlib
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class OptimizedDataLoader:
    """Hochperformanter Datenloader mit Caching und Lazy Loading"""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.parquet_dir = self.base_path / "data_optimized"
        self.cache_dir = self.base_path / "cache"
        
        # Legacy Pfade für Fallback
        self.twin2sim_path = self.base_path / "Daten" / "Beispieldaten"
        self.erentrudis_path = self.base_path / "Daten" / "Monitoringdaten" / "Erentrudisstr"
        self.fis_path = self.base_path / "Daten" / "Monitoringdaten" / "FIS_Inhauser"
        self.kw_path = self.base_path / "Daten" / "vertraulich_erzeugungsdaten-kw-neukirchen_2025-07-21_0937"
        
        # In-Memory Cache mit LRU (Least Recently Used)
        self.memory_cache = {}
        self.cache_timestamps = {}
        self.cache_ttl = 300  # 5 Minuten TTL
        
        # Performance Monitoring
        self.load_times = []
    
    def _get_cache_key(self, source, dataset, columns=None, filters=None):
        """Generiert eindeutigen Cache-Key"""
        key_parts = [source, dataset]
        if columns:
            key_parts.append('_'.join(sorted(columns)))
        if filters:
            key_parts.append(str(filters))
        return hashlib.md5('_'.join(key_parts).encode()).hexdigest()
    
    def _is_cache_valid(self, cache_key):
        """Prüft ob Cache noch gültig ist"""
        if cache_key not in self.cache_timestamps:
            return False
        age = time.time() - self.cache_timestamps[cache_key]
        return age < self.cache_ttl
    
    def _get_from_cache(self, cache_key):
        """Holt Daten aus Cache wenn gültig"""
        if cache_key in self.memory_cache and self._is_cache_valid(cache_key):
            return self.memory_cache[cache_key]
        return None
    
    def _save_to_cache(self, cache_key, data):
        """Speichert Daten in Cache"""
        self.memory_cache[cache_key] = data
        self.cache_timestamps[cache_key] = time.time()
        
        # Bereinige alten Cache wenn zu groß (max 10 Einträge)
        if len(self.memory_cache) > 10:
            # Entferne älteste Einträge
            oldest_keys = sorted(self.cache_timestamps.items(), key=lambda x: x[1])[:5]
            for key, _ in oldest_keys:
                del self.memory_cache[key]
                del self.cache_timestamps[key]
    
    def load_dataset_optimized(self, source, dataset_name, columns=None, 
                              filters=None, sample_size=None):
        """
        Lädt Dataset mit Optimierungen
        
        Args:
            source: Datenquelle ('twin2sim', 'erentrudis', 'fis', 'kw')
            dataset_name: Name des Datasets
            columns: Optionale Spaltenliste zum Laden
            filters: Optionale Filter für Zeilen
            sample_size: Optionale Anzahl Zeilen für Sampling
        
        Returns:
            DataFrame oder None
        """
        start_time = time.time()
        
        # Check Cache
        cache_key = self._get_cache_key(source, dataset_name, columns, filters)
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            load_time = time.time() - start_time
            print(f"[CACHE] Aus Cache geladen: {dataset_name} ({load_time:.2f}s)")
            return cached_data
        
        # Versuche Parquet zu laden
        parquet_path = self._find_parquet_file(source, dataset_name)
        
        if parquet_path and parquet_path.exists():
            df = self._load_from_parquet(parquet_path, columns, filters, sample_size)
        else:
            # Fallback zu Legacy-Loading
            print(f"⚠️ Kein Parquet gefunden für {dataset_name}, verwende Legacy-Loader")
            df = self._load_legacy(source, dataset_name)
            
            if df is not None and not df.empty:
                # Optimiere für zukünftige Loads
                df = self._optimize_dataframe(df)
        
        # Cache das Ergebnis
        if df is not None and not df.empty:
            self._save_to_cache(cache_key, df)
        
        load_time = time.time() - start_time
        self.load_times.append(load_time)
        print(f"[GELADEN] {dataset_name} ({load_time:.2f}s, {len(df) if df is not None else 0:,} Zeilen)")
        
        return df
    
    def _find_parquet_file(self, source, dataset_name):
        """Findet die passende Parquet-Datei"""
        if not self.parquet_dir.exists():
            return None
        
        # Mapping von Dataset-Namen zu Dateinamen
        mappings = {
            'erentrudis': {
                'gesamtdaten_2024': 'Relevant-1_2024_export',
                'detail_juli_2024': 'All_24-07_export',
                'langzeit_2023_2025': 'export_ERS_2023'
            },
            'fis': {
                'export_q1_2025': 'export_1551_2024',
                'data_2024_2025_at': '2024-2025-05_AT'
            },
            'kw': {
                'kw_duernbach_gesamt': 'KW DÜRNBACH_ERZEUGUNG_2020_2024',
                'kw_untersulzbach_gesamt': 'KW UNTERSULZBACH_ERZEUGUNG_2020_2024',
                'kw_wiesbach_gesamt': 'KW WIESBACH_ERZEUGUNG_2020_2024',
                'uebergabe_bezug_gesamt': 'ÜBERGABE_BEZUG_2020_2024',
                'uebergabe_lieferung_gesamt': 'ÜBERGABE_LIEFERUNG_2020_2024'
            },
            'twin2sim': {
                'intpv': 'T2S_IntPV',
                'lüftung': 'T2S_Lüftung',
                'manipv': 'T2S_ManiPV',
                'rau006': 'T2S_RAU006',
                'wetterdaten': 'T2S_Wetterdaten'
            }
        }
        
        # Suche nach passendem Parquet-File
        if source in mappings and dataset_name in mappings[source]:
            pattern = mappings[source][dataset_name]
            for parquet_file in self.parquet_dir.glob("*.parquet"):
                if pattern.lower() in parquet_file.name.lower():
                    return parquet_file
        
        # Generischer Fallback
        for parquet_file in self.parquet_dir.glob("*.parquet"):
            if dataset_name.lower() in parquet_file.name.lower():
                return parquet_file
        
        return None
    
    def _load_from_parquet(self, parquet_path, columns=None, filters=None, sample_size=None):
        """Lädt Daten aus Parquet mit Optimierungen"""
        try:
            if sample_size:
                # Sampling für große Dateien
                pf = pq.ParquetFile(parquet_path)
                total_rows = pf.metadata.num_rows
                
                if total_rows > sample_size:
                    # Zufälliges Sampling
                    skip_rows = np.random.choice(
                        total_rows, 
                        total_rows - sample_size, 
                        replace=False
                    )
                    df = pd.read_parquet(
                        parquet_path,
                        columns=columns,
                        engine='pyarrow'
                    )
                    df = df.drop(skip_rows)
                else:
                    df = pd.read_parquet(
                        parquet_path,
                        columns=columns,
                        filters=filters,
                        engine='pyarrow'
                    )
            else:
                # Normales Laden mit optionalen Filtern
                df = pd.read_parquet(
                    parquet_path,
                    columns=columns,
                    filters=filters,
                    engine='pyarrow'
                )
            
            # WICHTIG: Stelle sicher, dass Date-Spalte existiert und korrekt ist
            if df.index.name in ['Date', 'DateTime', 'ZEIT_VON_UTC', 'Datum']:
                # Index ist bereits ein Datum - kopiere es als Spalte
                df['Date'] = df.index
            
            # Konvertiere Date-Spalten zu datetime wenn nötig
            date_cols = ['Date', 'DateTime', 'ZEIT_VON_UTC', 'ZEIT_BIS_UTC', 'Datum']
            for col in date_cols:
                if col in df.columns:
                    try:
                        df[col] = pd.to_datetime(df[col])
                    except:
                        pass
            
            return df
            
        except Exception as e:
            print(f"Fehler beim Parquet-Laden: {e}")
            return None
    
    def _load_legacy(self, source, dataset_name):
        """Legacy-Loader als Fallback"""
        try:
            if source == 'twin2sim':
                return self._load_twin2sim_legacy(dataset_name)
            elif source == 'erentrudis':
                return self._load_erentrudis_legacy(dataset_name)
            elif source == 'fis':
                return self._load_fis_legacy(dataset_name)
            elif source == 'kw':
                return self._load_kw_legacy(dataset_name)
        except Exception as e:
            print(f"Legacy-Loading fehlgeschlagen: {e}")
            return None
    
    def _optimize_dataframe(self, df):
        """Optimiert DataFrame für bessere Performance"""
        # Reduziere Speicherverbrauch
        for col in df.columns:
            col_type = df[col].dtype
            
            if col_type != 'object' and col_type != 'datetime64[ns]':
                c_min = df[col].min()
                c_max = df[col].max()
                
                if str(col_type)[:3] == 'int':
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                        df[col] = df[col].astype(np.int16)
                    elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                        df[col] = df[col].astype(np.int32)
                else:
                    if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                        df[col] = df[col].astype(np.float32)
        
        return df
    
    def load_dataset_paginated(self, source, dataset_name, page=1, page_size=1000):
        """
        Lädt Dataset seitenweise für große Datenmengen
        
        Args:
            source: Datenquelle
            dataset_name: Dataset Name
            page: Seitennummer (1-basiert)
            page_size: Anzahl Zeilen pro Seite
        
        Returns:
            DataFrame mit einer Seite Daten
        """
        # Lade komplettes Dataset (mit Cache)
        df = self.load_dataset_optimized(source, dataset_name)
        
        if df is None or df.empty:
            return pd.DataFrame()
        
        # Berechne Pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        return df.iloc[start_idx:end_idx]
    
    def get_dataset_info(self, source, dataset_name):
        """Gibt Informationen über ein Dataset zurück ohne es komplett zu laden"""
        parquet_path = self._find_parquet_file(source, dataset_name)
        
        if parquet_path and parquet_path.exists():
            pf = pq.ParquetFile(parquet_path)
            return {
                'rows': pf.metadata.num_rows,
                'columns': len(pf.schema),
                'column_names': [col.name for col in pf.schema],
                'size_mb': parquet_path.stat().st_size / (1024*1024),
                'format': 'parquet',
                'optimized': True
            }
        else:
            # Fallback: Lade Sample für Info
            df = self.load_dataset_optimized(source, dataset_name, sample_size=100)
            if df is not None:
                return {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': df.columns.tolist(),
                    'format': 'csv/excel',
                    'optimized': False
                }
        
        return None
    
    def preload_common_datasets(self):
        """Lädt häufig verwendete Datasets im Voraus"""
        common_datasets = [
            ('twin2sim', 'wetterdaten'),
            ('erentrudis', 'gesamtdaten_2024'),
            ('fis', 'export_q1_2025')
        ]
        
        print("[PRELOAD] Lade haeufige Datasets...")
        for source, dataset in common_datasets:
            self.load_dataset_optimized(source, dataset)
    
    def clear_cache(self):
        """Leert den Memory-Cache"""
        self.memory_cache.clear()
        self.cache_timestamps.clear()
        print("🗑️ Cache geleert")
    
    def get_performance_stats(self):
        """Gibt Performance-Statistiken zurück"""
        if not self.load_times:
            return None
        
        return {
            'avg_load_time': np.mean(self.load_times),
            'max_load_time': np.max(self.load_times),
            'min_load_time': np.min(self.load_times),
            'total_loads': len(self.load_times),
            'cache_size': len(self.memory_cache),
            'cache_hit_rate': len([t for t in self.load_times if t < 0.1]) / len(self.load_times)
        }
    
    # Legacy Loading Methods (vereinfacht)
    def _load_twin2sim_legacy(self, dataset_name):
        """Legacy Twin2Sim Loader"""
        file_map = {
            'intpv': 'T2S_IntPV.csv',
            'lüftung': 'T2S_Lüftung.csv',
            'manipv': 'T2S_ManiPV.csv',
            'rau006': 'T2S_RAU006.csv',
            'wetterdaten': 'T2S_Wetterdaten.csv'
        }
        
        if dataset_name in file_map:
            filepath = self.twin2sim_path / file_map[dataset_name]
            if filepath.exists():
                return pd.read_csv(filepath, sep=';', decimal=',', parse_dates=True)
        return None
    
    def _load_erentrudis_legacy(self, dataset_name):
        """Legacy Erentrudis Loader"""
        file_map = {
            'gesamtdaten_2024': self.erentrudis_path / "Monitoring" / "2024" / 
                               "Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv",
            'detail_juli_2024': self.erentrudis_path / "Monitoring" / "2024" / 
                               "All_24-07_export_2011_2024-07-01-00-00_2024-07-31-23-59.csv",
            'langzeit_2023_2025': self.erentrudis_path / "Monitoring" / 
                                 "export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv"
        }
        
        if dataset_name in file_map and file_map[dataset_name].exists():
            return pd.read_csv(file_map[dataset_name], parse_dates=True)
        return None
    
    def _load_fis_legacy(self, dataset_name):
        """Legacy FIS Loader"""
        file_map = {
            'export_q1_2025': self.fis_path / "Monitoring" / "250101-250331" / 
                             "export_1551_2024-12-31-00-00_2025-03-31-23-55.csv",
            'data_2024_2025_at': self.fis_path / "Monitoring" / "2024-2025-05_AT.csv"
        }
        
        if dataset_name in file_map and file_map[dataset_name].exists():
            return pd.read_csv(file_map[dataset_name], parse_dates=True)
        return None
    
    def _load_kw_legacy(self, dataset_name):
        """Legacy KW Loader - Lädt ALLE Jahre 2020-2024"""
        dfs = []
        
        # Bestimme welches Kraftwerk
        if 'duernbach' in dataset_name.lower():
            base_name = "KW DÜRNBACH_ERZEUGUNG"
        elif 'untersulzbach' in dataset_name.lower():
            base_name = "KW UNTERSULZBACH_ERZEUGUNG"
        elif 'wiesbach' in dataset_name.lower():
            base_name = "KW WIESBACH_ERZEUGUNG"
        else:
            return None
        
        # Lade ALLE Jahre (2020-2024)
        for year in range(2020, 2025):  # 2020 bis 2024
            file_path = self.kw_path / f"{base_name}_{year}.XLSX"
            if file_path.exists():
                try:
                    df = pd.read_excel(file_path, engine='openpyxl')
                    # Füge Jahr als Spalte hinzu für Nachverfolgbarkeit
                    df['Jahr'] = year
                    dfs.append(df)
                    print(f"   [OK] {base_name} {year}: {len(df):,} Zeilen")
                except Exception as e:
                    print(f"   [FEHLER] bei {file_path.name}: {e}")
        
        if dfs:
            # Kombiniere alle Jahre
            combined_df = pd.concat(dfs, ignore_index=True)
            
            # Stelle sicher, dass Date-Spalte existiert
            if 'ZEIT_VON_UTC' in combined_df.columns:
                combined_df['Date'] = pd.to_datetime(combined_df['ZEIT_VON_UTC'])
            elif 'Date' not in combined_df.columns:
                # Fallback: erstelle Date aus Index oder Jahr
                combined_df['Date'] = pd.date_range(start='2020-01-01', periods=len(combined_df), freq='H')
            
            print(f"   → Gesamt: {len(combined_df):,} Zeilen (2020-2024)")
            return combined_df
        
        return None