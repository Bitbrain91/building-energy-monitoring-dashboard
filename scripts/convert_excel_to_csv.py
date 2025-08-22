"""
Convert FIS_Inhauser Excel file to CSV for dashboard usage
"""
import pandas as pd
from pathlib import Path

# Define paths
base_path = Path(__file__).parent.parent
excel_file = base_path / "Daten" / "Monitoringdaten" / "FIS_Inhauser" / "Monitoring" / "2024-2025-05_AT.xlsx"
output_file = base_path / "docs" / "FIS_Inhauser_2024-2025-05_AT.csv"

print(f"Converting Excel file to CSV...")
print(f"Source: {excel_file}")
print(f"Target: {output_file}")

try:
    # Read Excel file
    df = pd.read_excel(excel_file, engine='openpyxl')
    
    # Save as CSV
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"✓ Successfully converted! {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {', '.join(df.columns[:10])}...")
    
except Exception as e:
    print(f"✗ Error converting file: {e}")