"""
Datenlade-Modul für MokiG Dashboard
====================================
Handhabt das Laden und Verarbeiten aller Datenquellen.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from functools import lru_cache
import warnings
warnings.filterwarnings('ignore')


class DataLoader:
    """Zentrale Klasse für das Laden aller Datenquellen"""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.twin2sim_path = self.base_path / "Daten" / "Beispieldaten"
        self.erentrudis_path = self.base_path / "Daten" / "Monitoringdaten" / "Erentrudisstr"
        self.fis_path = self.base_path / "Daten" / "Monitoringdaten" / "FIS_Inhauser"
        self.kw_path = self.base_path / "Daten" / "vertraulich_erzeugungsdaten-kw-neukirchen_2025-07-21_0937"
    
    def load_csv_flexible(self, filepath, name, source_type="generic"):
        """
        Flexibler CSV-Loader mit mehreren Encoding-Optionen.
        Behebt das Problem mit leeren Datum-Werten durch bessere Fehlerbehandlung.
        """
        try:
            encodings = ['utf-8-sig', 'utf-8', 'iso-8859-1', 'windows-1252', 'cp1252']
            df = None
            
            # Spezielle Behandlung je nach Datenquelle
            if source_type == "erentrudis":
                for encoding in encodings:
                    try:
                        df = pd.read_csv(filepath, sep=',', encoding=encoding, decimal=',', dayfirst=True)
                        if df is not None and not df.empty:
                            break
                    except:
                        continue
            
            elif source_type == "twin2sim":
                separators = [';', ',', '\t']
                for encoding in encodings:
                    for sep in separators:
                        try:
                            df = pd.read_csv(filepath, sep=sep, decimal=',', encoding=encoding)
                            # Überspringe Header-Zeilen wenn vorhanden
                            if len(df) > 2 and df.iloc[0].isna().sum() > len(df.columns) * 0.5:
                                original_columns = df.columns.tolist()
                                df = df.iloc[2:].reset_index(drop=True)
                                df.columns = original_columns
                            if df is not None and not df.empty:
                                break
                        except:
                            continue
                    if df is not None and not df.empty:
                        break
            
            else:
                # Standard-Behandlung
                separators = [';', ',', '\t']
                for encoding in encodings:
                    for sep in separators:
                        try:
                            df = pd.read_csv(filepath, sep=sep, encoding=encoding)
                            if df is not None and not df.empty:
                                break
                        except:
                            continue
                    if df is not None and not df.empty:
                        break
            
            if df is None:
                return pd.DataFrame()
            
            # Verbesserte Datumsspalten-Verarbeitung
            df = self._process_datetime_columns(df, source_type)
            
            # Numerische Spalten konvertieren
            for col in df.columns:
                if col != 'Date' and df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.replace(',', '.')
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            print(f"✓ {source_type} {name}: {len(df)} Zeilen, {len(df.columns)} Spalten")
            return df
            
        except Exception as e:
            print(f"✗ Fehler beim Laden von {name}: {e}")
            return pd.DataFrame()
    
    def _process_datetime_columns(self, df, source_type):
        """
        Verarbeitet und standardisiert Datumsspalten.
        Behebt das Problem mit leeren/ungültigen Datumswerten.
        """
        date_columns = ['Date', 'Datum + Uhrzeit', 'Time', 'Timestamp', 'Zeit', 
                       'ZEIT_VON_UTC', 'ZEIT_BIS_UTC', 'Datum', 'DateTime']
        
        date_found = False
        
        # Suche nach Datumsspalte
        for col in date_columns:
            if col in df.columns:
                try:
                    # Konvertiere zu datetime mit verbesserter Fehlerbehandlung
                    df['Date'] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
                    
                    # Fülle fehlende Werte mit linearer Interpolation
                    if df['Date'].isna().sum() > 0 and df['Date'].notna().sum() > 0:
                        # Versuche Zeitstempel zu interpolieren für kleinere Lücken
                        df['Date'] = df['Date'].interpolate(method='time', limit=10)
                    
                    # Entferne Zeilen mit immer noch fehlenden Datumswerten
                    initial_len = len(df)
                    df = df.dropna(subset=['Date'])
                    
                    if len(df) < initial_len:
                        print(f"  ⚠ {initial_len - len(df)} Zeilen mit ungültigen Datumswerten entfernt")
                    
                    date_found = True
                    break
                except Exception as e:
                    print(f"  ⚠ Warnung bei Datumskonvertierung ({col}): {e}")
                    continue
        
        # Falls keine Datumsspalte gefunden, versuche erste Spalte
        if not date_found and len(df.columns) > 0:
            first_col = df.columns[0]
            if any(keyword in first_col.lower() for keyword in ['date', 'zeit', 'time']):
                try:
                    df['Date'] = pd.to_datetime(df[first_col], errors='coerce', dayfirst=True)
                    df = df.dropna(subset=['Date'])
                    date_found = True
                except:
                    pass
        
        # Falls immer noch kein Datum, erstelle Index-basiertes Datum
        if not date_found and len(df) > 0:
            print(f"  ℹ Keine Datumsspalte gefunden, verwende Index")
            df['Date'] = pd.date_range(start='2024-01-01', periods=len(df), freq='H')
        
        return df
    
    def load_excel_flexible(self, filepath, name):
        """Flexibler Excel-Loader mit verbesserter Fehlerbehandlung"""
        try:
            # Versuche verschiedene Engines
            try:
                df = pd.read_excel(filepath, engine='openpyxl')
            except:
                try:
                    df = pd.read_excel(filepath)
                except:
                    df = pd.read_excel(filepath, engine='xlrd')
            
            # Spaltennamen normalisieren
            column_mapping = {
                'ZEIT_VON_UTC': 'Date',
                'ZEIT_BIS_UTC': 'Date_To',
                'Zeit_Von': 'Date',
                'WERT': 'Value',
                'Energie (kWh)': 'Energy_kWh',
                'Leistung (kW)': 'Power_kW',
                'EINHEIT': 'Unit',
                'DateTime': 'Date'
            }
            
            df = df.rename(columns=column_mapping)
            
            # Datum konvertieren mit verbesserter Fehlerbehandlung
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                initial_len = len(df)
                df = df.dropna(subset=['Date'])
                if len(df) < initial_len:
                    print(f"  ⚠ {initial_len - len(df)} Zeilen mit ungültigen Datumswerten entfernt")
            
            # Numerische Spalten
            numeric_cols = ['Value', 'Energy_kWh', 'Power_kW', 'WERT']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            print(f"✓ Excel {name}: {len(df)} Zeilen")
            return df
            
        except Exception as e:
            print(f"✗ Fehler bei {name}: {e}")
            return pd.DataFrame()
    
    @lru_cache(maxsize=1)
    def load_all_data(self):
        """Lädt ALLE Daten aus allen Quellen (gecached)"""
        data = {
            'twin2sim': {},
            'erentrudis': {},
            'fis': {},
            'kw': {}
        }
        
        print("\n" + "="*60)
        print("Lade alle Datenquellen...")
        print("="*60)
        
        # Twin2Sim
        if self.twin2sim_path.exists():
            for file in self.twin2sim_path.glob("*.csv"):
                key = file.stem.lower().replace('t2s_', '')[:30]
                data['twin2sim'][key] = self.load_csv_flexible(file, file.stem, "twin2sim")
        
        # Erentrudisstraße
        if self.erentrudis_path.exists():
            monitoring_path = self.erentrudis_path / "Monitoring"
            if monitoring_path.exists():
                # CSV Dateien direkt im Monitoring-Ordner
                for csv_file in monitoring_path.glob("*.csv"):
                    key = csv_file.stem[:30]
                    data['erentrudis'][key] = self.load_csv_flexible(csv_file, key, "erentrudis")
                
                # Unterordner durchsuchen
                for subdir in monitoring_path.iterdir():
                    if subdir.is_dir():
                        for csv_file in subdir.rglob("*.csv"):
                            key = f"{subdir.name}_{csv_file.stem}"[:30]
                            data['erentrudis'][key] = self.load_csv_flexible(csv_file, key, "erentrudis")
        
        # FIS
        if self.fis_path.exists():
            monitoring_path = self.fis_path / "Monitoring"
            if monitoring_path.exists():
                # Excel-Dateien
                for xlsx_file in monitoring_path.glob("*.xlsx"):
                    key = xlsx_file.stem[:30]
                    data['fis'][key] = self.load_excel_flexible(xlsx_file, key)
                
                # CSV in Unterordnern
                for subdir in monitoring_path.iterdir():
                    if subdir.is_dir():
                        for csv_file in subdir.rglob("*.csv"):
                            key = f"{subdir.name}_{csv_file.stem}"[:30]
                            data['fis'][key] = self.load_csv_flexible(csv_file, key, "fis")
        
        # KW Neukirchen
        if self.kw_path.exists():
            # Erzeugungsdaten
            for xlsx_file in self.kw_path.glob("KW*.XLSX"):
                key = xlsx_file.stem.lower().replace(' ', '_')[:30]
                data['kw'][key] = self.load_excel_flexible(xlsx_file, xlsx_file.stem)
            
            # Bezugs- und Lieferungsdaten
            for year_dir in self.kw_path.glob("20*"):
                if year_dir.is_dir():
                    for xlsx_file in year_dir.glob("*.XLSX"):
                        key = f"{year_dir.name}_{xlsx_file.stem}"[:30]
                        data['kw'][key] = self.load_excel_flexible(xlsx_file, key)
        
        # Statistiken ausgeben
        self._print_statistics(data)
        
        return data
    
    def _print_statistics(self, data):
        """Gibt Ladestatistiken aus"""
        for source, datasets in data.items():
            if datasets:
                total = sum(len(df) for df in datasets.values() if not df.empty)
                count = sum(1 for df in datasets.values() if not df.empty)
                print(f"\n{source.upper()}: {count} Datasets, {total:,} Zeilen")
                for key in list(datasets.keys())[:3]:
                    df = datasets[key]
                    if not df.empty:
                        print(f"  - {key}: {len(df):,} Zeilen")
        
        print("\n" + "="*60 + "\n")