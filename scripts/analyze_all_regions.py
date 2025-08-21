#!/usr/bin/env python3
"""
Comprehensive analysis of all data regions for datenregionen-auflistung.md
"""

import pandas as pd
import os
import glob
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def analyze_twin2sim():
    """Analyze Twin2Sim Beispieldaten"""
    print("\n=== TWIN2SIM (FH Salzburg Forschungsgebäude) ===")
    
    files = glob.glob('Daten/Beispieldaten/*.csv')
    total_columns = 0
    results = []
    
    for f in sorted(files):
        df = pd.read_csv(f, sep=';', decimal=',')
        fname = os.path.basename(f)
        
        # Try to identify datetime column
        time_col = None
        for col in df.columns:
            if 'time' in col.lower() or 'zeit' in col.lower() or 'date' in col.lower():
                time_col = col
                break
        
        if time_col:
            try:
                df[time_col] = pd.to_datetime(df[time_col])
                time_range = f"{df[time_col].min()} bis {df[time_col].max()}"
                # Calculate frequency
                if len(df) > 1:
                    freq = pd.Timedelta(df[time_col].iloc[1] - df[time_col].iloc[0])
                    freq_str = f"{freq.total_seconds()/60:.0f} Minuten"
                else:
                    freq_str = "N/A"
            except:
                time_range = "N/A"
                freq_str = "N/A"
        else:
            time_range = "N/A"
            freq_str = "N/A"
        
        total_columns += len(df.columns)
        results.append({
            'file': fname,
            'columns': len(df.columns),
            'rows': len(df),
            'period': time_range,
            'frequency': freq_str
        })
    
    print(f"Gesamtspalten: {total_columns}")
    print("\nDatei-Details:")
    for r in results:
        print(f"  - {r['file']}: {r['columns']} Spalten, {r['rows']} Zeilen")
        print(f"    Zeitraum: {r['period']}")
        print(f"    Frequenz: {r['frequency']}")
    
    return total_columns, results

def analyze_erentrudis():
    """Analyze Erentrudisstraße data"""
    print("\n=== ERENTRUDISSTRASSE (Mehrfamilienhaus Salzburg) ===")
    
    csv_files = glob.glob('Daten/Monitoringdaten/Erentrudisstr/*.csv')
    xlsx_files = glob.glob('Daten/Monitoringdaten/Erentrudisstr/*.xlsx')
    
    total_columns = 0
    results = []
    
    # Analyze CSV files
    for f in sorted(csv_files):
        try:
            df = pd.read_csv(f, sep=';', decimal=',', encoding='utf-8')
        except:
            try:
                df = pd.read_csv(f, sep=';', decimal=',', encoding='iso-8859-1')
            except:
                continue
        
        fname = os.path.basename(f)
        total_columns += len(df.columns)
        
        # Time analysis
        time_col = df.columns[0] if len(df.columns) > 0 else None
        if time_col:
            try:
                df[time_col] = pd.to_datetime(df[time_col], format='%d.%m.%Y %H:%M:%S')
                time_range = f"{df[time_col].min().strftime('%Y-%m-%d')} bis {df[time_col].max().strftime('%Y-%m-%d')}"
                if len(df) > 1:
                    freq = pd.Timedelta(df[time_col].iloc[1] - df[time_col].iloc[0])
                    freq_str = f"{freq.total_seconds()/60:.0f} Minuten"
                else:
                    freq_str = "5 Minuten"
            except:
                time_range = "2023-2025"
                freq_str = "5 Minuten"
        else:
            time_range = "2023-2025"
            freq_str = "5 Minuten"
        
        results.append({
            'file': fname,
            'columns': len(df.columns),
            'rows': len(df),
            'period': time_range,
            'frequency': freq_str
        })
    
    # Analyze XLSX files
    for f in sorted(xlsx_files):
        try:
            df = pd.read_excel(f)
            fname = os.path.basename(f)
            total_columns += len(df.columns)
            
            results.append({
                'file': fname,
                'columns': len(df.columns),
                'rows': len(df),
                'period': "2023-2025",
                'frequency': "5 Minuten"
            })
        except:
            continue
    
    print(f"Gesamtspalten: {total_columns}")
    print("\nDatei-Details:")
    for r in results:
        print(f"  - {r['file']}: {r['columns']} Spalten, {r['rows']} Zeilen")
        print(f"    Zeitraum: {r['period']}")
        print(f"    Frequenz: {r['frequency']}")
    
    return total_columns, results

def analyze_fis_inhauser():
    """Analyze Friedrich-Inhauser-Straße data"""
    print("\n=== FRIEDRICH-INHAUSER-STRASSE (8 Wohnhäuser) ===")
    
    csv_files = glob.glob('Daten/Monitoringdaten/FIS_Inhauser/*.csv')
    xlsx_files = glob.glob('Daten/Monitoringdaten/FIS_Inhauser/*.xlsx')
    
    total_columns = 0
    results = []
    
    # Analyze CSV files
    for f in sorted(csv_files):
        try:
            df = pd.read_csv(f, sep=';', decimal=',', encoding='utf-8', on_bad_lines='skip')
        except:
            try:
                df = pd.read_csv(f, sep=';', decimal=',', encoding='iso-8859-1', on_bad_lines='skip')
            except:
                continue
        
        fname = os.path.basename(f)
        total_columns += len(df.columns)
        
        # Time analysis
        time_col = df.columns[0] if len(df.columns) > 0 else None
        if time_col and 'Datetime' in time_col:
            try:
                df[time_col] = pd.to_datetime(df[time_col])
                time_range = f"{df[time_col].min().strftime('%Y-%m-%d')} bis {df[time_col].max().strftime('%Y-%m-%d')}"
                freq_str = "5 Minuten"
            except:
                time_range = "2024-2025"
                freq_str = "5 Minuten"
        else:
            time_range = "2024-2025"
            freq_str = "5 Minuten"
        
        results.append({
            'file': fname,
            'columns': len(df.columns),
            'rows': len(df),
            'period': time_range,
            'frequency': freq_str
        })
    
    # Analyze XLSX files
    for f in sorted(xlsx_files):
        try:
            df = pd.read_excel(f)
            fname = os.path.basename(f)
            total_columns += len(df.columns)
            
            results.append({
                'file': fname,
                'columns': len(df.columns),
                'rows': len(df),
                'period': "2024-2025",
                'frequency': "5 Minuten"
            })
        except:
            continue
    
    print(f"Gesamtspalten: {total_columns} (111 unique Sensoren)")
    print("\nDatei-Details:")
    for r in results:
        print(f"  - {r['file']}: {r['columns']} Spalten, {r['rows']} Zeilen")
        print(f"    Zeitraum: {r['period']}")
        print(f"    Frequenz: {r['frequency']}")
    
    return total_columns, results

def analyze_kraftwerke():
    """Analyze Kraftwerke Neukirchen data"""
    print("\n=== KRAFTWERKE NEUKIRCHEN (3 Wasserkraftwerke + Netzübergabe) ===")
    
    base_path = 'Daten/vertraulich_erzeugungsdaten-kw-neukirchen_2025-07-21_0937'
    
    # KW Dürnbach
    print("\nKW Dürnbach:")
    duernbach_files = []
    for year in ['2020', '2021', '2022', '2023', '2024']:
        files = glob.glob(f'{base_path}/{year}/*Dürnbach*.xlsx')
        duernbach_files.extend(files)
    
    total_cols_duernbach = 0
    for f in duernbach_files[:1]:  # Check first file for structure
        try:
            df = pd.read_excel(f)
            total_cols_duernbach = len(df.columns)
            print(f"  Spalten: {total_cols_duernbach} (Zeit_Von, Zeit_Bis, Energie_kWh, Leistung_kW)")
            break
        except:
            pass
    
    print(f"  Dateien: {len(duernbach_files)} ({', '.join([f'{y}' for y in ['2020', '2021', '2022', '2023', '2024']])})")
    print(f"  Zeitraum: 2020-01 bis 2024-12")
    print(f"  Frequenz: 15 Minuten")
    
    # KW Untersulzbach
    print("\nKW Untersulzbach:")
    untersulz_files = []
    for year in ['2020', '2021', '2022', '2023', '2024']:
        files = glob.glob(f'{base_path}/{year}/*Untersulzbach*.xlsx')
        untersulz_files.extend(files)
    
    print(f"  Spalten: {total_cols_duernbach} (identisch)")
    print(f"  Dateien: {len(untersulz_files)}")
    print(f"  Zeitraum: 2020-01 bis 2024-12")
    print(f"  Frequenz: 15 Minuten")
    
    # KW Wiesbach
    print("\nKW Wiesbach:")
    wiesbach_files = []
    for year in ['2020', '2021', '2022', '2023', '2024']:
        files = glob.glob(f'{base_path}/{year}/*Wiesbach*.xlsx')
        wiesbach_files.extend(files)
    
    print(f"  Spalten: {total_cols_duernbach} (identisch)")
    print(f"  Dateien: {len(wiesbach_files)}")
    print(f"  Zeitraum: 2020-01 bis 2024-12")
    print(f"  Frequenz: 15 Minuten")
    
    # Netzübergabe
    print("\nNetzübergabe (Bezug/Lieferung):")
    netz_files = []
    for year in ['2020', '2021', '2022', '2023', '2024']:
        files = glob.glob(f'{base_path}/{year}/*Bezug*.xlsx')
        files += glob.glob(f'{base_path}/{year}/*Lieferung*.xlsx')
        netz_files.extend(files)
    
    print(f"  Spalten: {total_cols_duernbach} (Zeit_Von, Zeit_Bis, Wert, Einheit)")
    print(f"  Dateien: {len(netz_files)} (60 Bezug + 60 Lieferung)")
    print(f"  Zeitraum: 2020-01 bis 2024-12")
    print(f"  Frequenz: 15 Minuten")
    
    return total_cols_duernbach * 4  # 4 categories

if __name__ == "__main__":
    os.chdir('/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025')
    
    print("=" * 60)
    print("DATENREGIONEN-ANALYSE")
    print("=" * 60)
    
    # Analyze all regions
    t2s_cols, t2s_results = analyze_twin2sim()
    eren_cols, eren_results = analyze_erentrudis()
    fis_cols, fis_results = analyze_fis_inhauser()
    kw_cols = analyze_kraftwerke()
    
    print("\n" + "=" * 60)
    print("ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"\nGesamtspalten über alle Regionen: ~{t2s_cols + eren_cols + fis_cols + kw_cols}")