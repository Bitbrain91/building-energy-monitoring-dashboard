"""
Verbesserter Datenlade-Modul für MokiG Dashboard
================================================
Behebt Probleme mit Datumsspalten und lädt alle Datasets korrekt.
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
        Flexibler CSV-Loader mit verbesserter Datumsbehandlung.
        """
        try:
            encodings = ['utf-8-sig', 'utf-8', 'iso-8859-1', 'windows-1252', 'cp1252']
            df = None
            
            # Spezielle Behandlung je nach Datenquelle
            if source_type == "erentrudis":
                # Erentrudis hat oft spezielle Formatierung
                for encoding in encodings:
                    try:
                        # Versuche verschiedene Trennzeichen
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
                    except:
                        continue
            
            elif source_type == "twin2sim":
                # Twin2Sim Format
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
            
            elif source_type == "fis":
                # FIS Format - oft mit speziellen Headers
                for encoding in encodings:
                    for sep in [',', ';', '\t']:
                        try:
                            df = pd.read_csv(filepath, sep=sep, encoding=encoding,
                                           parse_dates=True, infer_datetime_format=True)
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
            df = self._process_datetime_columns_improved(df, source_type)
            
            # Numerische Spalten konvertieren
            for col in df.columns:
                if col not in ['Date', 'DateTime', 'Datum + Uhrzeit', 'Datum', 'Zeit']:
                    if df[col].dtype == 'object':
                        # Ersetze Komma durch Punkt für deutsche Zahlenformate
                        df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
                        df[col] = pd.to_numeric(df[col], errors='coerce')
            
            print(f"✓ {source_type} {name}: {len(df)} Zeilen, {len(df.columns)} Spalten")
            return df
            
        except Exception as e:
            print(f"✗ Fehler beim Laden von {name}: {e}")
            return pd.DataFrame()
    
    def _process_datetime_columns_improved(self, df, source_type):
        """
        Verbesserte Verarbeitung von Datumsspalten.
        Behebt das Problem mit leeren Datum + Uhrzeit Werten.
        """
        # Mögliche Datumsspalten-Namen
        date_columns = [
            'Date', 'Datum + Uhrzeit', 'Datum+Uhrzeit', 'DateTime', 
            'Time', 'Timestamp', 'Zeit', 'Datum', 
            'ZEIT_VON_UTC', 'ZEIT_BIS_UTC', 'Zeitstempel'
        ]
        
        date_found = False
        date_col_name = None
        
        # Suche nach Datumsspalte (case-insensitive)
        for col in df.columns:
            for date_col in date_columns:
                if date_col.lower() in col.lower():
                    date_col_name = col
                    break
            if date_col_name:
                break
        
        # Falls keine explizite Datumsspalte, prüfe erste Spalte
        if not date_col_name:
            first_col = df.columns[0]
            # Prüfe ob erste Spalte Datum enthält
            if any(keyword in first_col.lower() for keyword in ['date', 'zeit', 'time', 'datum']):
                date_col_name = first_col
        
        if date_col_name:
            try:
                # Spezielle Behandlung für FIS
                if source_type == "fis":
                    # FIS verwendet deutsches Format ohne Sekunden oder ISO-Format
                    # Prüfe erste Zeile für Format-Erkennung
                    sample_val = str(df[date_col_name].iloc[0]) if len(df) > 0 else ""
                    
                    if '.' in sample_val and ':' in sample_val:
                        # Deutsches Format: 31.12.2024 00:00
                        df['Date'] = pd.to_datetime(df[date_col_name], 
                                                   format='%d.%m.%Y %H:%M', 
                                                   errors='coerce')
                    elif '-' in sample_val and ':' in sample_val:
                        # ISO Format: 2024-01-01 01:15:00
                        df['Date'] = pd.to_datetime(df[date_col_name], 
                                                   format='%Y-%m-%d %H:%M:%S', 
                                                   errors='coerce')
                    else:
                        # Fallback: automatische Erkennung
                        df['Date'] = pd.to_datetime(df[date_col_name], 
                                                   infer_datetime_format=True,
                                                   errors='coerce',
                                                   dayfirst=True)
                    
                    # Keine Interpolation für FIS - die Daten sind korrekt
                    invalid_dates = df['Date'].isna().sum()
                    if invalid_dates > 0 and invalid_dates < len(df) * 0.01:  # Nur wenn < 1% ungültig
                        df = df.dropna(subset=['Date'])
                        print(f"  ⚠ {invalid_dates} Zeilen mit ungültigen Datumswerten entfernt")
                    date_found = True
                    
                # Spezielle Behandlung für Erentrudis
                elif source_type == "erentrudis":
                    # Versuche verschiedene Datumsformate
                    date_formats = [
                        '%d.%m.%Y %H:%M:%S',
                        '%Y-%m-%d %H:%M:%S',
                        '%d/%m/%Y %H:%M:%S',
                        '%Y/%m/%d %H:%M:%S',
                        '%d.%m.%Y %H:%M',
                        '%Y-%m-%d %H:%M',
                        '%d-%m-%Y %H:%M:%S',
                        '%m/%d/%Y %H:%M:%S'
                    ]
                    
                    for fmt in date_formats:
                        try:
                            df['Date'] = pd.to_datetime(df[date_col_name], format=fmt, errors='coerce')
                            valid_dates = df['Date'].notna().sum()
                            if valid_dates > len(df) * 0.5:  # Wenn mehr als 50% gültig
                                date_found = True
                                break
                        except:
                            continue
                    
                    # Falls kein Format passt, verwende flexible Parsing
                    if not date_found:
                        df['Date'] = pd.to_datetime(df[date_col_name], 
                                                   infer_datetime_format=True, 
                                                   errors='coerce',
                                                   dayfirst=True)
                        date_found = True
                    
                    # Entferne ungültige Dates nur bei kleinen Mengen
                    invalid_dates = df['Date'].isna().sum()
                    if invalid_dates > 0 and invalid_dates < len(df) * 0.1:
                        df = df.dropna(subset=['Date'])
                        print(f"  ⚠ {invalid_dates} Zeilen mit ungültigen Datumswerten entfernt")
                        
                else:
                    # Standard Datetime-Konvertierung für andere Quellen
                    df['Date'] = pd.to_datetime(df[date_col_name], 
                                               errors='coerce',
                                               infer_datetime_format=True,
                                               dayfirst=True)
                    date_found = True
                    
                    # Entferne Zeilen mit ungültigen Datumswerten nur wenn wenige
                    invalid_dates = df['Date'].isna().sum()
                    if invalid_dates > 0:
                        if invalid_dates < len(df) * 0.1:  # Weniger als 10% ungültig
                            df = df.dropna(subset=['Date'])
                            print(f"  ⚠ {invalid_dates} Zeilen mit ungültigen Datumswerten entfernt")
                        else:
                            # Versuche zu interpolieren nur für nicht-FIS Daten
                            print(f"  ⚠ {invalid_dates} ungültige Datumswerte - versuche Interpolation")
                            if df['Date'].notna().sum() > 2:
                                df['Date'] = df['Date'].interpolate(method='time', limit_direction='both')
                            else:
                                # Erstelle synthetische Zeitreihe
                                print(f"  ℹ Erstelle synthetische Zeitreihe")
                                df['Date'] = pd.date_range(start='2024-01-01', periods=len(df), freq='H')
                
            except Exception as e:
                print(f"  ⚠ Warnung bei Datumskonvertierung ({date_col_name}): {e}")
        
        # Falls immer noch kein Datum, erstelle Index-basiertes Datum
        if 'Date' not in df.columns or df['Date'].isna().all():
            print(f"  ℹ Keine gültige Datumsspalte gefunden, verwende Index")
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
                'DateTime': 'Date',
                'Datum + Uhrzeit': 'Date'
            }
            
            df = df.rename(columns=column_mapping)
            
            # Datum konvertieren
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                invalid_dates = df['Date'].isna().sum()
                if invalid_dates > 0 and invalid_dates < len(df) * 0.1:
                    df = df.dropna(subset=['Date'])
                    print(f"  ⚠ {invalid_dates} Zeilen mit ungültigen Datumswerten entfernt")
            
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
        """Lädt ALLE Daten aus allen Quellen"""
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
        print("\n📊 Twin2Sim Daten:")
        if self.twin2sim_path.exists():
            for file in self.twin2sim_path.glob("*.csv"):
                key = file.stem.lower().replace('t2s_', '')
                data['twin2sim'][key] = self.load_csv_flexible(file, file.stem, "twin2sim")
        
        # Erentrudisstraße - Nur die 3 spezifischen Datasets
        print("\n🏢 Erentrudisstraße Daten (optimiert für 3 Haupt-Datasets):")
        if self.erentrudis_path.exists():
            monitoring_path = self.erentrudis_path / "Monitoring"
            if monitoring_path.exists():
                # Dataset 1: Gesamtdaten 2024 (23 Parameter)
                relevant1_2024 = monitoring_path / "2024" / "Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv"
                if relevant1_2024.exists():
                    data['erentrudis']['gesamtdaten_2024'] = self.load_csv_flexible(
                        relevant1_2024, 
                        "Gesamtdaten 2024 (Relevant-1_2024)", 
                        "erentrudis"
                    )
                
                # Dataset 2: Juli 2024 Detaildaten (44 Parameter)
                all_july_2024 = monitoring_path / "2024" / "All_24-07_export_2011_2024-07-01-00-00_2024-07-31-23-59.csv"
                if all_july_2024.exists():
                    data['erentrudis']['detail_juli_2024'] = self.load_csv_flexible(
                        all_july_2024, 
                        "Juli 2024 Detaildaten (All_24-07)", 
                        "erentrudis"
                    )
                
                # Dataset 3: Langzeit 2023-2025 (täglich)
                export_ers = monitoring_path / "export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv"
                if export_ers.exists():
                    data['erentrudis']['langzeit_2023_2025'] = self.load_csv_flexible(
                        export_ers, 
                        "Langzeit 2023-2025 (EXPORTERS)", 
                        "erentrudis"
                    )
        
        # FIS Inhauser - Nur 2 spezifische Datasets
        print("\n🏭 FIS Inhauser Daten (optimiert für 2 Haupt-Datasets):")
        if self.fis_path.exists():
            monitoring_path = self.fis_path / "Monitoring"
            
            # Dataset 1: Gebäudemonitoring Komplett - Q1 2025
            export_q1_2025 = monitoring_path / "250101-250331" / "export_1551_2024-12-31-00-00_2025-03-31-23-55.csv"
            if export_q1_2025.exists():
                data['fis']['export_q1_2025'] = self.load_csv_flexible(
                    export_q1_2025,
                    "Gebäudemonitoring Komplett (111 Parameter)",
                    "fis"
                )
            
            # Dataset 2: Außentemperatur-Zeitreihe 2024-2025
            fis_at_csv = monitoring_path / "2024-2025-05_AT.csv"
            if fis_at_csv.exists():
                data['fis']['data_2024_2025_at'] = self.load_csv_flexible(
                    fis_at_csv,
                    "Außentemperatur-Messungen (2024-2025)",
                    "fis"
                )
        
        # KW Neukirchen
        print("\n⚡ KW Neukirchen Daten:")
        if self.kw_path.exists():
            # Erzeugungsdaten (Hauptdateien)
            for xlsx_file in self.kw_path.glob("KW*.XLSX"):
                key = xlsx_file.stem.replace('_ERZEUGUNG', '')
                data['kw'][key] = self.load_excel_flexible(xlsx_file, key)
            
            # Jahresordner für Übergabedaten
            for year_dir in self.kw_path.iterdir():
                if year_dir.is_dir() and year_dir.name.isdigit():
                    for xlsx_file in year_dir.glob("*.XLSX"):
                        key = f"{year_dir.name}_{xlsx_file.stem}"[:30]
                        data['kw'][key] = self.load_excel_flexible(xlsx_file, key)
        
        # Zusammenfassung
        print("\n" + "="*60)
        print("Lade-Zusammenfassung:")
        print("="*60)
        for source, datasets in data.items():
            valid_count = len([d for d in datasets.values() if not d.empty])
            print(f"  {source}: {valid_count} Datasets geladen")
        
        return data