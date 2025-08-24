"""
Optimierter Datenlade-Modul für MokiG Dashboard - Quiet Version
================================================================
Lädt alle Daten mit minimalen Ausgaben für schnelleren Start.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from functools import lru_cache
import warnings
import os
warnings.filterwarnings('ignore')


class DataLoader:
    """Zentrale Klasse für das Laden aller Datenquellen - Optimiert"""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.twin2sim_path = self.base_path / "Daten" / "Beispieldaten"
        self.erentrudis_path = self.base_path / "Daten" / "Monitoringdaten" / "Erentrudisstr"
        self.fis_path = self.base_path / "Daten" / "Monitoringdaten" / "FIS_Inhauser"
        self.kw_path = self.base_path / "Daten" / "vertraulich_erzeugungsdaten-kw-neukirchen_2025-07-21_0937"
        self.verbose = os.environ.get('DASHBOARD_VERBOSE', 'false').lower() == 'true'
    
    def log(self, message, level='info'):
        """Bedingte Ausgabe basierend auf Verbose-Modus"""
        if self.verbose:
            if level == 'success':
                print(f"[OK] {message}")
            elif level == 'warning':
                print(f"  [WARNUNG] {message}")
            elif level == 'error':
                print(f"[FEHLER] {message}")
            else:
                print(message)
    
    def load_csv_flexible(self, filepath, name, source_type="generic"):
        """Flexibler CSV-Loader - Quiet Version"""
        try:
            encodings = ['utf-8-sig', 'utf-8', 'iso-8859-1', 'windows-1252', 'cp1252']
            df = None
            
            # Lade CSV mit passender Encoding
            for encoding in encodings:
                for sep in [',', ';', '\t']:
                    try:
                        df = pd.read_csv(filepath, sep=sep, encoding=encoding, 
                                       decimal=',', dayfirst=True, 
                                       parse_dates=True, infer_datetime_format=True)
                        if df is not None and not df.empty:
                            break
                    except:
                        continue
                if df is not None and not df.empty:
                    break
            
            if df is None:
                return pd.DataFrame()
            
            # Datums-Verarbeitung
            df = self._process_datetime_columns_improved(df, source_type)
            
            # Numerische Spalten konvertieren
            for col in df.columns:
                if col not in ['Date', 'DateTime', 'Datum + Uhrzeit', 'Datum', 'Zeit']:
                    if df[col].dtype == 'object':
                        df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
                        df[col] = pd.to_numeric(df[col], errors='coerce')
            
            self.log(f"{source_type} {name}: {len(df)} Zeilen, {len(df.columns)} Spalten", 'success')
            return df
            
        except Exception as e:
            self.log(f"Fehler beim Laden von {name}: {e}", 'error')
            return pd.DataFrame()
    
    def _process_datetime_columns_improved(self, df, source_type):
        """Verbesserte Datumsverarbeitung - Quiet Version"""
        date_columns = ['Date', 'Datum + Uhrzeit', 'DateTime', 'Time', 'Timestamp', 'Zeit', 'Datum']
        date_col_name = None
        
        # Finde Datumsspalte
        for col in df.columns:
            for date_col in date_columns:
                if date_col.lower() in col.lower():
                    date_col_name = col
                    break
            if date_col_name:
                break
        
        if date_col_name:
            try:
                df['Date'] = pd.to_datetime(df[date_col_name], 
                                           infer_datetime_format=True,
                                           errors='coerce',
                                           dayfirst=True)
                
                # Entferne ungültige Dates
                invalid_dates = df['Date'].isna().sum()
                if invalid_dates > 0 and invalid_dates < len(df) * 0.1:
                    df = df.dropna(subset=['Date'])
                    self.log(f"{invalid_dates} Zeilen mit ungültigen Datumswerten entfernt", 'warning')
            except:
                pass
        
        # Falls kein Datum, erstelle Index-basiertes
        if 'Date' not in df.columns or df['Date'].isna().all():
            df['Date'] = pd.date_range(start='2024-01-01', periods=len(df), freq='H')
        
        return df
    
    def load_excel_flexible(self, filepath, name):
        """Excel-Loader - Quiet Version"""
        try:
            file_ext = str(filepath).lower()
            
            if file_ext.endswith('.xlsx'):
                df = pd.read_excel(filepath, engine='openpyxl')
            elif file_ext.endswith('.xls'):
                try:
                    import xlrd
                    df = pd.read_excel(filepath, engine='xlrd')
                except ImportError:
                    self.log(f"xlrd nicht installiert für {name}", 'warning')
                    return pd.DataFrame()
            else:
                df = pd.read_excel(filepath, engine='openpyxl')
            
            # Spaltennamen normalisieren
            column_mapping = {
                'ZEIT_VON_UTC': 'Date',
                'WERT': 'Value',
                'Energie (kWh)': 'Energy_kWh',
                'Leistung (kW)': 'Power_kW',
            }
            df = df.rename(columns=column_mapping)
            
            # Datum konvertieren
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            
            self.log(f"Excel {name}: {len(df)} Zeilen", 'success')
            return df
            
        except Exception as e:
            self.log(f"Fehler bei {name}: {e}", 'error')
            return pd.DataFrame()
    
    def aggregate_kw_datasets(self, datasets_dict, pattern, name):
        """Aggregiert KW Datasets - Quiet Version"""
        matching_dfs = []
        
        for key, df in datasets_dict.items():
            if pattern.lower() in key.lower() and not df.empty:
                df_copy = df.copy()
                df_copy['Quelle'] = key
                matching_dfs.append(df_copy)
        
        if matching_dfs:
            combined_df = pd.concat(matching_dfs, ignore_index=True)
            if 'Date' in combined_df.columns:
                combined_df = combined_df.sort_values('Date')
            self.log(f"Aggregiert: {name} - {len(matching_dfs)} Dateien, {len(combined_df):,} Zeilen", 'success')
            return combined_df
        else:
            return pd.DataFrame()
    
    @lru_cache(maxsize=1)
    def load_all_data(self):
        """Lädt alle Daten - Optimiert mit minimalen Ausgaben"""
        data = {
            'twin2sim': {},
            'erentrudis': {},
            'fis': {},
            'kw': {}
        }
        
        # Zusammenfassung am Anfang nur wenn verbose
        if self.verbose:
            print("\n" + "="*60)
            print("Lade Datenquellen...")
            print("="*60)
        else:
            print("Lade Daten... ", end='', flush=True)
        
        # Twin2Sim
        if self.twin2sim_path.exists():
            for file in self.twin2sim_path.glob("*.csv"):
                key = file.stem.lower().replace('t2s_', '')
                data['twin2sim'][key] = self.load_csv_flexible(file, file.stem, "twin2sim")
        
        # Erentrudisstraße - 3 Haupt-Datasets
        if self.erentrudis_path.exists():
            monitoring_path = self.erentrudis_path / "Monitoring"
            if monitoring_path.exists():
                files = [
                    (monitoring_path / "2024" / "Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv", 'gesamtdaten_2024'),
                    (monitoring_path / "2024" / "All_24-07_export_2011_2024-07-01-00-00_2024-07-31-23-59.csv", 'detail_juli_2024'),
                    (monitoring_path / "export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv", 'langzeit_2023_2025')
                ]
                for filepath, key in files:
                    if filepath.exists():
                        data['erentrudis'][key] = self.load_csv_flexible(filepath, key, "erentrudis")
        
        # FIS Inhauser - 2 Haupt-Datasets
        if self.fis_path.exists():
            monitoring_path = self.fis_path / "Monitoring"
            files = [
                (monitoring_path / "250101-250331" / "export_1551_2024-12-31-00-00_2025-03-31-23-55.csv", 'export_q1_2025'),
                (monitoring_path / "2024-2025-05_AT.csv", 'data_2024_2025_at')
            ]
            for filepath, key in files:
                if filepath.exists():
                    data['fis'][key] = self.load_csv_flexible(filepath, key, "fis")
        
        # KW Neukirchen
        if self.kw_path.exists():
            temp_kw_data = {}
            
            # Lade Excel-Dateien
            for xlsx_file in self.kw_path.glob("KW*.XLSX"):
                key = xlsx_file.stem
                temp_kw_data[key] = self.load_excel_flexible(xlsx_file, key)
            
            for year_dir in self.kw_path.iterdir():
                if year_dir.is_dir() and year_dir.name.isdigit():
                    for xlsx_file in year_dir.glob("*.XLSX"):
                        key = f"{year_dir.name}_{xlsx_file.stem}"
                        temp_kw_data[key] = self.load_excel_flexible(xlsx_file, key)
            
            # Aggregiere in Gruppen
            data['kw']['uebergabe_bezug_gesamt'] = self.aggregate_kw_datasets(
                temp_kw_data, 'ÜBERGABE_BEZUG', 'Übergabe Bezug'
            )
            data['kw']['uebergabe_lieferung_gesamt'] = self.aggregate_kw_datasets(
                temp_kw_data, 'ÜBERGABE_LIEFERUNG', 'Übergabe Lieferung'
            )
            data['kw']['kw_duernbach_gesamt'] = self.aggregate_kw_datasets(
                temp_kw_data, 'KW DÜRNBACH', 'Kraftwerk Dürnbach'
            )
            data['kw']['kw_untersulzbach_gesamt'] = self.aggregate_kw_datasets(
                temp_kw_data, 'KW UNTERSULZBACH', 'Kraftwerk Untersulzbach'
            )
            data['kw']['kw_wiesbach_gesamt'] = self.aggregate_kw_datasets(
                temp_kw_data, 'KW WIESBACH', 'Kraftwerk Wiesbach'
            )
        
        # Zusammenfassung
        if not self.verbose:
            total_datasets = sum(len([d for d in datasets.values() if not d.empty]) for datasets in data.values())
            print(f"OK - {total_datasets} Datasets geladen")
        else:
            print("\n" + "="*60)
            print("Zusammenfassung:")
            for source, datasets in data.items():
                valid_count = len([d for d in datasets.values() if not d.empty])
                print(f"  {source}: {valid_count} Datasets")
            print("="*60)
        
        return data