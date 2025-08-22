#!/usr/bin/env python3
"""
Analyze Erentrudisstraße monitoring datasets
This script loads and compares all CSV and Excel files to identify overlaps, subsets and similarities
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import json
from datetime import datetime
import sys

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set paths
BASE_PATH = Path("/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025")
DATA_PATH = BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring"

def parse_datetime_flexible(date_str):
    """Parse datetime strings with various formats"""
    formats = [
        '%d.%m.%Y %H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%d.%m.%Y %H:%M',
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%m/%d/%Y %H:%M:%S',
        '%m/%d/%Y'
    ]
    
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    
    # Try pandas' flexible parser as last resort
    try:
        return pd.to_datetime(date_str)
    except:
        return None

def analyze_csv_file(file_path):
    """Analyze a single CSV file"""
    print(f"\nAnalyzing CSV: {file_path.name}")
    print("-" * 60)
    
    try:
        # Try different encodings
        encodings = ['utf-8', 'cp1252', 'iso-8859-1', 'latin1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding, sep=';', decimal=',')
                break
            except:
                continue
        
        if df is None:
            # Try with comma separator
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding, sep=',', decimal='.')
                    break
                except:
                    continue
        
        if df is None:
            print(f"Could not read file {file_path.name}")
            return None
        
        # Basic info
        info = {
            'file_name': file_path.name,
            'file_path': str(file_path),
            'rows': len(df),
            'columns': list(df.columns),
            'column_count': len(df.columns),
            'data_types': df.dtypes.to_dict() if not df.empty else {},
        }
        
        # Try to identify datetime columns
        datetime_cols = []
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower() or 'zeit' in col.lower():
                datetime_cols.append(col)
            elif df[col].dtype == 'object' and len(df) > 0:
                # Check if it looks like datetime
                sample = str(df[col].iloc[0])
                if any(char in sample for char in ['-', '/', '.', ':']):
                    try:
                        parse_datetime_flexible(sample)
                        datetime_cols.append(col)
                    except:
                        pass
        
        # Parse datetime columns
        for col in datetime_cols:
            try:
                df[col] = df[col].apply(parse_datetime_flexible)
            except:
                pass
        
        # Get time range if datetime columns exist
        time_range = {}
        for col in datetime_cols:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                time_range[col] = {
                    'min': str(df[col].min()),
                    'max': str(df[col].max())
                }
        
        info['datetime_columns'] = datetime_cols
        info['time_range'] = time_range
        
        # Get numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        info['numeric_columns'] = numeric_cols
        
        # Sample data
        if len(df) > 0:
            info['sample_data'] = df.head(3).to_dict('records')
        
        # Parameter analysis
        parameters = []
        for col in df.columns:
            if col not in datetime_cols:
                params = {
                    'name': col,
                    'dtype': str(df[col].dtype),
                    'unique_values': df[col].nunique() if len(df) > 0 else 0,
                    'null_count': df[col].isnull().sum()
                }
                if df[col].dtype in ['float64', 'int64']:
                    params['min'] = float(df[col].min()) if not df[col].isnull().all() else None
                    params['max'] = float(df[col].max()) if not df[col].isnull().all() else None
                    params['mean'] = float(df[col].mean()) if not df[col].isnull().all() else None
                parameters.append(params)
        
        info['parameters'] = parameters
        
        print(f"Rows: {info['rows']}")
        print(f"Columns: {info['column_count']}")
        print(f"Column names: {', '.join(info['columns'][:10])}")
        if len(info['columns']) > 10:
            print(f"  ... and {len(info['columns']) - 10} more columns")
        if time_range:
            for col, range_info in time_range.items():
                print(f"Time range ({col}): {range_info['min']} to {range_info['max']}")
        
        return info
        
    except Exception as e:
        print(f"Error analyzing {file_path.name}: {str(e)}")
        return None

def analyze_excel_file(file_path):
    """Analyze an Excel file with multiple sheets"""
    print(f"\nAnalyzing Excel: {file_path.name}")
    print("-" * 60)
    
    try:
        # Read Excel file
        xl_file = pd.ExcelFile(file_path)
        
        file_info = {
            'file_name': file_path.name,
            'file_path': str(file_path),
            'sheets': {},
            'sheet_count': len(xl_file.sheet_names)
        }
        
        print(f"Sheet count: {file_info['sheet_count']}")
        print(f"Sheet names: {', '.join(xl_file.sheet_names)}")
        
        # Analyze each sheet
        for sheet_name in xl_file.sheet_names:
            print(f"\n  Sheet: {sheet_name}")
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                if df.empty:
                    print(f"    Empty sheet")
                    continue
                
                sheet_info = {
                    'rows': len(df),
                    'columns': list(df.columns),
                    'column_count': len(df.columns),
                    'data_types': {str(k): str(v) for k, v in df.dtypes.to_dict().items()}
                }
                
                # Identify datetime columns
                datetime_cols = []
                for col in df.columns:
                    if pd.api.types.is_datetime64_any_dtype(df[col]):
                        datetime_cols.append(col)
                    elif 'date' in str(col).lower() or 'time' in str(col).lower() or 'zeit' in str(col).lower():
                        datetime_cols.append(col)
                
                # Get time range
                time_range = {}
                for col in datetime_cols:
                    try:
                        if pd.api.types.is_datetime64_any_dtype(df[col]):
                            time_range[col] = {
                                'min': str(df[col].min()),
                                'max': str(df[col].max())
                            }
                    except:
                        pass
                
                sheet_info['datetime_columns'] = datetime_cols
                sheet_info['time_range'] = time_range
                
                # Get numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                sheet_info['numeric_columns'] = numeric_cols
                
                # Parameters
                parameters = []
                for col in df.columns:
                    if col not in datetime_cols:
                        params = {
                            'name': str(col),
                            'dtype': str(df[col].dtype),
                            'unique_values': df[col].nunique(),
                            'null_count': df[col].isnull().sum()
                        }
                        if df[col].dtype in ['float64', 'int64']:
                            params['min'] = float(df[col].min()) if not df[col].isnull().all() else None
                            params['max'] = float(df[col].max()) if not df[col].isnull().all() else None
                        parameters.append(params)
                
                sheet_info['parameters'] = parameters
                
                file_info['sheets'][sheet_name] = sheet_info
                
                print(f"    Rows: {sheet_info['rows']}")
                print(f"    Columns: {sheet_info['column_count']}")
                if time_range:
                    for col, range_info in time_range.items():
                        print(f"    Time range ({col}): {range_info['min']} to {range_info['max']}")
                
            except Exception as e:
                print(f"    Error reading sheet: {str(e)}")
                file_info['sheets'][sheet_name] = {'error': str(e)}
        
        return file_info
        
    except Exception as e:
        print(f"Error analyzing {file_path.name}: {str(e)}")
        return None

def compare_datasets(datasets):
    """Compare datasets for overlaps and relationships"""
    print("\n\n" + "=" * 80)
    print("DATASET COMPARISON AND RELATIONSHIPS")
    print("=" * 80)
    
    comparisons = {
        'parameter_overlaps': [],
        'time_overlaps': [],
        'potential_subsets': [],
        'similar_structures': []
    }
    
    # Extract all parameters from all datasets
    all_params = {}
    all_time_ranges = {}
    
    for dataset in datasets:
        if dataset is None:
            continue
            
        file_name = dataset['file_name']
        
        # For CSV files
        if 'parameters' in dataset:
            params = set([p['name'] for p in dataset['parameters']])
            all_params[file_name] = params
            
            if dataset.get('time_range'):
                all_time_ranges[file_name] = dataset['time_range']
        
        # For Excel files
        elif 'sheets' in dataset:
            for sheet_name, sheet_data in dataset['sheets'].items():
                if 'parameters' in sheet_data:
                    key = f"{file_name} - {sheet_name}"
                    params = set([p['name'] for p in sheet_data['parameters']])
                    all_params[key] = params
                    
                    if sheet_data.get('time_range'):
                        all_time_ranges[key] = sheet_data['time_range']
    
    # Compare parameters between datasets
    print("\n1. PARAMETER OVERLAPS:")
    print("-" * 40)
    
    file_names = list(all_params.keys())
    for i in range(len(file_names)):
        for j in range(i + 1, len(file_names)):
            file1 = file_names[i]
            file2 = file_names[j]
            
            params1 = all_params[file1]
            params2 = all_params[file2]
            
            common = params1.intersection(params2)
            
            if common:
                overlap_pct = len(common) * 100 / min(len(params1), len(params2))
                print(f"\n{file1} <-> {file2}")
                print(f"  Common parameters ({len(common)}): {', '.join(list(common)[:10])}")
                if len(common) > 10:
                    print(f"    ... and {len(common) - 10} more")
                print(f"  Overlap: {overlap_pct:.1f}%")
                
                comparisons['parameter_overlaps'].append({
                    'file1': file1,
                    'file2': file2,
                    'common_params': list(common),
                    'overlap_percentage': overlap_pct
                })
                
                # Check for subset relationships
                if params1.issubset(params2):
                    print(f"  → {file1} is a SUBSET of {file2}")
                    comparisons['potential_subsets'].append({
                        'subset': file1,
                        'superset': file2
                    })
                elif params2.issubset(params1):
                    print(f"  → {file2} is a SUBSET of {file1}")
                    comparisons['potential_subsets'].append({
                        'subset': file2,
                        'superset': file1
                    })
    
    # Compare time ranges
    print("\n2. TIME PERIOD OVERLAPS:")
    print("-" * 40)
    
    for file1, range1 in all_time_ranges.items():
        for file2, range2 in all_time_ranges.items():
            if file1 >= file2:
                continue
            
            # Find common time columns
            for col1, times1 in range1.items():
                for col2, times2 in range2.items():
                    try:
                        start1 = pd.to_datetime(times1['min'])
                        end1 = pd.to_datetime(times1['max'])
                        start2 = pd.to_datetime(times2['min'])
                        end2 = pd.to_datetime(times2['max'])
                        
                        # Check for overlap
                        if start1 <= end2 and start2 <= end1:
                            overlap_start = max(start1, start2)
                            overlap_end = min(end1, end2)
                            
                            print(f"\n{file1} <-> {file2}")
                            print(f"  Time overlap: {overlap_start} to {overlap_end}")
                            
                            comparisons['time_overlaps'].append({
                                'file1': file1,
                                'file2': file2,
                                'overlap_start': str(overlap_start),
                                'overlap_end': str(overlap_end)
                            })
                    except:
                        pass
    
    # Check for similar structures
    print("\n3. SIMILAR STRUCTURES:")
    print("-" * 40)
    
    for i in range(len(file_names)):
        for j in range(i + 1, len(file_names)):
            file1 = file_names[i]
            file2 = file_names[j]
            
            params1 = all_params[file1]
            params2 = all_params[file2]
            
            if len(params1) == len(params2) and params1 == params2:
                print(f"\n{file1} and {file2} have IDENTICAL structure")
                comparisons['similar_structures'].append({
                    'file1': file1,
                    'file2': file2,
                    'relationship': 'identical'
                })
    
    return comparisons

def main():
    """Main analysis function"""
    print("=" * 80)
    print("ERENTRUDISSTRASSE DATASET ANALYSIS")
    print("=" * 80)
    
    # Find all CSV and Excel files
    csv_files = list(DATA_PATH.rglob("*.csv"))
    excel_files = list(DATA_PATH.rglob("*.xlsx"))
    
    print(f"\nFound {len(csv_files)} CSV files and {len(excel_files)} Excel files")
    
    # Analyze all files
    datasets = []
    
    for csv_file in csv_files:
        result = analyze_csv_file(csv_file)
        if result:
            datasets.append(result)
    
    for excel_file in excel_files:
        result = analyze_excel_file(excel_file)
        if result:
            datasets.append(result)
    
    # Compare datasets
    comparison_results = compare_datasets(datasets)
    
    # Save results to JSON for documentation generation
    output = {
        'analysis_date': datetime.now().isoformat(),
        'datasets': datasets,
        'comparisons': comparison_results
    }
    
    output_path = BASE_PATH / "scripts/erentrudisstr_analysis_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"\n\nAnalysis complete! Results saved to {output_path}")
    
    return datasets, comparison_results

if __name__ == "__main__":
    datasets, comparisons = main()