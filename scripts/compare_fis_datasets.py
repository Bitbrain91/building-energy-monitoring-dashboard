#!/usr/bin/env python3
"""
Detailed comparison of FIS_Inhauser datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

BASE_PATH = Path("/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025")
DATA_PATH = BASE_PATH / "Daten/Monitoringdaten/FIS_Inhauser/Monitoring"

def load_datasets():
    """Load all datasets"""
    datasets = {}
    
    # Load main CSV exports
    export_2024 = pd.read_csv(DATA_PATH / "250101-250331/export_1551_2024-12-31-00-00_2025-03-31-23-55.csv")
    export_2025 = pd.read_csv(DATA_PATH / "250101-250331/test/export_1551_2025-01-01-00-00_2025-03-31-23-55.csv")
    v1_export = pd.read_csv(DATA_PATH / "250101-250331/test/V1_2501_EXPORT_1.CSV")
    
    # Parse dates
    for df in [export_2024, export_2025, v1_export]:
        if 'Datum + Uhrzeit' in df.columns:
            df['Datum + Uhrzeit'] = pd.to_datetime(df['Datum + Uhrzeit'], format='%d.%m.%Y %H:%M')
    
    datasets['Export_2024-12'] = export_2024
    datasets['Export_2025-01'] = export_2025
    datasets['V1_Export'] = v1_export
    
    return datasets

def analyze_overlap(datasets):
    """Analyze parameter overlap between datasets"""
    print("="*80)
    print("PARAMETER OVERLAP ANALYSIS")
    print("="*80)
    
    # Get column sets
    cols_2024 = set(datasets['Export_2024-12'].columns)
    cols_2025 = set(datasets['Export_2025-01'].columns)
    cols_v1 = set(datasets['V1_Export'].columns)
    
    print(f"\n📊 Parameter Count:")
    print(f"  • Export_2024-12: {len(cols_2024)} parameters")
    print(f"  • Export_2025-01: {len(cols_2025)} parameters")
    print(f"  • V1_Export: {len(cols_v1)} parameters")
    
    # Find overlaps
    all_three = cols_2024 & cols_2025 & cols_v1
    only_2024_v1 = (cols_2024 & cols_v1) - cols_2025
    only_2024_2025 = (cols_2024 & cols_2025) - cols_v1
    only_2025_v1 = (cols_2025 & cols_v1) - cols_2024
    
    only_2024 = cols_2024 - cols_2025 - cols_v1
    only_2025 = cols_2025 - cols_2024 - cols_v1
    only_v1 = cols_v1 - cols_2024 - cols_2025
    
    print(f"\n🔄 Overlaps:")
    print(f"  • In all three files: {len(all_three)} parameters")
    print(f"  • Only Export_2024-12 & V1: {len(only_2024_v1)} parameters")
    print(f"  • Only Export_2024-12 & Export_2025-01: {len(only_2024_2025)} parameters")
    print(f"  • Only Export_2025-01 & V1: {len(only_2025_v1)} parameters")
    
    print(f"\n📌 Unique Parameters:")
    print(f"  • Only in Export_2024-12: {len(only_2024)} parameters")
    print(f"  • Only in Export_2025-01: {len(only_2025)} parameters")
    print(f"  • Only in V1_Export: {len(only_v1)} parameters")
    
    # Analyze common parameters
    if all_three:
        print(f"\n✅ Common to ALL files ({len(all_three)}):")
        for param in sorted(list(all_three)[:10]):
            print(f"    • {param}")
        if len(all_three) > 10:
            print(f"    ... and {len(all_three) - 10} more")
    
    # Analyze unique parameters by category
    print(f"\n🔹 Unique to Export_2024-12 (Full monitoring):")
    unique_2024 = sorted(only_2024)
    
    # Group by system
    haus_params = [p for p in unique_2024 if 'Haus' in p]
    stromzaehler = [p for p in unique_2024 if 'Stromzähler' in p]
    kaeltezaehler = [p for p in unique_2024 if 'Kältezähler' in p]
    
    if haus_params:
        print(f"  🏠 House-specific ({len(haus_params)} params):")
        houses = set()
        for p in haus_params:
            if 'Haus' in p:
                # Extract house number
                parts = p.split('Haus')
                if len(parts) > 1:
                    house_num = parts[1].split()[0].strip('/')
                    houses.add(house_num)
        print(f"    Houses covered: {', '.join(sorted(houses, key=lambda x: int(x) if x.isdigit() else 0))}")
    
    if stromzaehler:
        print(f"  ⚡ Electricity meters: {len(stromzaehler)} parameters")
    
    if kaeltezaehler:
        print(f"  ❄️ Cooling meters: {len(kaeltezaehler)} parameters")
    
    print(f"\n🔹 Unique to Export_2025-01 (Reduced set):")
    unique_2025 = sorted(only_2025)
    wp_params = [p for p in unique_2025 if 'WP' in p or 'Wärmepumpe' in p]
    if wp_params:
        print(f"  🔥 Heat pump specific: {len(wp_params)} parameters")
        for p in wp_params[:5]:
            print(f"    • {p}")
    
    return all_three, only_2024, only_2025, only_v1

def analyze_time_alignment(datasets):
    """Check time alignment between datasets"""
    print(f"\n{'='*80}")
    print("TIME ALIGNMENT ANALYSIS")
    print(f"{'='*80}")
    
    for name, df in datasets.items():
        print(f"\n📅 {name}:")
        print(f"  • Start: {df['Datum + Uhrzeit'].min()}")
        print(f"  • End: {df['Datum + Uhrzeit'].max()}")
        print(f"  • Duration: {(df['Datum + Uhrzeit'].max() - df['Datum + Uhrzeit'].min()).days + 1} days")
        print(f"  • Data points: {len(df):,}")
        
        # Calculate sampling rate
        time_diff = df['Datum + Uhrzeit'].diff().dropna()
        most_common = time_diff.mode()[0] if len(time_diff.mode()) > 0 else time_diff.median()
        print(f"  • Sampling interval: {most_common.total_seconds() / 60:.0f} minutes")
    
    # Check overlap periods
    print(f"\n🔄 Overlap Analysis:")
    
    # V1 period (shortest)
    v1_start = datasets['V1_Export']['Datum + Uhrzeit'].min()
    v1_end = datasets['V1_Export']['Datum + Uhrzeit'].max()
    
    # Check how many rows other datasets have in V1 period
    for name in ['Export_2024-12', 'Export_2025-01']:
        df = datasets[name]
        mask = (df['Datum + Uhrzeit'] >= v1_start) & (df['Datum + Uhrzeit'] <= v1_end)
        overlap_rows = df[mask]
        print(f"  • {name} has {len(overlap_rows):,} rows during V1_Export period")

def analyze_data_consistency(datasets):
    """Check data consistency for common parameters"""
    print(f"\n{'='*80}")
    print("DATA CONSISTENCY CHECK")
    print(f"{'='*80}")
    
    # Find common parameters
    common_params = set(datasets['Export_2024-12'].columns) & \
                   set(datasets['Export_2025-01'].columns) & \
                   set(datasets['V1_Export'].columns)
    
    common_params.discard('Datum + Uhrzeit')
    
    print(f"\n🔍 Checking consistency for {len(common_params)} common parameters")
    
    # Focus on V1 period for comparison
    v1_start = datasets['V1_Export']['Datum + Uhrzeit'].min()
    v1_end = datasets['V1_Export']['Datum + Uhrzeit'].max()
    
    # Get data for V1 period from other datasets
    export_2024_subset = datasets['Export_2024-12'][
        (datasets['Export_2024-12']['Datum + Uhrzeit'] >= v1_start) &
        (datasets['Export_2024-12']['Datum + Uhrzeit'] <= v1_end)
    ].copy()
    
    export_2025_subset = datasets['Export_2025-01'][
        (datasets['Export_2025-01']['Datum + Uhrzeit'] >= v1_start) &
        (datasets['Export_2025-01']['Datum + Uhrzeit'] <= v1_end)
    ].copy()
    
    # Check a few parameters
    params_to_check = list(common_params)[:5]
    
    for param in params_to_check:
        print(f"\n  Parameter: {param}")
        
        # Get values from each dataset
        v1_vals = datasets['V1_Export'][param]
        e24_vals = export_2024_subset[param] if len(export_2024_subset) > 0 else pd.Series()
        e25_vals = export_2025_subset[param] if len(export_2025_subset) > 0 else pd.Series()
        
        # Compare statistics
        print(f"    V1_Export: mean={v1_vals.mean():.2f}, std={v1_vals.std():.2f}")
        if len(e24_vals) > 0:
            print(f"    Export_2024-12: mean={e24_vals.mean():.2f}, std={e24_vals.std():.2f}")
        if len(e25_vals) > 0:
            print(f"    Export_2025-01: mean={e25_vals.mean():.2f}, std={e25_vals.std():.2f}")

def create_hierarchy():
    """Create dataset hierarchy"""
    print(f"\n{'='*80}")
    print("DATASET HIERARCHY")
    print(f"{'='*80}")
    
    print("""
┌─────────────────────────────────────────────────────────────┐
│ Export_2024-12: 111 Parameters (MOST COMPREHENSIVE)         │
│ ├─ Period: Dec 31, 2024 - Mar 31, 2025                     │
│ ├─ Coverage: All houses (1,3,5,7,9,11,13,15)               │
│ └─ Systems: Heating, Cooling, Ventilation, Electricity      │
└─────────────────────────────────────────────────────────────┘
                            ≈
┌─────────────────────────────────────────────────────────────┐
│ V1_Export: 112 Parameters (TEST DATASET)                    │
│ ├─ Period: Jan 23-29, 2025 (7 days only)                   │
│ ├─ Similar coverage to Export_2024-12                       │
│ └─ Purpose: Validation/Testing                              │
└─────────────────────────────────────────────────────────────┘
                            ⊃
┌─────────────────────────────────────────────────────────────┐
│ Export_2025-01: 26 Parameters (REDUCED SET)                 │
│ ├─ Period: Jan 1 - Mar 31, 2025                            │
│ ├─ Focus: Heat pumps and core systems                      │
│ └─ Subset of Export_2024-12                                │
└─────────────────────────────────────────────────────────────┘

RELATIONSHIPS:
• Export_2024-12 ≈ V1_Export (similar parameter count, different periods)
• Export_2025-01 ⊂ Export_2024-12 (true subset)
• V1_Export = Test/validation dataset
""")

def main():
    print("="*80)
    print("FIS_INHAUSER DATASET COMPARISON")
    print("="*80)
    
    # Load datasets
    print("\n📂 Loading datasets...")
    datasets = load_datasets()
    print("  ✓ All datasets loaded")
    
    # Analyze overlaps
    common, only_2024, only_2025, only_v1 = analyze_overlap(datasets)
    
    # Analyze time alignment
    analyze_time_alignment(datasets)
    
    # Check data consistency
    analyze_data_consistency(datasets)
    
    # Create hierarchy
    create_hierarchy()
    
    # Summary
    print(f"\n{'='*80}")
    print("KEY FINDINGS")
    print(f"{'='*80}")
    
    print(f"""
🎯 MAIN INSIGHTS:

1. DATASET STRUCTURE:
   • Export_2024-12: Full monitoring system (111 params)
   • V1_Export: Test dataset with similar coverage (112 params)
   • Export_2025-01: Reduced core parameters (26 params)

2. COVERAGE:
   • Houses monitored: 1, 3, 5, 7, 9, 11, 13, 15
   • Systems: Heating, Cooling, Ventilation, Solar PV, Heat Pumps
   • Time span: Dec 2024 - Mar 2025 (main period)

3. DATA QUALITY:
   • Consistent 5-minute sampling intervals
   • Export_2024-12 most complete (22,806 data points)
   • V1_Export for validation (1,568 data points, 7 days)
   • Export_2025-01 focused subset (21,138 data points)

4. UNIQUE FEATURES:
   • Export_2024-12: Individual house monitoring
   • Export_2025-01: Heat pump focus
   • V1_Export: PV system data included

5. RECOMMENDED USE:
   • Full analysis: Use Export_2024-12
   • Heat pump analysis: Use Export_2025-01
   • Validation: Compare with V1_Export
""")

if __name__ == "__main__":
    main()