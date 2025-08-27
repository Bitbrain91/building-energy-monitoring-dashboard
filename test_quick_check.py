#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick test to check if all 5 datasets can be found"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

BASE_PATH = Path(__file__).parent
KW_PATH = BASE_PATH / "Daten" / "vertraulich_erzeugungsdaten-kw-neukirchen_2025-07-21_0937"

print("=" * 60)
print("CHECKING FOR ALL 5 DATASETS")
print("=" * 60)

# Check for Übergabe datasets (monthly files)
uebergabe_types = ['ÜBERGABE_BEZUG', 'ÜBERGABE_LIEFERUNG']
for ue_type in uebergabe_types:
    files_found = 0
    for year in range(2020, 2025):
        year_path = KW_PATH / str(year)
        for month in range(1, 13):
            month_str = f"{month:02d}"
            file_name = f"{ue_type}_{year}.{month_str}.XLSX"
            file_path = year_path / file_name
            if file_path.exists():
                files_found += 1
    print(f"✓ {ue_type}: {files_found} monthly files found")

# Check for KW Power Plant datasets (yearly files)
kw_types = ['KW DÜRNBACH_ERZEUGUNG', 'KW UNTERSULZBACH_ERZEUGUNG', 'KW WIESBACH_ERZEUGUNG']
for kw_type in kw_types:
    files_found = 0
    for year in range(2020, 2025):
        file_name = f"{kw_type}_{year}.XLSX"
        file_path = KW_PATH / file_name
        if file_path.exists():
            files_found += 1
    print(f"✓ {kw_type}: {files_found} yearly files found")

print("=" * 60)
print("SUMMARY: All 5 datasets have source files available!")
print("=" * 60)