"""
Analysiert die Datumsspalten-Probleme bei FIS-Daten
"""
import pandas as pd
from pathlib import Path

base_path = Path("..")
monitoring_path = base_path / "Daten" / "Monitoringdaten" / "FIS_Inhauser" / "Monitoring"

print("="*60)
print("FIS Datumsspalten-Analyse")
print("="*60)

# Dataset 1: Gebäudemonitoring
print("\n1. GEBÄUDEMONITORING (export_1551):")
print("-"*40)
export_file = monitoring_path / "250101-250331" / "export_1551_2024-12-31-00-00_2025-03-31-23-55.csv"

if export_file.exists():
    # Teste verschiedene Encodings und Separatoren
    for sep in [',', ';', '\t']:
        try:
            df = pd.read_csv(export_file, sep=sep, encoding='utf-8-sig', nrows=5)
            print(f"\nSeparator '{sep}' funktioniert:")
            print(f"  Spalten: {df.columns.tolist()[:5]}...")
            print(f"  Erste Zeile:")
            for col in df.columns[:3]:
                print(f"    {col}: {df[col].iloc[0] if len(df) > 0 else 'N/A'}")
            
            # Vollständiges Laden
            df_full = pd.read_csv(export_file, sep=sep, encoding='utf-8-sig')
            
            # Suche Datumsspalte
            date_col = None
            for col in df_full.columns:
                if 'datum' in col.lower() or 'date' in col.lower() or 'zeit' in col.lower():
                    date_col = col
                    break
            
            if date_col:
                print(f"\n  Datumsspalte gefunden: '{date_col}'")
                print(f"  Beispielwerte:")
                for i in [0, 1, 100, 1000, 10000, -1]:
                    if 0 <= i < len(df_full) or i == -1:
                        val = df_full[date_col].iloc[i]
                        print(f"    Zeile {i}: {val} (Typ: {type(val).__name__})")
                
                # Versuche Datumskonvertierung
                print(f"\n  Teste Datumskonvertierung:")
                
                # Test 1: Direkte Konvertierung
                try:
                    dates = pd.to_datetime(df_full[date_col], errors='coerce')
                    valid = dates.notna().sum()
                    print(f"    pd.to_datetime (default): {valid}/{len(df_full)} gültig")
                    if valid > 0:
                        print(f"      Bereich: {dates.min()} bis {dates.max()}")
                except Exception as e:
                    print(f"    pd.to_datetime failed: {e}")
                
                # Test 2: Deutsches Format
                try:
                    dates = pd.to_datetime(df_full[date_col], format='%d.%m.%Y %H:%M:%S', errors='coerce')
                    valid = dates.notna().sum()
                    print(f"    Format '%d.%m.%Y %H:%M:%S': {valid}/{len(df_full)} gültig")
                    if valid > 0:
                        print(f"      Bereich: {dates.min()} bis {dates.max()}")
                except:
                    pass
                
                # Test 3: Ohne Sekunden
                try:
                    dates = pd.to_datetime(df_full[date_col], format='%d.%m.%Y %H:%M', errors='coerce')
                    valid = dates.notna().sum()
                    print(f"    Format '%d.%m.%Y %H:%M': {valid}/{len(df_full)} gültig")
                    if valid > 0:
                        print(f"      Bereich: {dates.min()} bis {dates.max()}")
                except:
                    pass
            
            break
        except Exception as e:
            print(f"Separator '{sep}' failed: {e}")

# Dataset 2: Außentemperatur
print("\n\n2. AUSSENTEMPERATUR (2024-2025-05_AT.csv):")
print("-"*40)
at_file = monitoring_path / "2024-2025-05_AT.csv"

if at_file.exists():
    df_at = pd.read_csv(at_file, encoding='utf-8')
    print(f"Datei geladen: {len(df_at)} Zeilen")
    print(f"Spalten: {df_at.columns.tolist()}")
    
    # Prüfe Datumsspalte
    date_col = None
    for col in df_at.columns:
        if 'datum' in col.lower() or 'date' in col.lower() or 'zeit' in col.lower():
            date_col = col
            break
    
    if date_col:
        print(f"\nDatumsspalte: '{date_col}'")
        print("Beispielwerte:")
        for i in [0, 1, 100, 1000, 10000, 30000, 50000, -1]:
            if 0 <= i < len(df_at) or i == -1:
                val = df_at[date_col].iloc[i]
                print(f"  Zeile {i:5}: {val}")
        
        # Konvertiere zu Datetime
        df_at['Date'] = pd.to_datetime(df_at[date_col], errors='coerce')
        valid = df_at['Date'].notna().sum()
        print(f"\nDatumskonvertierung: {valid}/{len(df_at)} gültig")
        
        if valid > 0:
            print(f"Zeitraum: {df_at['Date'].min()} bis {df_at['Date'].max()}")
            
            # Prüfe auf Lücken
            df_at_sorted = df_at.sort_values('Date')
            print(f"\nDatenverteilung nach Jahr:")
            year_counts = df_at_sorted['Date'].dt.year.value_counts().sort_index()
            for year, count in year_counts.items():
                print(f"  {year}: {count} Einträge")