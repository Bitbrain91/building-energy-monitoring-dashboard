#!/usr/bin/env python3
"""
Detaillierte Analyse der Monitoringdaten Erentrudisstraße
Erstellt: 2025-08-20
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Basis-Pfad für Monitoringdaten
BASE_PATH = '/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025/Daten/Monitoringdaten/Erentrudisstr/Monitoring'

def analyze_csv_detailed(filepath, max_rows=5):
    """Detaillierte Analyse einer CSV-Datei"""
    print(f"\n{'='*80}")
    print(f"DATEI: {os.path.basename(filepath)}")
    print(f"{'='*80}")
    
    try:
        # Lade Datei mit verschiedenen Separatoren
        for sep in [';', ',', '\t']:
            try:
                df = pd.read_csv(filepath, sep=sep, encoding='utf-8', nrows=5)
                if len(df.columns) > 1:
                    # Lade vollständige Datei
                    df = pd.read_csv(filepath, sep=sep, encoding='utf-8')
                    break
            except:
                try:
                    df = pd.read_csv(filepath, sep=sep, encoding='iso-8859-1', nrows=5)
                    if len(df.columns) > 1:
                        df = pd.read_csv(filepath, sep=sep, encoding='iso-8859-1')
                        break
                except:
                    continue
        
        print(f"\nGrundinformationen:")
        print(f"- Anzahl Zeilen: {len(df):,}")
        print(f"- Anzahl Spalten: {len(df.columns)}")
        print(f"- Speichergröße: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print(f"\nSpaltenübersicht:")
        for i, col in enumerate(df.columns[:15], 1):  # Erste 15 Spalten
            dtype = df[col].dtype
            non_null = df[col].notna().sum()
            null_pct = (df[col].isna().sum() / len(df) * 100)
            print(f"  {i:2d}. {col[:50]:<50} | {str(dtype):<10} | {non_null:>7,} Werte | {null_pct:>5.1f}% fehlen")
        
        if len(df.columns) > 15:
            print(f"  ... und {len(df.columns) - 15} weitere Spalten")
        
        # Zeitanalyse
        time_cols = [col for col in df.columns if any(x in col.lower() for x in ['time', 'zeit', 'date', 'datum'])]
        if time_cols:
            print(f"\nZeitliche Analyse:")
            for col in time_cols[:2]:
                try:
                    df[col] = pd.to_datetime(df[col])
                    print(f"  Spalte '{col}':")
                    print(f"    - Zeitraum: {df[col].min()} bis {df[col].max()}")
                    print(f"    - Zeitspanne: {(df[col].max() - df[col].min()).days} Tage")
                    
                    # Zeitliche Auflösung
                    if len(df) > 1:
                        time_diff = df[col].diff().dropna()
                        common_diff = time_diff.value_counts().head(3)
                        print(f"    - Häufigste Zeitabstände:")
                        for td, count in common_diff.items():
                            print(f"      • {td}: {count:,} mal ({count/len(time_diff)*100:.1f}%)")
                except:
                    pass
        
        # Numerische Analyse
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"\nNumerische Spalten ({len(numeric_cols)} insgesamt):")
            
            # Kategorisiere nach Inhalt
            temp_cols = [c for c in numeric_cols if 'temp' in c.lower()]
            flow_cols = [c for c in numeric_cols if any(x in c.lower() for x in ['flow', 'durchfluss', 'durchfluß'])]
            power_cols = [c for c in numeric_cols if any(x in c.lower() for x in ['power', 'leistung', 'kw'])]
            energy_cols = [c for c in numeric_cols if any(x in c.lower() for x in ['energy', 'energie', 'kwh'])]
            
            if temp_cols:
                print(f"  Temperatur-Messungen ({len(temp_cols)} Spalten):")
                for col in temp_cols[:3]:
                    print(f"    • {col}: {df[col].min():.1f} - {df[col].max():.1f} °C")
            
            if flow_cols:
                print(f"  Durchfluss-Messungen ({len(flow_cols)} Spalten):")
                for col in flow_cols[:3]:
                    if df[col].notna().any():
                        print(f"    • {col}: {df[col].min():.2f} - {df[col].max():.2f}")
            
            if power_cols:
                print(f"  Leistungs-Messungen ({len(power_cols)} Spalten):")
                for col in power_cols[:3]:
                    if df[col].notna().any():
                        print(f"    • {col}: {df[col].min():.2f} - {df[col].max():.2f} kW")
            
            if energy_cols:
                print(f"  Energie-Messungen ({len(energy_cols)} Spalten):")
                for col in energy_cols[:3]:
                    if df[col].notna().any():
                        print(f"    • {col}: {df[col].min():.2f} - {df[col].max():.2f} kWh")
        
        # Erste Zeilen anzeigen
        print(f"\nErste 3 Datenzeilen (erste 5 Spalten):")
        print(df.iloc[:3, :5].to_string())
        
        return df
        
    except Exception as e:
        print(f"FEHLER beim Lesen der Datei: {e}")
        return None

def analyze_excel_detailed(filepath):
    """Detaillierte Analyse einer Excel-Datei"""
    print(f"\n{'='*80}")
    print(f"EXCEL-DATEI: {os.path.basename(filepath)}")
    print(f"{'='*80}")
    
    try:
        xl_file = pd.ExcelFile(filepath)
        print(f"\nAnzahl Sheets: {len(xl_file.sheet_names)}")
        print(f"Sheet-Namen: {', '.join(xl_file.sheet_names)}")
        
        for sheet_name in xl_file.sheet_names[:3]:  # Erste 3 Sheets
            print(f"\n--- Sheet: '{sheet_name}' ---")
            try:
                df = pd.read_excel(filepath, sheet_name=sheet_name)
                if len(df) == 0:
                    print("  (Leeres Sheet)")
                    continue
                    
                print(f"  Dimensionen: {len(df)} Zeilen × {len(df.columns)} Spalten")
                
                # Spaltenanalyse
                print(f"  Erste 10 Spalten:")
                for i, col in enumerate(df.columns[:10], 1):
                    dtype = df[col].dtype
                    non_null = df[col].notna().sum()
                    print(f"    {i:2d}. {str(col)[:40]:<40} | {str(dtype):<10} | {non_null:,} Werte")
                
                # Identifiziere Inhalt
                col_str = ' '.join([str(c).lower() for c in df.columns])
                if 'temperatur' in col_str or 'temp' in col_str:
                    print("  → Enthält Temperaturdaten")
                if 'durchfluss' in col_str or 'flow' in col_str:
                    print("  → Enthält Durchflussdaten")
                if 'leistung' in col_str or 'power' in col_str:
                    print("  → Enthält Leistungsdaten")
                    
            except Exception as e:
                print(f"  Fehler beim Lesen: {e}")
                
        return xl_file
        
    except Exception as e:
        print(f"FEHLER beim Lesen der Excel-Datei: {e}")
        return None

def main():
    """Hauptfunktion für detaillierte Analyse"""
    
    print("=" * 80)
    print("DETAILLIERTE ANALYSE - MONITORINGDATEN ERENTRUDISSTRASSE")
    print("=" * 80)
    print(f"Zeitpunkt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Wichtige CSV-Dateien analysieren
    csv_files = [
        'export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv',
        'Vp.csv',
        '2024/Relevant_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (2).csv',
        '2024/Durchfluß/export_2011_2024-01-01-00-00_2024-12-31-23-59.csv'
    ]
    
    for csv_file in csv_files:
        filepath = os.path.join(BASE_PATH, csv_file)
        if os.path.exists(filepath):
            analyze_csv_detailed(filepath)
    
    # Excel-Dateien analysieren
    excel_files = [
        '2024/Monitoring_ERS_2024_V2_250506.xlsx',
        '2024/Monitoring_ERS_24-07_all.xlsx'
    ]
    
    for excel_file in excel_files:
        filepath = os.path.join(BASE_PATH, excel_file)
        if os.path.exists(filepath):
            analyze_excel_detailed(filepath)
    
    print("\n" + "=" * 80)
    print("ANALYSE ABGESCHLOSSEN")
    print("=" * 80)

if __name__ == "__main__":
    main()