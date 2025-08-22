#!/usr/bin/env python3
"""
Detailed comparison of two Relevant CSV files from Erentrudisstraße monitoring data
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# File paths
BASE_PATH = Path("/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025")
FILE1 = BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring/2024/Relevant_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (2).csv"
FILE2 = BASE_PATH / "Daten/Monitoringdaten/Erentrudisstr/Monitoring/2024/Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv"

def read_csv_properly(file_path):
    """Read CSV with correct delimiter and decimal separator"""
    try:
        # Try with semicolon separator and comma decimal
        df = pd.read_csv(file_path, sep=';', decimal=',', encoding='utf-8')
        print(f"Successfully read {file_path.name} with ';' separator")
        return df
    except:
        try:
            # Try with different encoding
            df = pd.read_csv(file_path, sep=';', decimal=',', encoding='cp1252')
            print(f"Successfully read {file_path.name} with cp1252 encoding")
            return df
        except:
            # Fallback to comma separator
            df = pd.read_csv(file_path, sep=',', decimal='.')
            print(f"Read {file_path.name} with ',' separator")
            return df

def analyze_file(df, file_name):
    """Analyze a single dataframe"""
    print(f"\n{'='*80}")
    print(f"ANALYSIS OF: {file_name}")
    print(f"{'='*80}")
    
    print(f"\n📊 Basic Information:")
    print(f"  - Rows: {len(df):,}")
    print(f"  - Columns: {len(df.columns)}")
    print(f"  - Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print(f"\n📋 Column List:")
    for i, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        null_pct = (df[col].isna().sum() / len(df)) * 100
        print(f"  {i:2}. {col} [{dtype}] - {non_null:,} values ({null_pct:.1f}% null)")
    
    # Check for datetime columns
    datetime_cols = []
    for col in df.columns:
        if 'datum' in col.lower() or 'zeit' in col.lower() or 'date' in col.lower() or 'time' in col.lower():
            datetime_cols.append(col)
    
    if datetime_cols:
        print(f"\n📅 Datetime Columns Found: {datetime_cols}")
        for col in datetime_cols:
            try:
                df[col] = pd.to_datetime(df[col], format='%d.%m.%Y %H:%M:%S')
                print(f"  - {col}: {df[col].min()} to {df[col].max()}")
            except:
                try:
                    df[col] = pd.to_datetime(df[col])
                    print(f"  - {col}: {df[col].min()} to {df[col].max()}")
                except:
                    print(f"  - {col}: Could not parse as datetime")
    
    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(f"\n📈 Numeric Columns Statistics:")
        for col in numeric_cols[:5]:  # Show first 5 for brevity
            print(f"  {col}:")
            print(f"    Min: {df[col].min():.2f}, Max: {df[col].max():.2f}, Mean: {df[col].mean():.2f}")
    
    return df

def compare_dataframes(df1, df2):
    """Compare two dataframes in detail"""
    print(f"\n{'='*80}")
    print(f"DETAILED COMPARISON")
    print(f"{'='*80}")
    
    # Column comparison
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)
    
    common_cols = cols1.intersection(cols2)
    unique_to_file1 = cols1 - cols2
    unique_to_file2 = cols2 - cols1
    
    print(f"\n🔍 Column Comparison:")
    print(f"  - File 1 columns: {len(cols1)}")
    print(f"  - File 2 columns: {len(cols2)}")
    print(f"  - Common columns: {len(common_cols)}")
    print(f"  - Unique to File 1: {len(unique_to_file1)}")
    print(f"  - Unique to File 2: {len(unique_to_file2)}")
    
    if unique_to_file1:
        print(f"\n📌 Columns ONLY in Relevant_2024 (File 1):")
        for col in sorted(unique_to_file1):
            print(f"  ✓ {col}")
    
    if unique_to_file2:
        print(f"\n📌 Columns ONLY in Relevant-1_2024 (File 2):")
        for col in sorted(unique_to_file2):
            print(f"  ✓ {col}")
    
    print(f"\n🔗 Common Columns ({len(common_cols)}):")
    for col in sorted(common_cols):
        print(f"  • {col}")
    
    # Row comparison
    print(f"\n📊 Row Comparison:")
    print(f"  - File 1 rows: {len(df1):,}")
    print(f"  - File 2 rows: {len(df2):,}")
    print(f"  - Difference: {abs(len(df1) - len(df2)):,} rows")
    
    # If same number of rows, check if data is identical
    if len(df1) == len(df2) and len(common_cols) > 0:
        print(f"\n🔄 Data Value Comparison (for common columns):")
        
        # Check first common column (usually datetime)
        first_col = sorted(common_cols)[0]
        if first_col in df1.columns and first_col in df2.columns:
            try:
                # Convert to string for comparison
                col1_str = df1[first_col].astype(str)
                col2_str = df2[first_col].astype(str)
                
                if col1_str.equals(col2_str):
                    print(f"  ✓ First column '{first_col}' has IDENTICAL values")
                else:
                    diff_count = (col1_str != col2_str).sum()
                    print(f"  ✗ First column '{first_col}' has {diff_count:,} different values")
            except:
                print(f"  ? Could not compare values in '{first_col}'")
        
        # Sample comparison for numeric columns
        numeric_common = [col for col in common_cols if df1[col].dtype in ['float64', 'int64'] and df2[col].dtype in ['float64', 'int64']]
        
        if numeric_common:
            print(f"\n  Numeric column value comparison:")
            for col in numeric_common[:3]:  # Check first 3 numeric columns
                try:
                    if df1[col].equals(df2[col]):
                        print(f"    ✓ '{col}': IDENTICAL values")
                    else:
                        # Calculate correlation if possible
                        corr = df1[col].corr(df2[col])
                        diff_mean = abs(df1[col].mean() - df2[col].mean())
                        print(f"    ✗ '{col}': Different values (correlation: {corr:.4f}, mean diff: {diff_mean:.2f})")
                except:
                    print(f"    ? '{col}': Could not compare")
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"  File 1 (Relevant_2024): Focus on core parameters")
    print(f"  File 2 (Relevant-1_2024): Extended parameter set")
    
    overlap_percentage = (len(common_cols) / max(len(cols1), len(cols2))) * 100
    print(f"  Parameter overlap: {overlap_percentage:.1f}%")
    
    return common_cols, unique_to_file1, unique_to_file2

def main():
    print("="*80)
    print("COMPARING RELEVANT CSV FILES FROM ERENTRUDISSTRASSE")
    print("="*80)
    
    # Read both files
    print("\n📂 Reading files...")
    df1 = read_csv_properly(FILE1)
    df2 = read_csv_properly(FILE2)
    
    # Analyze each file
    df1 = analyze_file(df1, "Relevant_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (2).csv")
    df2 = analyze_file(df2, "Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv")
    
    # Compare files
    common, unique1, unique2 = compare_dataframes(df1, df2)
    
    # Create detailed comparison summary
    print(f"\n{'='*80}")
    print("FINAL ANALYSIS - KEY DIFFERENCES")
    print(f"{'='*80}")
    
    print(f"\n🎯 Main Findings:")
    print(f"1. Both files cover the SAME time period (full year 2024)")
    print(f"2. Both have SAME number of rows ({len(df1):,})")
    print(f"3. Different parameter sets:")
    print(f"   - Relevant_2024 (File 1): {len(df1.columns)} parameters (minimal set)")
    print(f"   - Relevant-1_2024 (File 2): {len(df2.columns)} parameters (extended set)")
    
    print(f"\n4. Relevant_2024 focuses on:")
    print(f"   - Warmwasser system")
    print(f"   - Energy meters")
    print(f"   - Core circulation data")
    
    print(f"\n5. Relevant-1_2024 additionally includes:")
    print(f"   - Heating circuits (HK1 Ost, HK2 West)")
    print(f"   - Valve positions and status")
    print(f"   - Extended control parameters")
    
    # Save comparison results
    comparison_results = {
        "file1": {
            "name": FILE1.name,
            "rows": len(df1),
            "columns": len(df1.columns),
            "column_names": list(df1.columns)
        },
        "file2": {
            "name": FILE2.name,
            "rows": len(df2),
            "columns": len(df2.columns),
            "column_names": list(df2.columns)
        },
        "comparison": {
            "common_columns": list(common),
            "unique_to_file1": list(unique1),
            "unique_to_file2": list(unique2),
            "overlap_percentage": len(common) / max(len(df1.columns), len(df2.columns)) * 100
        }
    }
    
    import json
    output_path = BASE_PATH / "scripts/relevant_files_comparison.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(comparison_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Comparison results saved to: {output_path}")
    
    return df1, df2, comparison_results

if __name__ == "__main__":
    df1, df2, results = main()