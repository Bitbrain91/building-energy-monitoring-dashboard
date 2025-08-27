#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script zum Prüfen ob Übergabe Datensätze geladen werden"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Stelle sicher, dass src im Path ist
src_path = Path(__file__).parent / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Teste das Laden der Übergabe Datensätze
from load_kw_aggregated import aggregate_all_kw_data

BASE_PATH = Path(__file__).parent

print("=" * 60)
print("TESTE ÜBERGABE DATENSÄTZE LADEN")
print("=" * 60)

# Lade alle KW Datensätze
kw_data = aggregate_all_kw_data(BASE_PATH)

print("\n" + "=" * 60)
print("ERGEBNISSE:")
print("=" * 60)

# Zeige welche Datensätze erfolgreich geladen wurden
for key, df in kw_data.items():
    if not df.empty:
        print(f"✓ {key}: {len(df):,} Zeilen geladen")
        if 'Date' in df.columns:
            jahre = df['Date'].dt.year.unique()
            print(f"  → Jahre: {sorted(jahre)}")
    else:
        print(f"✗ {key}: LEER")

# Prüfe explizit die Übergabe Datensätze
print("\n" + "=" * 60)
print("KRITISCHE PRÜFUNG:")
print("=" * 60)

expected_datasets = [
    'uebergabe_bezug_gesamt',
    'uebergabe_lieferung_gesamt', 
    'kw_duernbach_gesamt',
    'kw_untersulzbach_gesamt',
    'kw_wiesbach_gesamt'
]

for dataset in expected_datasets:
    if dataset in kw_data and not kw_data[dataset].empty:
        print(f"✓ {dataset}: VORHANDEN")
    else:
        print(f"✗ {dataset}: FEHLT")

print("\n" + "=" * 60)
print(f"ZUSAMMENFASSUNG: {len(kw_data)} von 5 Datensätzen geladen")
print("=" * 60)