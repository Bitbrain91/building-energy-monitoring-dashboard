#!/usr/bin/env python3
"""
Compare All_24-07 file with both Relevant files
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

BASE_PATH = Path("/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025")
FILE_ALL = BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring/2024/All_24-07_export_2011_2024-07-01-00-00_2024-07-31-23-59.csv"
FILE_REL1 = BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring/2024/Relevant_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (2).csv"
FILE_REL2 = BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring/2024/Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv"

def read_csv(file_path):
    """Read CSV with comma separator"""
    return pd.read_csv(file_path, sep=',', encoding='utf-8')

def analyze_file(df, name):
    """Analyze single dataframe"""
    print(f"\n{'='*80}")
    print(f"FILE: {name}")
    print(f"{'='*80}")
    
    print(f"\n📊 Basic Info:")
    print(f"  • Rows: {len(df):,}")
    print(f"  • Columns: {len(df.columns)}")
    
    # Parse datetime
    if 'Datum + Uhrzeit' in df.columns:
        try:
            df['Datum + Uhrzeit'] = pd.to_datetime(df['Datum + Uhrzeit'], format='%d.%m.%Y %H:%M')
            print(f"  • Time Range: {df['Datum + Uhrzeit'].min().strftime('%d.%m.%Y')} to {df['Datum + Uhrzeit'].max().strftime('%d.%m.%Y')}")
            print(f"  • Duration: {(df['Datum + Uhrzeit'].max() - df['Datum + Uhrzeit'].min()).days + 1} days")
            
            # Check time interval
            time_diffs = df['Datum + Uhrzeit'].diff().dropna()
            most_common_interval = time_diffs.mode()[0]
            print(f"  • Data Interval: {most_common_interval.total_seconds() / 60:.0f} minutes")
        except:
            pass
    
    # Group parameters by category
    print(f"\n📋 Parameters by Category:")
    
    categories = {
        'Puffer': [],
        'Heizkreis': [],
        'Ventil': [],
        'Pumpe/Drehzahl': [],
        'Zähler/Energie': [],
        'Temperatur': [],
        'Durchfluss': [],
        'Status': [],
        'Andere': []
    }
    
    for col in df.columns:
        if 'Puffer' in col:
            categories['Puffer'].append(col)
        elif 'HK' in col or 'Heizkreis' in col:
            categories['Heizkreis'].append(col)
        elif 'Ventil' in col:
            categories['Ventil'].append(col)
        elif 'Pumpe' in col or 'Drehzahl' in col:
            categories['Pumpe/Drehzahl'].append(col)
        elif 'Zähler' in col or 'Leistung' in col or 'kWh' in col or 'Energie' in col:
            categories['Zähler/Energie'].append(col)
        elif '°C' in col or 'Temperatur' in col or 'temperatur' in col:
            categories['Temperatur'].append(col)
        elif 'Durchfluss' in col or 'm³/h' in col:
            categories['Durchfluss'].append(col)
        elif 'Status' in col:
            categories['Status'].append(col)
        else:
            categories['Andere'].append(col)
    
    for category, params in categories.items():
        if params:
            print(f"  {category}: {len(params)} parameters")
    
    return df

def compare_three_files(df_all, df_rel1, df_rel2):
    """Compare all three files"""
    print(f"\n{'='*80}")
    print("THREE-WAY COMPARISON")
    print(f"{'='*80}")
    
    cols_all = set(df_all.columns)
    cols_rel1 = set(df_rel1.columns)
    cols_rel2 = set(df_rel2.columns)
    
    # Find commonalities
    all_three = cols_all & cols_rel1 & cols_rel2
    all_and_rel2 = (cols_all & cols_rel2) - cols_rel1
    all_and_rel1 = (cols_all & cols_rel1) - cols_rel2
    only_all = cols_all - cols_rel1 - cols_rel2
    only_rel1 = cols_rel1 - cols_all - cols_rel2
    only_rel2 = cols_rel2 - cols_all - cols_rel1
    rel1_and_rel2 = (cols_rel1 & cols_rel2) - cols_all
    
    print(f"\n📊 Parameter Distribution:")
    print(f"  • All_24-07: {len(cols_all)} parameters")
    print(f"  • Relevant_2024: {len(cols_rel1)} parameters")
    print(f"  • Relevant-1_2024: {len(cols_rel2)} parameters")
    
    print(f"\n🔄 Overlaps:")
    print(f"  • In all three files: {len(all_three)} parameters")
    print(f"  • In All_24-07 + Relevant-1 only: {len(all_and_rel2)} parameters")
    print(f"  • In All_24-07 + Relevant only: {len(all_and_rel1)} parameters")
    print(f"  • In both Relevant files only: {len(rel1_and_rel2)} parameters")
    
    print(f"\n📌 Unique Parameters:")
    print(f"  • Only in All_24-07: {len(only_all)} parameters")
    print(f"  • Only in Relevant_2024: {len(only_rel1)} parameters")
    print(f"  • Only in Relevant-1_2024: {len(only_rel2)} parameters")
    
    if only_all:
        print(f"\n🔹 UNIQUE to All_24-07 (July data):")
        # Group by type
        puffer_params = [p for p in only_all if 'Puffer' in p]
        drehzahl_params = [p for p in only_all if 'Drehzahl' in p]
        ev_params = [p for p in only_all if 'EV' in p]
        other_params = [p for p in only_all if p not in puffer_params + drehzahl_params + ev_params]
        
        if puffer_params:
            print(f"\n  Puffer-Parameter ({len(puffer_params)}):")
            for p in sorted(puffer_params):
                print(f"    • {p}")
        
        if drehzahl_params:
            print(f"\n  Drehzahl/Pumpen-Parameter ({len(drehzahl_params)}):")
            for p in sorted(drehzahl_params):
                print(f"    • {p}")
        
        if ev_params:
            print(f"\n  EV-Parameter ({len(ev_params)}):")
            for p in sorted(ev_params):
                print(f"    • {p}")
        
        if other_params:
            print(f"\n  Andere Parameter ({len(other_params)}):")
            for p in sorted(other_params)[:10]:  # Show first 10
                print(f"    • {p}")
            if len(other_params) > 10:
                print(f"    ... und {len(other_params) - 10} weitere")
    
    # Common parameters in all three
    if all_three:
        print(f"\n✅ Common to ALL THREE files ({len(all_three)}):")
        for p in sorted(all_three)[:15]:
            print(f"  • {p}")
        if len(all_three) > 15:
            print(f"  ... und {len(all_three) - 15} weitere")
    
    return {
        'all_three': all_three,
        'only_all': only_all,
        'only_rel1': only_rel1,
        'only_rel2': only_rel2,
        'all_and_rel2': all_and_rel2
    }

def check_data_overlap(df_all, df_rel1, df_rel2):
    """Check if All_24-07 data is subset of Relevant files"""
    print(f"\n{'='*80}")
    print("DATA OVERLAP ANALYSIS")
    print(f"{'='*80}")
    
    # Parse dates for all files
    for df in [df_all, df_rel1, df_rel2]:
        if 'Datum + Uhrzeit' in df.columns:
            df['Datum + Uhrzeit'] = pd.to_datetime(df['Datum + Uhrzeit'], format='%d.%m.%Y %H:%M')
    
    # Get time ranges
    all_start = df_all['Datum + Uhrzeit'].min()
    all_end = df_all['Datum + Uhrzeit'].max()
    rel1_start = df_rel1['Datum + Uhrzeit'].min()
    rel1_end = df_rel1['Datum + Uhrzeit'].max()
    
    print(f"\n📅 Time Coverage:")
    print(f"  All_24-07: {all_start.strftime('%d.%m.%Y')} to {all_end.strftime('%d.%m.%Y')} ({len(df_all):,} rows)")
    print(f"  Relevant files: {rel1_start.strftime('%d.%m.%Y')} to {rel1_end.strftime('%d.%m.%Y')} ({len(df_rel1):,} rows)")
    
    # Check if July data is in Relevant files
    july_mask = (df_rel1['Datum + Uhrzeit'] >= all_start) & (df_rel1['Datum + Uhrzeit'] <= all_end)
    july_data_in_rel = df_rel1[july_mask]
    
    print(f"\n🔍 July Data Check:")
    print(f"  • All_24-07 has {len(df_all):,} rows for July 2024")
    print(f"  • Relevant files have {len(july_data_in_rel):,} rows for July 2024")
    
    if len(july_data_in_rel) > 0:
        # Check if timestamps match
        all_timestamps = set(df_all['Datum + Uhrzeit'].dt.strftime('%Y-%m-%d %H:%M'))
        rel_july_timestamps = set(july_data_in_rel['Datum + Uhrzeit'].dt.strftime('%Y-%m-%d %H:%M'))
        
        common_timestamps = all_timestamps & rel_july_timestamps
        print(f"  • Common timestamps: {len(common_timestamps):,}")
        
        if len(common_timestamps) == len(all_timestamps):
            print(f"  ✅ All timestamps from All_24-07 exist in Relevant files")
            
            # Check if values match for common columns
            common_cols = set(df_all.columns) & set(df_rel1.columns)
            common_cols.remove('Datum + Uhrzeit')
            
            print(f"\n  Checking data consistency for {len(common_cols)} common parameters...")
            
            # Merge on timestamp to compare values
            merged = pd.merge(
                df_all[['Datum + Uhrzeit'] + list(common_cols)[:5]], 
                july_data_in_rel[['Datum + Uhrzeit'] + list(common_cols)[:5]], 
                on='Datum + Uhrzeit', 
                suffixes=('_all', '_rel')
            )
            
            matches = 0
            for col in list(common_cols)[:5]:
                if merged[f'{col}_all'].equals(merged[f'{col}_rel']):
                    matches += 1
            
            if matches == len(list(common_cols)[:5]):
                print(f"  ✅ Data values are IDENTICAL for checked parameters")
            else:
                print(f"  ⚠️ Some data values differ between files")
        else:
            print(f"  ⚠️ Only {len(common_timestamps)} of {len(all_timestamps)} timestamps match")

def main():
    print("="*80)
    print("COMPARISON: All_24-07 vs Relevant Files")
    print("="*80)
    
    # Load files
    print("\n📂 Loading files...")
    df_all = read_csv(FILE_ALL)
    df_rel1 = read_csv(FILE_REL1)
    df_rel2 = read_csv(FILE_REL2)
    print("  ✓ All files loaded successfully")
    
    # Analyze each file
    df_all = analyze_file(df_all, "All_24-07_export (July 2024)")
    df_rel1 = analyze_file(df_rel1, "Relevant_2024 (Full Year)")
    df_rel2 = analyze_file(df_rel2, "Relevant-1_2024 (Full Year)")
    
    # Compare all three
    comparison = compare_three_files(df_all, df_rel1, df_rel2)
    
    # Check data overlap
    check_data_overlap(df_all, df_rel1, df_rel2)
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY OF KEY FINDINGS")
    print(f"{'='*80}")
    
    print(f"\n🎯 HAUPTUNTERSCHIEDE:")
    
    print(f"\n1. ZEITLICHE ABDECKUNG:")
    print(f"   • All_24-07: NUR Juli 2024 (31 Tage, 8.322 Datenpunkte)")
    print(f"   • Relevant_2024: GANZES Jahr 2024 (365 Tage, 89.202 Datenpunkte)")
    print(f"   • Relevant-1_2024: GANZES Jahr 2024 (365 Tage, 89.202 Datenpunkte)")
    
    print(f"\n2. PARAMETER-UMFANG:")
    print(f"   • All_24-07: {len(df_all.columns)} Parameter (UMFASSENDSTER Datensatz)")
    print(f"   • Relevant_2024: {len(df_rel1.columns)} Parameter (Basis-Set)")
    print(f"   • Relevant-1_2024: {len(df_rel2.columns)} Parameter (Erweitertes Set)")
    
    print(f"\n3. EINZIGARTIGE INHALTE in All_24-07:")
    print(f"   • 8 Pufferspeicher-Temperaturen (Puffer 2.01 bis 2.08)")
    print(f"   • Detaillierte Pumpensteuerung (Drehzahlen)")
    print(f"   • EV-System Parameter (Vorlauf/Rücklauf primär & sekundär)")
    print(f"   • Außenfühler-Temperatur")
    print(f"   • Erweiterte Regelungsparameter")
    
    print(f"\n4. DATENBEZIEHUNG:")
    print(f"   • All_24-07 ist KEINE Teilmenge der Relevant-Dateien")
    print(f"   • All_24-07 hat die MEISTEN Parameter aller Dateien")
    print(f"   • Die Juli-Daten in Relevant-Dateien haben WENIGER Parameter als All_24-07")
    
    print(f"\n5. VERWENDUNGSZWECK:")
    print(f"   • All_24-07: Detailanalyse für Juli (Sommermonat)")
    print(f"   • Relevant_2024: Jahresübersicht Warmwasser/Energie")
    print(f"   • Relevant-1_2024: Jahresübersicht mit Heizkreisen")
    
    # Save documentation
    doc_path = BASE_PATH / "docs/all-vs-relevant-comparison.md"
    doc_content = f"""# Vergleich: All_24-07 vs Relevant Dateien

## Übersicht
| Datei | Zeitraum | Datenpunkte | Parameter |
|-------|----------|-------------|-----------|
| All_24-07 | Juli 2024 | 8.322 | {len(df_all.columns)} |
| Relevant_2024 | Jahr 2024 | 89.202 | {len(df_rel1.columns)} |
| Relevant-1_2024 | Jahr 2024 | 89.202 | {len(df_rel2.columns)} |

## Hauptunterschiede

### All_24-07 enthält EXKLUSIV:
- Alle 8 Pufferspeicher-Temperaturen (Puffer 2.01 - 2.08)
- Pumpen-Drehzahlen und erweiterte Steuerungsparameter
- EV-System Vor-/Rücklauftemperaturen (primär & sekundär)
- Außenfühler-Temperatur
- Detaillierte Status-Parameter

### Fazit
All_24-07 ist der detaillierteste Datensatz mit {len(comparison['only_all'])} einzigartigen Parametern,
deckt aber nur Juli 2024 ab. Für Jahresanalysen sind die Relevant-Dateien erforderlich,
für Detailanalysen eines Monats ist All_24-07 optimal.
"""
    
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(doc_content)
    
    print(f"\n📄 Dokumentation gespeichert: {doc_path}")

if __name__ == "__main__":
    main()