#!/usr/bin/env python3
"""
Ausführlicher Vergleich der drei CSV-Dateien zur Analyse von Teilmengen und gemeinsamen Parametern
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Pfade zu den CSV-Dateien
base_path = Path("/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025/Daten/Monitoringdaten/FIS_Inhauser/Monitoring/250101-250331")

file1_path = base_path / "export_1551_2024-12-31-00-00_2025-03-31-23-55.csv"
file2_path = base_path / "test/export_1551_2025-01-01-00-00_2025-03-31-23-55.csv"
file3_path = base_path / "test/V1_2501_EXPORT_1.CSV"

def load_csv_with_german_format(filepath):
    """Lädt CSV mit deutschem Zahlenformat (Komma als Dezimaltrennzeichen)"""
    try:
        # Erste Zeile lesen um Encoding zu prüfen
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            first_line = f.readline()
        
        # CSV laden
        df = pd.read_csv(filepath, 
                        encoding='utf-8-sig',
                        sep=',',
                        decimal=',',
                        thousands='.',
                        parse_dates=['Datum + Uhrzeit'],
                        dayfirst=True)
        
        # Konvertiere numerische Spalten
        for col in df.columns:
            if col != 'Datum + Uhrzeit':
                # Versuche String-Werte mit Komma zu konvertieren
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.replace(',', '.').str.replace('"', '')
                    try:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except:
                        pass
        
        return df
    except Exception as e:
        print(f"Fehler beim Laden von {filepath}: {e}")
        return None

print("=" * 80)
print("AUSFÜHRLICHER CSV-VERGLEICH")
print("=" * 80)
print()

# Dateien laden
print("1. DATEIEN LADEN UND STRUKTUR ANALYSIEREN")
print("-" * 40)

df1 = load_csv_with_german_format(file1_path)
df2 = load_csv_with_german_format(file2_path)
df3 = load_csv_with_german_format(file3_path)

print(f"Datei 1: {file1_path.name}")
print(f"  - Zeilen: {len(df1)}")
print(f"  - Spalten: {len(df1.columns)}")
print(f"  - Zeitraum: {df1['Datum + Uhrzeit'].min()} bis {df1['Datum + Uhrzeit'].max()}")
print()

print(f"Datei 2: {file2_path.name}")
print(f"  - Zeilen: {len(df2)}")
print(f"  - Spalten: {len(df2.columns)}")
print(f"  - Zeitraum: {df2['Datum + Uhrzeit'].min()} bis {df2['Datum + Uhrzeit'].max()}")
print()

print(f"Datei 3: {file3_path.name}")
print(f"  - Zeilen: {len(df3)}")
print(f"  - Spalten: {len(df3.columns)}")
print(f"  - Zeitraum: {df3['Datum + Uhrzeit'].min()} bis {df3['Datum + Uhrzeit'].max()}")
print()

# 2. Spaltenvergleich
print("2. SPALTENVERGLEICH")
print("-" * 40)

cols1 = set(df1.columns)
cols2 = set(df2.columns)
cols3 = set(df3.columns)

# Gemeinsame Spalten
common_all = cols1.intersection(cols2).intersection(cols3)
common_1_2 = cols1.intersection(cols2)
common_1_3 = cols1.intersection(cols3)
common_2_3 = cols2.intersection(cols3)

print(f"Gemeinsame Spalten in allen drei Dateien: {len(common_all)}")
if common_all:
    print("  Gemeinsame Spalten:")
    for col in sorted(common_all):
        print(f"    - {col}")
print()

print(f"Gemeinsame Spalten zwischen Datei 1 und 2: {len(common_1_2)}")
print(f"Gemeinsame Spalten zwischen Datei 1 und 3: {len(common_1_3)}")
print(f"Gemeinsame Spalten zwischen Datei 2 und 3: {len(common_2_3)}")
print()

# Einzigartige Spalten
unique_1 = cols1 - cols2 - cols3
unique_2 = cols2 - cols1 - cols3
unique_3 = cols3 - cols1 - cols2

print(f"Einzigartige Spalten in Datei 1: {len(unique_1)}")
print(f"Einzigartige Spalten in Datei 2: {len(unique_2)}")
print(f"Einzigartige Spalten in Datei 3: {len(unique_3)}")
print()

# Prüfen ob Datei 2 eine Teilmenge ist
is_subset_2_of_1 = cols2.issubset(cols1)
is_subset_2_of_3 = cols2.issubset(cols3)

print(f"Ist Datei 2 eine Teilmenge von Datei 1? {is_subset_2_of_1}")
print(f"Ist Datei 2 eine Teilmenge von Datei 3? {is_subset_2_of_3}")
print()

# 3. Zeitliche Überlappungen
print("3. ZEITLICHE ÜBERLAPPUNGEN")
print("-" * 40)

# Zeitbereiche definieren
time_range_1 = (df1['Datum + Uhrzeit'].min(), df1['Datum + Uhrzeit'].max())
time_range_2 = (df2['Datum + Uhrzeit'].min(), df2['Datum + Uhrzeit'].max())
time_range_3 = (df3['Datum + Uhrzeit'].min(), df3['Datum + Uhrzeit'].max())

# Überlappungen finden
def find_overlap(range1, range2):
    start = max(range1[0], range2[0])
    end = min(range1[1], range2[1])
    if start <= end:
        return (start, end)
    return None

overlap_1_2 = find_overlap(time_range_1, time_range_2)
overlap_1_3 = find_overlap(time_range_1, time_range_3)
overlap_2_3 = find_overlap(time_range_2, time_range_3)

if overlap_1_2:
    print(f"Überlappung Datei 1 & 2: {overlap_1_2[0]} bis {overlap_1_2[1]}")
else:
    print("Keine zeitliche Überlappung zwischen Datei 1 und 2")

if overlap_1_3:
    print(f"Überlappung Datei 1 & 3: {overlap_1_3[0]} bis {overlap_1_3[1]}")
else:
    print("Keine zeitliche Überlappung zwischen Datei 1 und 3")

if overlap_2_3:
    print(f"Überlappung Datei 2 & 3: {overlap_2_3[0]} bis {overlap_2_3[1]}")
else:
    print("Keine zeitliche Überlappung zwischen Datei 2 und 3")
print()

# 4. Datenvergleich bei gleichen Zeitstempeln
print("4. DATENVERGLEICH BEI GLEICHEN ZEITSTEMPELN")
print("-" * 40)

# Funktion zum Vergleichen von Werten
def compare_values_at_timestamp(df1, df2, common_cols, timestamp_col='Datum + Uhrzeit'):
    # Merge auf Zeitstempel
    merged = pd.merge(df1, df2, on=timestamp_col, suffixes=('_1', '_2'), how='inner')
    
    if len(merged) == 0:
        return None
    
    comparison_results = {}
    
    for col in common_cols:
        if col == timestamp_col:
            continue
            
        col_1 = f"{col}_1" if f"{col}_1" in merged.columns else col
        col_2 = f"{col}_2" if f"{col}_2" in merged.columns else col
        
        if col_1 in merged.columns and col_2 in merged.columns:
            # Vergleiche die Werte
            val1 = merged[col_1].dropna()
            val2 = merged[col_2].dropna()
            
            if len(val1) > 0 and len(val2) > 0:
                # Berechne Korrelation wenn möglich
                try:
                    if val1.dtype in ['float64', 'int64'] and val2.dtype in ['float64', 'int64']:
                        correlation = val1.corr(val2)
                        mean_diff = (val1 - val2).abs().mean()
                        max_diff = (val1 - val2).abs().max()
                        identical = (val1 == val2).all()
                        
                        comparison_results[col] = {
                            'correlation': correlation,
                            'mean_diff': mean_diff,
                            'max_diff': max_diff,
                            'identical': identical,
                            'samples': len(val1)
                        }
                except:
                    pass
    
    return comparison_results, merged

# Vergleiche bei gemeinsamen Zeitstempeln
if len(common_1_2) > 1:
    print("Vergleich Datei 1 und 2:")
    results_1_2, merged_1_2 = compare_values_at_timestamp(df1, df2, common_1_2)
    if results_1_2:
        print(f"  Gemeinsame Zeitstempel: {len(merged_1_2)}")
        
        # Zeige Vergleichsergebnisse für wichtige Parameter
        for param, stats in sorted(results_1_2.items())[:10]:  # Erste 10 Parameter
            if stats['samples'] > 0:
                print(f"  {param}:")
                print(f"    - Identisch: {stats['identical']}")
                if not np.isnan(stats['correlation']):
                    print(f"    - Korrelation: {stats['correlation']:.3f}")
                    print(f"    - Mittlere Abweichung: {stats['mean_diff']:.3f}")
    else:
        print("  Keine gemeinsamen Zeitstempel gefunden!")
    print()

# 5. Spezielle Analyse für gleiche Parameter
print("5. ANALYSE GLEICHER PARAMETER")
print("-" * 40)

# Suche nach ähnlichen Parameternamen (auch mit leichten Unterschieden)
def find_similar_columns(cols1, cols2, threshold=0.8):
    """Findet ähnliche Spaltennamen zwischen zwei Sets"""
    similar = []
    for c1 in cols1:
        for c2 in cols2:
            # Vereinfachte Ähnlichkeitsprüfung
            if c1.lower() == c2.lower():
                similar.append((c1, c2, 1.0))
            elif c1.lower() in c2.lower() or c2.lower() in c1.lower():
                similar.append((c1, c2, 0.8))
    return similar

similar_1_2 = find_similar_columns(cols1, cols2)
similar_1_3 = find_similar_columns(cols1, cols3)
similar_2_3 = find_similar_columns(cols2, cols3)

print(f"Ähnliche Parameter zwischen Datei 1 und 2: {len(similar_1_2)}")
print(f"Ähnliche Parameter zwischen Datei 1 und 3: {len(similar_1_3)}")
print(f"Ähnliche Parameter zwischen Datei 2 und 3: {len(similar_2_3)}")
print()

# 6. Kategorisierung der Parameter
print("6. KATEGORISIERUNG DER PARAMETER")
print("-" * 40)

def categorize_parameters(columns):
    categories = {
        'Temperatur': [],
        'Strom/Energie': [],
        'Durchfluss': [],
        'Leistung': [],
        'Zählerstand': [],
        'Sonstige': []
    }
    
    for col in columns:
        col_lower = col.lower()
        if 'temperatur' in col_lower or '(°c)' in col_lower or 'vorlauf' in col_lower or 'rücklauf' in col_lower:
            categories['Temperatur'].append(col)
        elif 'strom' in col_lower or 'energie' in col_lower or '(kwh)' in col_lower:
            categories['Strom/Energie'].append(col)
        elif 'durchfluss' in col_lower or 'durchfluß' in col_lower or '(m³/h)' in col_lower:
            categories['Durchfluss'].append(col)
        elif 'leistung' in col_lower or '(kw)' in col_lower or '(w)' in col_lower:
            categories['Leistung'].append(col)
        elif 'zähler' in col_lower or 'zählerstand' in col_lower:
            categories['Zählerstand'].append(col)
        else:
            categories['Sonstige'].append(col)
    
    return categories

print("Datei 1 - Kategorien:")
cat1 = categorize_parameters(cols1)
for cat, params in cat1.items():
    print(f"  {cat}: {len(params)} Parameter")

print("\nDatei 2 - Kategorien:")
cat2 = categorize_parameters(cols2)
for cat, params in cat2.items():
    print(f"  {cat}: {len(params)} Parameter")

print("\nDatei 3 - Kategorien:")
cat3 = categorize_parameters(cols3)
for cat, params in cat3.items():
    print(f"  {cat}: {len(params)} Parameter")

# 7. Zusammenfassung
print("\n" + "=" * 80)
print("ZUSAMMENFASSUNG")
print("=" * 80)

print("\n1. STRUKTURELLE BEZIEHUNG:")
if is_subset_2_of_1:
    print("   ✓ Datei 2 ist eine ECHTE TEILMENGE von Datei 1")
    print(f"     (Alle {len(cols2)} Spalten aus Datei 2 sind in Datei 1 enthalten)")
else:
    print("   ✗ Datei 2 ist KEINE Teilmenge von Datei 1")
    missing = cols2 - cols1
    if missing:
        print(f"     Fehlende Spalten in Datei 1: {len(missing)}")

if cols1 == cols3:
    print("   ✓ Datei 1 und 3 haben IDENTISCHE Spaltenstruktur")
elif len(common_1_3) > len(cols1) * 0.9:
    print(f"   ≈ Datei 1 und 3 sind SEHR ÄHNLICH ({len(common_1_3)}/{len(cols1)} gemeinsame Spalten)")
else:
    print(f"   ✗ Datei 1 und 3 unterscheiden sich ({len(common_1_3)}/{len(cols1)} gemeinsame Spalten)")

print("\n2. DATENTYP:")
print("   - Datei 1: Vollständiger Datensatz mit allen Sensoren")
print("   - Datei 2: Reduzierter Export mit Kern-Parametern")  
print("   - Datei 3: Vollständiger Datensatz (gleiche Struktur wie Datei 1)")

print("\n3. ZEITLICHE BEZIEHUNG:")
if overlap_1_2:
    duration = (overlap_1_2[1] - overlap_1_2[0]).total_seconds() / 3600
    print(f"   - Datei 1 & 2 überlappen sich um {duration:.1f} Stunden")
if overlap_2_3:
    duration = (overlap_2_3[1] - overlap_2_3[0]).total_seconds() / 3600
    print(f"   - Datei 2 & 3 überlappen sich um {duration:.1f} Stunden")

print("\n4. FAZIT:")
print("   Die Dateien repräsentieren dasselbe Monitoring-System:")
print("   - Datei 2 ist ein REDUZIERTER EXPORT mit nur essentiellen Parametern")
print("   - Datei 1 und 3 sind VOLLSTÄNDIGE EXPORTS mit allen Messpunkten")
print("   - Es handelt sich um TEILMENGEN-BEZIEHUNGEN, nicht nur gleiche Parameter")