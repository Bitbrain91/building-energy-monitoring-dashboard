import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

class KWNeukirchenAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.data_summary = {
            'ubergabe_bezug': {},
            'ubergabe_lieferung': {},
            'kw_erzeugung': {}
        }
        self.file_mapping = []
        
    def analyze_ubergabe_files(self):
        """Analyze ÜBERGABE BEZUG and LIEFERUNG files"""
        print("Analyzing ÜBERGABE files...")
        
        for year in ['2020', '2021', '2022', '2023', '2024']:
            year_path = self.base_path / year
            if year_path.exists():
                for month in range(1, 13):
                    # Analyze BEZUG files
                    bezug_file = year_path / f"ÜBERGABE_BEZUG_{year}.{month:02d}.XLSX"
                    if bezug_file.exists():
                        try:
                            df = pd.read_excel(bezug_file, engine='openpyxl')
                            self.data_summary['ubergabe_bezug'][f"{year}-{month:02d}"] = {
                                'rows': len(df),
                                'columns': list(df.columns),
                                'column_count': len(df.columns),
                                'null_count': int(df.isnull().sum().sum()),
                                'null_percentage': float((df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)) if len(df) > 0 else 0,
                                'dtypes': {str(k): v for k, v in df.dtypes.value_counts().to_dict().items()},
                                'file_size_kb': os.path.getsize(bezug_file) / 1024
                            }
                            
                            # Add to file mapping
                            self.file_mapping.append({
                                'file': str(bezug_file.relative_to(self.base_path)),
                                'type': 'ÜBERGABE_BEZUG',
                                'year': year,
                                'month': month,
                                'rows': len(df),
                                'columns': len(df.columns),
                                'data_description': 'Bezugsdaten (consumption/procurement data)'
                            })
                            
                            print(f"  Analyzed: {bezug_file.name} - {len(df)} rows")
                        except Exception as e:
                            print(f"  Error reading {bezug_file.name}: {e}")
                    
                    # Analyze LIEFERUNG files
                    lieferung_file = year_path / f"ÜBERGABE_LIEFERUNG_{year}.{month:02d}.XLSX"
                    if lieferung_file.exists():
                        try:
                            df = pd.read_excel(lieferung_file, engine='openpyxl')
                            self.data_summary['ubergabe_lieferung'][f"{year}-{month:02d}"] = {
                                'rows': len(df),
                                'columns': list(df.columns),
                                'column_count': len(df.columns),
                                'null_count': int(df.isnull().sum().sum()),
                                'null_percentage': float((df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)) if len(df) > 0 else 0,
                                'dtypes': {str(k): v for k, v in df.dtypes.value_counts().to_dict().items()},
                                'file_size_kb': os.path.getsize(lieferung_file) / 1024
                            }
                            
                            # Add to file mapping
                            self.file_mapping.append({
                                'file': str(lieferung_file.relative_to(self.base_path)),
                                'type': 'ÜBERGABE_LIEFERUNG',
                                'year': year,
                                'month': month,
                                'rows': len(df),
                                'columns': len(df.columns),
                                'data_description': 'Lieferungsdaten (delivery/supply data)'
                            })
                            
                            print(f"  Analyzed: {lieferung_file.name} - {len(df)} rows")
                        except Exception as e:
                            print(f"  Error reading {lieferung_file.name}: {e}")
    
    def analyze_kw_erzeugung_files(self):
        """Analyze KW ERZEUGUNG files for different power plants"""
        print("\nAnalyzing KW ERZEUGUNG files...")
        
        power_plants = ['DÜRNBACH', 'UNTERSULZBACH', 'WIESBACH']
        
        for plant in power_plants:
            for year in ['2020', '2021', '2022', '2023', '2024']:
                file_name = f"KW {plant}_ERZEUGUNG_{year}.XLSX"
                file_path = self.base_path / file_name
                
                if file_path.exists():
                    try:
                        df = pd.read_excel(file_path, engine='openpyxl')
                        
                        # Analyze time series if datetime column exists
                        time_info = {}
                        for col in df.columns:
                            if 'date' in col.lower() or 'zeit' in col.lower() or 'time' in col.lower():
                                try:
                                    df[col] = pd.to_datetime(df[col])
                                    time_info = {
                                        'time_column': col,
                                        'start_date': str(df[col].min()),
                                        'end_date': str(df[col].max()),
                                        'frequency': self.detect_frequency(df[col])
                                    }
                                    break
                                except:
                                    pass
                        
                        self.data_summary['kw_erzeugung'][f"{plant}_{year}"] = {
                            'rows': len(df),
                            'columns': list(df.columns),
                            'column_count': len(df.columns),
                            'null_count': int(df.isnull().sum().sum()),
                            'null_percentage': float((df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)) if len(df) > 0 else 0,
                            'dtypes': {str(k): v for k, v in df.dtypes.value_counts().to_dict().items()},
                            'file_size_kb': os.path.getsize(file_path) / 1024,
                            'time_info': time_info,
                            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist()
                        }
                        
                        # Add to file mapping
                        self.file_mapping.append({
                            'file': file_name,
                            'type': 'KW_ERZEUGUNG',
                            'power_plant': plant,
                            'year': year,
                            'rows': len(df),
                            'columns': len(df.columns),
                            'data_description': f'Erzeugungsdaten (generation data) for {plant} power plant',
                            'time_range': f"{time_info.get('start_date', 'N/A')} to {time_info.get('end_date', 'N/A')}" if time_info else 'N/A'
                        })
                        
                        print(f"  Analyzed: {file_name} - {len(df)} rows")
                    except Exception as e:
                        print(f"  Error reading {file_name}: {e}")
    
    def detect_frequency(self, date_series):
        """Detect the frequency of a time series"""
        if len(date_series) < 2:
            return "Unknown"
        
        # Calculate differences
        diffs = date_series.diff().dropna()
        if len(diffs) == 0:
            return "Unknown"
            
        mode_diff = diffs.mode()
        if len(mode_diff) == 0:
            return "Irregular"
            
        mode_diff = mode_diff[0]
        
        # Determine frequency based on mode difference
        if mode_diff == pd.Timedelta(minutes=15):
            return "15-minute"
        elif mode_diff == pd.Timedelta(hours=1):
            return "Hourly"
        elif mode_diff == pd.Timedelta(days=1):
            return "Daily"
        elif mode_diff == pd.Timedelta(days=7):
            return "Weekly"
        elif 28 <= mode_diff.days <= 31:
            return "Monthly"
        else:
            return f"~{mode_diff.days} days" if mode_diff.days > 0 else f"~{mode_diff.seconds/3600:.1f} hours"
    
    def generate_statistics(self):
        """Generate overall statistics"""
        stats = {
            'total_files': len(self.file_mapping),
            'file_types': {},
            'years_covered': set(),
            'power_plants': set(),
            'total_rows': 0,
            'total_null_percentage': [],
            'data_availability': {}
        }
        
        # Aggregate statistics
        for file_info in self.file_mapping:
            file_type = file_info['type']
            stats['file_types'][file_type] = stats['file_types'].get(file_type, 0) + 1
            stats['years_covered'].add(file_info['year'])
            stats['total_rows'] += file_info['rows']
            
            if 'power_plant' in file_info:
                stats['power_plants'].add(file_info['power_plant'])
        
        # Calculate data availability
        for year in ['2020', '2021', '2022', '2023', '2024']:
            year_files = [f for f in self.file_mapping if f['year'] == year]
            stats['data_availability'][year] = {
                'files': len(year_files),
                'bezug_months': len([f for f in year_files if f['type'] == 'ÜBERGABE_BEZUG']),
                'lieferung_months': len([f for f in year_files if f['type'] == 'ÜBERGABE_LIEFERUNG']),
                'kw_plants': len([f for f in year_files if f['type'] == 'KW_ERZEUGUNG'])
            }
        
        return stats
    
    def sample_data_quality(self):
        """Sample a few files to check data quality in detail"""
        quality_samples = []
        
        # Sample one file from each category
        sample_files = [
            ('2024/ÜBERGABE_BEZUG_2024.12.XLSX', 'ÜBERGABE_BEZUG'),
            ('2024/ÜBERGABE_LIEFERUNG_2024.12.XLSX', 'ÜBERGABE_LIEFERUNG'),
            ('KW DÜRNBACH_ERZEUGUNG_2024.XLSX', 'KW_ERZEUGUNG')
        ]
        
        for file_rel, file_type in sample_files:
            file_path = self.base_path / file_rel
            if file_path.exists():
                try:
                    df = pd.read_excel(file_path, engine='openpyxl')
                    
                    # Detailed quality check
                    quality = {
                        'file': file_rel,
                        'type': file_type,
                        'shape': df.shape,
                        'columns': list(df.columns)[:10],  # First 10 columns
                        'null_by_column': {str(k): int(v) for k, v in df.isnull().sum().to_dict().items()},
                        'data_types': {str(k): str(v) for k, v in df.dtypes.to_dict().items()},
                        'numeric_summary': {}
                    }
                    
                    # Get summary statistics for numeric columns
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    for col in numeric_cols[:5]:  # First 5 numeric columns
                        quality['numeric_summary'][col] = {
                            'mean': float(df[col].mean()) if not pd.isna(df[col].mean()) else None,
                            'std': float(df[col].std()) if not pd.isna(df[col].std()) else None,
                            'min': float(df[col].min()) if not pd.isna(df[col].min()) else None,
                            'max': float(df[col].max()) if not pd.isna(df[col].max()) else None,
                            'nulls': int(df[col].isnull().sum())
                        }
                    
                    quality_samples.append(quality)
                    print(f"  Quality sampled: {file_rel}")
                except Exception as e:
                    print(f"  Error sampling {file_rel}: {e}")
        
        return quality_samples
    
    def run_analysis(self):
        """Run complete analysis"""
        print("Starting KW-Neukirchen Data Analysis")
        print("=" * 50)
        
        # Run analyses
        self.analyze_ubergabe_files()
        self.analyze_kw_erzeugung_files()
        
        # Generate statistics
        stats = self.generate_statistics()
        
        # Sample data quality
        quality_samples = self.sample_data_quality()
        
        # Prepare results
        results = {
            'analysis_timestamp': datetime.now().isoformat(),
            'base_path': str(self.base_path),
            'statistics': stats,
            'file_mapping': self.file_mapping,
            'data_summary': self.data_summary,
            'quality_samples': quality_samples
        }
        
        return results

# Run the analysis
if __name__ == "__main__":
    base_path = "/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025/Daten/vertraulich_erzeugungsdaten-kw-neukirchen_2025-07-21_0937"
    
    analyzer = KWNeukirchenAnalyzer(base_path)
    results = analyzer.run_analysis()
    
    # Save results to JSON
    output_file = Path("/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025/scripts/kw_neukirchen_analysis_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\nAnalysis complete! Results saved to {output_file}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total files analyzed: {results['statistics']['total_files']}")
    print(f"Years covered: {sorted(results['statistics']['years_covered'])}")
    print(f"Power plants: {sorted(results['statistics']['power_plants'])}")
    print(f"Total data rows: {results['statistics']['total_rows']:,}")
    print("\nFile type breakdown:")
    for ftype, count in results['statistics']['file_types'].items():
        print(f"  {ftype}: {count} files")