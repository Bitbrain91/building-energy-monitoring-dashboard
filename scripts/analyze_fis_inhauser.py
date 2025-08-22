#!/usr/bin/env python3
"""
Comprehensive analysis of FIS_Inhauser monitoring datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import json
from datetime import datetime

warnings.filterwarnings('ignore')

# Base path
BASE_PATH = Path("/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025")
DATA_PATH = BASE_PATH / "Daten/Monitoringdaten/FIS_Inhauser/Monitoring"

# Files to analyze
FILES = {
    'Main_Excel': DATA_PATH / "2024-2025-05_AT.xlsx",
    'Export_2024-12': DATA_PATH / "250101-250331/export_1551_2024-12-31-00-00_2025-03-31-23-55.csv",
    'Export_2025-01': DATA_PATH / "250101-250331/test/export_1551_2025-01-01-00-00_2025-03-31-23-55.csv",
    'V1_Export': DATA_PATH / "250101-250331/test/V1_2501_EXPORT_1.CSV",
    'Test_Excel': DATA_PATH / "250101-250331/test/250123-250129_ok_250130.xlsx"
}

def read_csv_flexible(file_path):
    """Try different methods to read CSV"""
    encodings = ['utf-8', 'cp1252', 'iso-8859-1', 'latin1']
    separators = [',', ';', '\t']
    
    for sep in separators:
        for enc in encodings:
            try:
                df = pd.read_csv(file_path, sep=sep, encoding=enc)
                # Check if parsing was successful
                if len(df.columns) > 1 or (len(df.columns) == 1 and sep not in df.columns[0]):
                    print(f"  ✓ Read with separator '{sep}' and encoding '{enc}'")
                    return df
            except:
                continue
    
    # Try with decimal comma
    for sep in [';', '\t']:
        try:
            df = pd.read_csv(file_path, sep=sep, decimal=',', encoding='utf-8')
            if len(df.columns) > 1:
                print(f"  ✓ Read with separator '{sep}' and decimal ','")
                return df
        except:
            continue
    
    print(f"  ⚠️ Could not parse CSV properly")
    return None

def analyze_csv_file(file_path, name):
    """Analyze a CSV file"""
    print(f"\n{'='*80}")
    print(f"ANALYZING: {name}")
    print(f"{'='*80}")
    print(f"File: {file_path.name}")
    print(f"Path: {file_path.parent.name}/{file_path.name}")
    
    df = read_csv_flexible(file_path)
    
    if df is None:
        print("  ❌ Failed to read file")
        return None
    
    info = {
        'file_name': file_path.name,
        'file_path': str(file_path),
        'rows': len(df),
        'columns': len(df.columns),
        'column_names': list(df.columns),
        'parameters': []
    }
    
    print(f"\n📊 Basic Info:")
    print(f"  • Rows: {info['rows']:,}")
    print(f"  • Columns: {info['columns']}")
    
    # Try to identify datetime columns
    datetime_cols = []
    for col in df.columns:
        if any(term in str(col).lower() for term in ['date', 'datum', 'zeit', 'time', 'timestamp']):
            datetime_cols.append(col)
    
    # Parse datetime columns
    for col in datetime_cols:
        try:
            # Try different date formats
            for fmt in ['%d.%m.%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%d.%m.%Y %H:%M', '%m/%d/%Y %H:%M']:
                try:
                    df[col] = pd.to_datetime(df[col], format=fmt)
                    break
                except:
                    continue
            
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                info['time_start'] = df[col].min()
                info['time_end'] = df[col].max()
                print(f"  • Time range: {info['time_start']} to {info['time_end']}")
                print(f"  • Duration: {(info['time_end'] - info['time_start']).days + 1} days")
        except:
            pass
    
    # List parameters
    print(f"\n📋 Parameters ({len(df.columns)}):")
    
    # Group parameters by type
    temp_params = []
    flow_params = []
    power_params = []
    valve_params = []
    pump_params = []
    other_params = []
    
    for col in df.columns:
        col_str = str(col)
        if '°C' in col_str or 'Temp' in col_str or 'temperatur' in col_str.lower():
            temp_params.append(col)
        elif 'm³/h' in col_str or 'Durchfluss' in col_str or 'flow' in col_str.lower():
            flow_params.append(col)
        elif 'kW' in col_str or 'W' in col_str or 'Leistung' in col_str or 'Power' in col_str:
            power_params.append(col)
        elif 'Ventil' in col_str or 'valve' in col_str.lower() or '%' in col_str:
            valve_params.append(col)
        elif 'Pumpe' in col_str or 'pump' in col_str.lower():
            pump_params.append(col)
        else:
            other_params.append(col)
    
    if temp_params:
        print(f"\n  🌡️ Temperature ({len(temp_params)}):")
        for p in temp_params[:5]:
            print(f"    • {p}")
        if len(temp_params) > 5:
            print(f"    ... and {len(temp_params) - 5} more")
    
    if flow_params:
        print(f"\n  💧 Flow ({len(flow_params)}):")
        for p in flow_params[:5]:
            print(f"    • {p}")
    
    if power_params:
        print(f"\n  ⚡ Power/Energy ({len(power_params)}):")
        for p in power_params[:5]:
            print(f"    • {p}")
    
    if valve_params:
        print(f"\n  🔧 Valves/Control ({len(valve_params)}):")
        for p in valve_params[:5]:
            print(f"    • {p}")
    
    if pump_params:
        print(f"\n  🔄 Pumps ({len(pump_params)}):")
        for p in pump_params[:5]:
            print(f"    • {p}")
    
    if other_params:
        print(f"\n  📌 Other ({len(other_params)}):")
        for p in other_params[:5]:
            print(f"    • {p}")
    
    # Store parameter info
    info['temp_params'] = len(temp_params)
    info['flow_params'] = len(flow_params)
    info['power_params'] = len(power_params)
    info['valve_params'] = len(valve_params)
    info['pump_params'] = len(pump_params)
    
    return info

def analyze_excel_file(file_path, name):
    """Analyze Excel file"""
    print(f"\n{'='*80}")
    print(f"ANALYZING: {name}")
    print(f"{'='*80}")
    print(f"File: {file_path.name}")
    
    try:
        xl_file = pd.ExcelFile(file_path)
        
        print(f"\n📊 Excel File Info:")
        print(f"  • Sheets: {len(xl_file.sheet_names)}")
        print(f"  • Sheet names: {', '.join(xl_file.sheet_names)}")
        
        file_info = {
            'file_name': file_path.name,
            'file_path': str(file_path),
            'sheet_count': len(xl_file.sheet_names),
            'sheets': {}
        }
        
        # Analyze each sheet
        for sheet_name in xl_file.sheet_names:
            print(f"\n  📄 Sheet: '{sheet_name}'")
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                if df.empty:
                    print(f"    Empty sheet")
                    continue
                
                print(f"    • Rows: {len(df):,}")
                print(f"    • Columns: {len(df.columns)}")
                
                sheet_info = {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': list(df.columns)
                }
                
                # Check for datetime
                for col in df.columns:
                    if pd.api.types.is_datetime64_any_dtype(df[col]):
                        sheet_info['time_start'] = str(df[col].min())
                        sheet_info['time_end'] = str(df[col].max())
                        print(f"    • Time range: {df[col].min()} to {df[col].max()}")
                        break
                
                file_info['sheets'][sheet_name] = sheet_info
                
            except Exception as e:
                print(f"    Error reading sheet: {str(e)}")
        
        return file_info
        
    except Exception as e:
        print(f"  ❌ Error reading Excel file: {str(e)}")
        return None

def compare_datasets(all_info):
    """Compare all datasets"""
    print(f"\n{'='*80}")
    print("DATASET COMPARISON")
    print(f"{'='*80}")
    
    # Extract valid datasets
    valid_datasets = [info for info in all_info if info is not None]
    
    if not valid_datasets:
        print("No valid datasets to compare")
        return
    
    print(f"\n📊 Overview:")
    print(f"  • Total files analyzed: {len(FILES)}")
    print(f"  • Successfully read: {len(valid_datasets)}")
    
    # Compare sizes
    print(f"\n📈 Dataset Sizes:")
    for info in valid_datasets:
        if 'rows' in info:
            print(f"  • {info['file_name']}: {info['rows']:,} rows × {info['columns']} columns")
        elif 'sheet_count' in info:
            total_rows = sum(sheet.get('rows', 0) for sheet in info.get('sheets', {}).values())
            print(f"  • {info['file_name']}: {info['sheet_count']} sheets, ~{total_rows:,} total rows")
    
    # Compare time ranges
    print(f"\n📅 Time Coverage:")
    for info in valid_datasets:
        if 'time_start' in info:
            print(f"  • {info['file_name']}: {info['time_start']} to {info['time_end']}")
        elif 'sheets' in info:
            for sheet_name, sheet_info in info['sheets'].items():
                if 'time_start' in sheet_info:
                    print(f"  • {info['file_name']} ({sheet_name}): {sheet_info['time_start']} to {sheet_info['time_end']}")
    
    # Compare parameter types
    print(f"\n🔧 Parameter Types:")
    for info in valid_datasets:
        if 'temp_params' in info:
            print(f"\n  {info['file_name']}:")
            print(f"    🌡️ Temperature: {info['temp_params']}")
            print(f"    💧 Flow: {info['flow_params']}")
            print(f"    ⚡ Power: {info['power_params']}")
            print(f"    🔧 Valves: {info['valve_params']}")
            print(f"    🔄 Pumps: {info['pump_params']}")

def main():
    print("="*80)
    print("FIS_INHAUSER MONITORING DATA ANALYSIS")
    print("="*80)
    print(f"\nAnalyzing datasets in: {DATA_PATH}")
    
    all_info = []
    
    # Analyze each file
    for name, file_path in FILES.items():
        if file_path.exists():
            if file_path.suffix == '.csv' or file_path.suffix == '.CSV':
                info = analyze_csv_file(file_path, name)
            elif file_path.suffix == '.xlsx':
                info = analyze_excel_file(file_path, name)
            else:
                print(f"\n⚠️ Unknown file type: {file_path.name}")
                info = None
            
            if info:
                all_info.append(info)
        else:
            print(f"\n❌ File not found: {file_path}")
    
    # Compare datasets
    compare_datasets(all_info)
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    
    print(f"""
🎯 Key Findings:

1. FILE STRUCTURE:
   • Main monitoring folder contains 1 Excel file and multiple CSV exports
   • Subfolder '250101-250331' contains recent exports (Jan-Mar 2025)
   • Test subfolder contains additional test data

2. TIME PERIODS:
   • Main period: End of 2024 to March 2025
   • Export files span from Dec 31, 2024 to Mar 31, 2025
   • Test data focuses on late January 2025

3. DATA ORGANIZATION:
   • Excel files likely contain aggregated/processed data
   • CSV exports are raw monitoring data
   • File naming convention: export_[ID]_[start-date]_[end-date].csv

4. RECOMMENDED ANALYSIS:
   • Start with main Excel file (2024-2025-05_AT.xlsx) for overview
   • Use CSV exports for detailed time-series analysis
   • Compare test folder data with main exports for validation
""")
    
    # Save results
    output_path = BASE_PATH / "scripts/fis_inhauser_analysis_results.json"
    
    results = {
        'analysis_date': datetime.now().isoformat(),
        'datasets': all_info,
        'file_count': len(FILES),
        'valid_datasets': len([i for i in all_info if i is not None])
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {output_path}")

if __name__ == "__main__":
    main()