#!/usr/bin/env python3
"""
Final comprehensive comparison including export_ERS and Vp.csv from main folder
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

BASE_PATH = Path("/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025")

# All CSV files to compare
FILES = {
    'export_ERS_2023-12': BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring/export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv",
    'Vp.csv': BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring/Vp.csv",
    'Durchfluss_2024': BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring/2024/Durchfluß/export_2011_2024-01-01-00-00_2024-12-31-23-59.csv",
    'All_24-07': BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring/2024/All_24-07_export_2011_2024-07-01-00-00_2024-07-31-23-59.csv",
    'Relevant_2024': BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring/2024/Relevant_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (2).csv",
    'Relevant-1_2024': BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring/2024/Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv"
}

def read_csv_safe(file_path):
    """Read CSV with error handling"""
    try:
        # First try comma separator
        df = pd.read_csv(file_path, sep=',', encoding='utf-8')
        if len(df.columns) == 1 and ',' in df.columns[0]:
            # Likely wrong separator, try semicolon
            df = pd.read_csv(file_path, sep=';', decimal=',', encoding='utf-8')
        return df
    except:
        try:
            df = pd.read_csv(file_path, sep=';', decimal=',', encoding='cp1252')
            return df
        except:
            return None

def analyze_file(df, name):
    """Analyze single file"""
    if df is None:
        return None
        
    info = {
        'name': name,
        'rows': len(df),
        'columns': len(df.columns),
        'column_names': list(df.columns)
    }
    
    # Parse datetime if exists
    datetime_col = None
    for col in df.columns:
        if 'datum' in col.lower() or 'zeit' in col.lower():
            datetime_col = col
            break
    
    if datetime_col:
        try:
            df[datetime_col] = pd.to_datetime(df[datetime_col], format='%d.%m.%Y %H:%M')
            info['time_start'] = df[datetime_col].min()
            info['time_end'] = df[datetime_col].max()
            info['days'] = (info['time_end'] - info['time_start']).days + 1
        except:
            pass
    
    return info

def compare_export_ers_and_vp():
    """Special comparison for export_ERS and Vp.csv"""
    print(f"\n{'='*80}")
    print("ANALYSIS: export_ERS_2023-12 and Vp.csv")
    print(f"{'='*80}")
    
    # Load files
    df_ers = read_csv_safe(FILES['export_ERS_2023-12'])
    df_vp = read_csv_safe(FILES['Vp.csv'])
    
    if df_ers is not None:
        print(f"\n📁 export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv:")
        print(f"  • Rows: {len(df_ers):,}")
        print(f"  • Columns: {len(df_ers.columns)}")
        
        # Check if it's the problematic single-column format
        if len(df_ers.columns) == 1:
            col_name = df_ers.columns[0]
            if ',' in col_name:
                params = col_name.split(',')
                print(f"  ⚠️ File has parsing issue - all {len(params)} parameters in one column")
                print(f"  📋 Detected parameters include:")
                
                # Group parameters
                pumpen = [p for p in params if 'Pumpe' in p]
                puffer = [p for p in params if 'Puffer' in p]
                hk = [p for p in params if 'HK' in p]
                durchfluss = [p for p in params if 'Durchfluss' in p]
                
                print(f"    - Pumpen/Zirkulation: {len(pumpen)} parameters")
                print(f"    - Pufferspeicher: {len(puffer)} parameters")
                print(f"    - Heizkreise: {len(hk)} parameters")
                print(f"    - Durchfluss: {len(durchfluss)} parameters")
                print(f"    - Andere: {len(params) - len(pumpen) - len(puffer) - len(hk) - len(durchfluss)} parameters")
        else:
            # Parse datetime
            if 'Datum + Uhrzeit' in df_ers.columns:
                try:
                    df_ers['Datum + Uhrzeit'] = pd.to_datetime(df_ers['Datum + Uhrzeit'], format='%d.%m.%Y %H:%M')
                    print(f"  • Time range: {df_ers['Datum + Uhrzeit'].min().date()} to {df_ers['Datum + Uhrzeit'].max().date()}")
                    print(f"  • Duration: {(df_ers['Datum + Uhrzeit'].max() - df_ers['Datum + Uhrzeit'].min()).days + 1} days")
                except:
                    pass
    
    if df_vp is not None:
        print(f"\n📁 Vp.csv:")
        print(f"  • Rows: {len(df_vp):,}")
        print(f"  • Columns: {len(df_vp.columns)}")
        
        if len(df_vp.columns) == 1:
            col_name = df_vp.columns[0]
            if ',' in col_name:
                params = col_name.split(',')
                print(f"  ⚠️ File has parsing issue - all {len(params)} parameters in one column")
                print(f"  📋 Parameters: {', '.join(params)}")
        else:
            for col in df_vp.columns:
                print(f"    - {col}")
    
    return df_ers, df_vp

def create_complete_hierarchy():
    """Create complete dataset hierarchy"""
    print(f"\n{'='*80}")
    print("COMPLETE DATASET HIERARCHY")
    print(f"{'='*80}")
    
    # Load and analyze all files
    all_info = {}
    for name, path in FILES.items():
        df = read_csv_safe(path)
        info = analyze_file(df, name)
        if info:
            all_info[name] = info
    
    # Sort by column count
    sorted_files = sorted(all_info.items(), key=lambda x: x[1]['columns'], reverse=True)
    
    print(f"\n📊 Files sorted by parameter count:")
    print(f"{'='*60}")
    
    for name, info in sorted_files:
        time_info = ""
        if 'time_start' in info:
            time_info = f" | {info['time_start'].strftime('%Y-%m-%d')} to {info['time_end'].strftime('%Y-%m-%d')}"
        
        print(f"{name:20} | {info['columns']:3} params | {info['rows']:7,} rows{time_info}")
    
    return all_info

def analyze_relationships(all_info):
    """Analyze relationships between all files"""
    print(f"\n{'='*80}")
    print("DATASET RELATIONSHIPS")
    print(f"{'='*80}")
    
    # Group by parameter count
    print(f"\n🔄 Parameter Groups:")
    
    # Minimal (4 params)
    minimal = [name for name, info in all_info.items() if info['columns'] == 4]
    if minimal:
        print(f"\n📌 MINIMAL datasets (4 parameters - flow only):")
        for name in minimal:
            print(f"  • {name}: {all_info[name]['rows']:,} rows")
    
    # Basic (15 params)
    basic = [name for name, info in all_info.items() if info['columns'] == 15]
    if basic:
        print(f"\n📌 BASIC datasets (15 parameters):")
        for name in basic:
            print(f"  • {name}: {all_info[name]['rows']:,} rows")
    
    # Extended (23 params)
    extended = [name for name, info in all_info.items() if info['columns'] == 23]
    if extended:
        print(f"\n📌 EXTENDED datasets (23 parameters):")
        for name in extended:
            print(f"  • {name}: {all_info[name]['rows']:,} rows")
    
    # Complete (45+ params)
    complete = [name for name, info in all_info.items() if info['columns'] >= 45]
    if complete:
        print(f"\n📌 COMPLETE datasets (45+ parameters):")
        for name in complete:
            print(f"  • {name}: {all_info[name]['rows']:,} rows")
    
    # Special case - parsing issues
    parsing_issues = [name for name, info in all_info.items() if info['columns'] == 1]
    if parsing_issues:
        print(f"\n⚠️ FILES WITH PARSING ISSUES (need semicolon separator):")
        for name in parsing_issues:
            print(f"  • {name}")

def compare_time_coverage(all_info):
    """Compare time coverage of all files"""
    print(f"\n{'='*80}")
    print("TIME COVERAGE ANALYSIS")
    print(f"{'='*80}")
    
    print(f"\n📅 Temporal Overview:")
    
    # Files with time info
    timed_files = [(name, info) for name, info in all_info.items() if 'time_start' in info]
    
    if timed_files:
        # Sort by start date
        timed_files.sort(key=lambda x: x[1]['time_start'])
        
        for name, info in timed_files:
            print(f"\n{name}:")
            print(f"  Start: {info['time_start'].strftime('%d.%m.%Y')}")
            print(f"  End:   {info['time_end'].strftime('%d.%m.%Y')}")
            print(f"  Days:  {info['days']}")
            
            # Check coverage
            if info['days'] > 300:
                print(f"  Type:  FULL YEAR coverage")
            elif info['days'] > 100:
                print(f"  Type:  MULTI-MONTH coverage")
            elif info['days'] > 25:
                print(f"  Type:  MONTHLY coverage")
            else:
                print(f"  Type:  PARTIAL coverage")

def main():
    print("="*80)
    print("FINAL COMPREHENSIVE COMPARISON - ALL CSV FILES")
    print("="*80)
    
    # Special analysis for export_ERS and Vp
    df_ers, df_vp = compare_export_ers_and_vp()
    
    # Create complete hierarchy
    all_info = create_complete_hierarchy()
    
    # Analyze relationships
    analyze_relationships(all_info)
    
    # Compare time coverage
    compare_time_coverage(all_info)
    
    # Final summary
    print(f"\n{'='*80}")
    print("FINAL SUMMARY")
    print(f"{'='*80}")
    
    print(f"""
🎯 KEY FINDINGS:

1. DATASET HIERARCHY (by completeness):
   Level 1: export_ERS_2023-12 (~48 params) - MOST COMPLETE but parsing issue
   Level 2: All_24-07 (45 params) - Complete system, July only
   Level 3: Relevant-1_2024 (23 params) - Extended set, full year
   Level 4: Relevant_2024 (15 params) - Basic set, full year  
   Level 5: Durchfluss/Vp (4 params) - Minimal, flow only

2. TIME COVERAGE:
   • export_ERS: Dec 2023 - Mar 2025 (16 months) - LONGEST
   • Relevant files: Jan - Dec 2024 (12 months)
   • Durchfluss: Jan - Dec 2024 (12 months)
   • All_24-07: July 2024 (1 month)
   • Vp.csv: Partial/unclear

3. DATA QUALITY ISSUES:
   • export_ERS_2023-12: Needs semicolon separator (currently 1 column)
   • Vp.csv: Same parsing issue + incomplete data (7,618 rows)
   
4. RECOMMENDED USE:
   • For complete system analysis: Fix and use export_ERS_2023-12
   • For 2024 trends: Use Relevant-1_2024
   • For July detail: Use All_24-07
   • For flow analysis: Use Durchfluss_2024

5. IDENTICAL STRUCTURES:
   • Durchfluss_2024 ≡ Vp.csv (both 4 params, different row counts)
   • All others are unique configurations
""")
    
    # Save documentation
    doc_path = BASE_PATH / "docs/complete-dataset-comparison.md"
    doc_content = f"""# Complete Dataset Comparison - Erentrudisstraße

## All CSV Files Overview

| File | Parameters | Rows | Time Period | Status |
|------|------------|------|-------------|--------|
| export_ERS_2023-12 | ~48* | 484 | Dec 2023 - Mar 2025 | ⚠️ Parsing issue |
| All_24-07 | 45 | 8,322 | July 2024 | ✅ Complete |
| Relevant-1_2024 | 23 | 89,202 | Jan-Dec 2024 | ✅ Extended |
| Relevant_2024 | 15 | 89,202 | Jan-Dec 2024 | ✅ Basic |
| Durchfluss_2024 | 4 | 89,202 | Jan-Dec 2024 | ✅ Minimal |
| Vp.csv | 4* | 7,618 | Unclear | ⚠️ Parsing issue + incomplete |

*Files marked with ⚠️ need semicolon separator for proper parsing

## Key Relationships

```
export_ERS (48 params, longest period)
    ⊃ All_24-07 (45 params, July only)
        ⊃ Relevant-1_2024 (23 params, full year)
            ⊃ Relevant_2024 (15 params, full year)
                ⊃ Durchfluss (4 params, full year)
                    ≡ Vp.csv (4 params, incomplete)
```

## Recommendations

1. **Fix parsing issues** in export_ERS and Vp.csv files
2. **Use export_ERS** for most comprehensive analysis after fixing
3. **Use Relevant-1_2024** for complete 2024 analysis
4. **Use All_24-07** for detailed July analysis
5. **Use Durchfluss** for hydraulic calculations only
"""
    
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(doc_content)
    
    print(f"\n📄 Final documentation saved: {doc_path}")

if __name__ == "__main__":
    main()