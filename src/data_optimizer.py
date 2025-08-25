"""
Data Optimizer für MokiG Dashboard
===================================
Konvertiert CSV/Excel Dateien in optimierte Parquet-Formate für schnelleren Datenzugriff.
Inkludiert Caching, Indizierung und Kompression.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import pyarrow.parquet as pq
import pyarrow as pa
import pickle
import hashlib
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class DataOptimizer:
    """Optimiert Datenladezeiten durch Parquet-Format und intelligentes Caching"""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.cache_dir = self.base_path / "cache"
        self.parquet_dir = self.base_path / "data_optimized"
        
        # Erstelle Cache-Verzeichnisse
        self.cache_dir.mkdir(exist_ok=True)
        self.parquet_dir.mkdir(exist_ok=True)
        
        # Metadaten für optimierte Dateien
        self.metadata_file = self.parquet_dir / "metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self):
        """Lädt Metadaten über optimierte Dateien"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_metadata(self):
        """Speichert Metadaten"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2, default=str)
    
    def get_file_hash(self, filepath):
        """Berechnet Hash einer Datei für Change Detection"""
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def convert_to_parquet(self, source_file, source_type="csv", force=False):
        """
        Konvertiert CSV/Excel zu Parquet mit Optimierungen
        
        Args:
            source_file: Pfad zur Quelldatei
            source_type: 'csv' oder 'excel'
            force: Erzwingt Neukonvertierung
        
        Returns:
            Path zum optimierten Parquet-File
        """
        source_path = Path(source_file)
        file_hash = self.get_file_hash(source_path)
        
        # Prüfe ob bereits konvertiert und aktuell
        parquet_name = f"{source_path.stem}_{file_hash[:8]}.parquet"
        parquet_path = self.parquet_dir / parquet_name
        
        # Check if conversion needed
        if not force and parquet_path.exists():
            if source_path.stem in self.metadata:
                if self.metadata[source_path.stem].get('hash') == file_hash:
                    print(f"✓ Verwende existierende Parquet-Datei: {parquet_name}")
                    return parquet_path
        
        print(f"🔄 Konvertiere {source_path.name} zu Parquet...")
        
        # Lade Daten
        try:
            if source_type == "csv":
                df = self._load_csv_optimized(source_path)
            else:
                df = self._load_excel_optimized(source_path)
            
            if df.empty:
                return None
            
            # Optimierungen vor dem Speichern
            df = self._optimize_datatypes(df)
            df = self._add_indices(df)
            
            # Speichere als Parquet mit Kompression
            table = pa.Table.from_pandas(df, preserve_index=True)
            pq.write_table(
                table, 
                parquet_path,
                compression='snappy',  # Schnelle Kompression (keine compression_level für snappy)
                use_dictionary=True   # Dictionary encoding für kategorische Daten
            )
            
            # Update Metadaten
            self.metadata[source_path.stem] = {
                'hash': file_hash,
                'original_file': str(source_path),
                'parquet_file': str(parquet_path),
                'rows': len(df),
                'columns': len(df.columns),
                'size_mb': parquet_path.stat().st_size / (1024*1024),
                'converted_at': datetime.now().isoformat(),
                'compression_ratio': source_path.stat().st_size / parquet_path.stat().st_size
            }
            self._save_metadata()
            
            print(f"✓ Konvertiert: {len(df):,} Zeilen, "
                  f"Kompression: {self.metadata[source_path.stem]['compression_ratio']:.1f}x")
            
            return parquet_path
            
        except Exception as e:
            print(f"✗ Fehler bei Konvertierung: {e}")
            return None
    
    def _load_csv_optimized(self, filepath):
        """Optimiertes CSV-Laden mit Type Inference"""
        try:
            # Versuche verschiedene Separatoren
            for sep in [';', ',', '\t']:
                try:
                    # Erste Zeilen für Type Inference
                    sample = pd.read_csv(filepath, nrows=100, sep=sep)
                    
                    if len(sample.columns) > 1:  # Gültiger Separator gefunden
                        # Lade vollständige Datei
                        df = pd.read_csv(
                            filepath,
                            sep=sep,
                            parse_dates=True,
                            infer_datetime_format=True,
                            low_memory=False  # Für c engine
                        )
                        
                        # Optimiere Datentypen nach dem Laden
                        for col in df.columns:
                            if df[col].dtype == 'object':
                                # Versuche numerische Konvertierung
                                try:
                                    # Ersetze Komma durch Punkt für deutsche Zahlen
                                    if df[col].astype(str).str.contains(',').any():
                                        df[col] = df[col].str.replace(',', '.', regex=False)
                                    df[col] = pd.to_numeric(df[col], errors='coerce')
                                except:
                                    # Check if categorical
                                    if df[col].nunique() < len(df) * 0.5:
                                        df[col] = df[col].astype('category')
                            elif df[col].dtype == 'float64':
                                df[col] = df[col].astype('float32')
                            elif df[col].dtype == 'int64':
                                # Downcast integers
                                if df[col].min() >= 0 and df[col].max() < 2147483647:
                                    df[col] = df[col].astype('int32')
                        
                        return df
                except:
                    continue
            
            # Fallback
            print(f"Warnung: Konnte keinen passenden Separator finden, verwende Standard")
            return pd.read_csv(filepath)
            
        except Exception as e:
            print(f"Fehler beim CSV-Laden: {e}")
            return pd.DataFrame()
    
    def _load_excel_optimized(self, filepath):
        """Optimiertes Excel-Laden"""
        try:
            df = pd.read_excel(filepath, engine='openpyxl')
            return df
        except:
            try:
                df = pd.read_excel(filepath, engine='xlrd')
                return df
            except Exception as e:
                print(f"Fehler beim Excel-Laden: {e}")
                return pd.DataFrame()
    
    def _optimize_datatypes(self, df):
        """Optimiert Datentypen für minimalen Speicherverbrauch"""
        for col in df.columns:
            col_type = df[col].dtype
            
            # Optimiere Integer
            if col_type != 'object' and col_type != 'datetime64[ns]':
                if 'int' in str(col_type):
                    # Downcast integers
                    if df[col].min() >= 0:
                        if df[col].max() < 255:
                            df[col] = df[col].astype('uint8')
                        elif df[col].max() < 65535:
                            df[col] = df[col].astype('uint16')
                        elif df[col].max() < 4294967295:
                            df[col] = df[col].astype('uint32')
                    else:
                        if df[col].min() > -128 and df[col].max() < 127:
                            df[col] = df[col].astype('int8')
                        elif df[col].min() > -32768 and df[col].max() < 32767:
                            df[col] = df[col].astype('int16')
                        elif df[col].min() > -2147483648 and df[col].max() < 2147483647:
                            df[col] = df[col].astype('int32')
                
                # Optimiere Floats
                elif 'float' in str(col_type):
                    df[col] = pd.to_numeric(df[col], downcast='float')
            
            # Konvertiere Strings zu Kategorien wenn sinnvoll
            elif col_type == 'object':
                num_unique = df[col].nunique()
                num_total = len(df[col])
                if num_unique / num_total < 0.5:  # Weniger als 50% unique
                    df[col] = df[col].astype('category')
        
        return df
    
    def _add_indices(self, df):
        """Fügt Indizes für schnellere Abfragen hinzu"""
        # WICHTIG: Setze Datum als Index OHNE drop=False zu verlieren
        date_columns = ['Date', 'DateTime', 'Datum', 'Datum + Uhrzeit', 'Zeit', 'ZEIT_VON_UTC', 'Zeitstempel']
        for col in date_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                    # WICHTIG: drop=False behält die Spalte im DataFrame!
                    df = df.set_index(col, drop=False)
                    df = df.sort_index()
                    break
                except:
                    continue
        
        # Stelle sicher, dass Date-Spalte existiert
        if 'Date' not in df.columns and df.index.name in date_columns:
            df['Date'] = df.index
        
        return df
    
    def load_parquet_chunked(self, parquet_path, chunk_size=10000):
        """Lädt Parquet-Datei in Chunks für große Dateien"""
        parquet_file = pq.ParquetFile(parquet_path)
        
        for batch in parquet_file.iter_batches(batch_size=chunk_size):
            yield batch.to_pandas()
    
    def load_parquet_filtered(self, parquet_path, columns=None, filters=None):
        """
        Lädt Parquet mit Spalten- und Zeilenfiltern
        
        Args:
            parquet_path: Pfad zur Parquet-Datei
            columns: Liste der zu ladenden Spalten
            filters: PyArrow Filter Expression
        
        Returns:
            Gefilterter DataFrame
        """
        return pd.read_parquet(
            parquet_path,
            columns=columns,
            filters=filters,
            engine='pyarrow'
        )
    
    def get_parquet_info(self, parquet_path):
        """Gibt Informationen über eine Parquet-Datei zurück"""
        pf = pq.ParquetFile(parquet_path)
        
        return {
            'num_rows': pf.metadata.num_rows,
            'num_columns': len(pf.schema),
            'columns': [col.name for col in pf.schema],
            'size_mb': Path(parquet_path).stat().st_size / (1024*1024),
            'compression': pf.metadata.row_group(0).column(0).compression,
            'created': datetime.fromtimestamp(Path(parquet_path).stat().st_ctime)
        }
    
    def preprocess_all_data(self):
        """Konvertiert alle Datenquellen zu Parquet"""
        conversions = []
        
        # Twin2Sim Daten
        twin2sim_path = self.base_path / "Daten" / "Beispieldaten"
        if twin2sim_path.exists():
            print("\n📊 Konvertiere Twin2Sim Daten...")
            for csv_file in twin2sim_path.glob("*.csv"):
                result = self.convert_to_parquet(csv_file, "csv")
                if result:
                    conversions.append(result)
        
        # Erentrudisstraße Daten
        erentrudis_path = self.base_path / "Daten" / "Monitoringdaten" / "Erentrudisstr" / "Monitoring"
        if erentrudis_path.exists():
            print("\n🏢 Konvertiere Erentrudisstraße Daten...")
            # Spezifische wichtige Dateien
            important_files = [
                erentrudis_path / "2024" / "Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv",
                erentrudis_path / "2024" / "All_24-07_export_2011_2024-07-01-00-00_2024-07-31-23-59.csv",
                erentrudis_path / "export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv"
            ]
            for csv_file in important_files:
                if csv_file.exists():
                    result = self.convert_to_parquet(csv_file, "csv")
                    if result:
                        conversions.append(result)
        
        # FIS Inhauser Daten
        fis_path = self.base_path / "Daten" / "Monitoringdaten" / "FIS_Inhauser" / "Monitoring"
        if fis_path.exists():
            print("\n🏭 Konvertiere FIS Inhauser Daten...")
            important_files = [
                fis_path / "250101-250331" / "export_1551_2024-12-31-00-00_2025-03-31-23-55.csv",
                fis_path / "2024-2025-05_AT.csv"
            ]
            for csv_file in important_files:
                if csv_file.exists():
                    result = self.convert_to_parquet(csv_file, "csv")
                    if result:
                        conversions.append(result)
        
        # KW Neukirchen Excel-Daten (nur Hauptdateien)
        kw_path = self.base_path / "Daten" / "vertraulich_erzeugungsdaten-kw-neukirchen_2025-07-21_0937"
        if kw_path.exists():
            print("\n⚡ Konvertiere KW Neukirchen Daten...")
            # Nur die aggregierten Hauptdateien
            for xlsx_file in kw_path.glob("KW*.XLSX"):
                result = self.convert_to_parquet(xlsx_file, "excel")
                if result:
                    conversions.append(result)
        
        print(f"\n✅ Konvertierung abgeschlossen: {len(conversions)} Dateien optimiert")
        return conversions