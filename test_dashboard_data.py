#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script to verify all 5 datasets are available in the dashboard"""

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

# Import dashboard code
from data_loader_optimized import OptimizedDataLoader
from load_kw_aggregated import aggregate_all_kw_data

BASE_PATH = Path(__file__).parent

print("=" * 60)
print("TESTING DASHBOARD DATA LOADING")
print("=" * 60)

# Initialize data loader
data_loader = OptimizedDataLoader(BASE_PATH)

# Test 1: Load KW data through aggregate function
print("\n[1] Testing aggregate_all_kw_data()...")
kw_data = aggregate_all_kw_data(BASE_PATH)

expected = ['uebergabe_bezug_gesamt', 'uebergabe_lieferung_gesamt', 
            'kw_duernbach_gesamt', 'kw_untersulzbach_gesamt', 'kw_wiesbach_gesamt']

print(f"\nExpected 5 datasets, got {len(kw_data)}")
for key in expected:
    if key in kw_data and not kw_data[key].empty:
        print(f"  ✓ {key}: LOADED ({len(kw_data[key]):,} rows)")
    else:
        print(f"  ✗ {key}: MISSING")

# Test 2: Load through data_loader
print("\n[2] Testing data_loader.load_dataset_optimized('kw', ...)...")
for key in expected:
    df = data_loader.load_dataset_optimized('kw', key)
    if df is not None and not df.empty:
        print(f"  ✓ {key}: LOADED ({len(df):,} rows)")
    else:
        print(f"  ✗ {key}: FAILED TO LOAD")

print("\n" + "=" * 60)
if len(kw_data) == 5:
    print("SUCCESS: All 5 datasets are available!")
else:
    print(f"PARTIAL SUCCESS: {len(kw_data)} of 5 datasets loaded")
print("=" * 60)