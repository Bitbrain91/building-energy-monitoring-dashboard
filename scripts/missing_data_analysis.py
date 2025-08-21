#!/usr/bin/env python3
"""
Detaillierte Analyse fehlender und fehlerhafter Daten
für FIS_Inhauser und Erentrudisstr
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class MissingDataAnalyzer:
    def __init__(self, base_path):
        self.base_path = base_path
        self.results = {
            'FIS_Inhauser': {},
            'Erentrudisstr': {},
            'summary': {}
        }
    
    def analyze_csv_file(self, filepath, encoding='utf-8', sep=',', decimal='.'):
        """Analysiert eine CSV-Datei auf fehlende und fehlerhafte Daten"""
        try:
            # Versuche verschiedene Einlesemethoden
            try:
                df = pd.read_csv(filepath, encoding=encoding, sep=sep, decimal=decimal)
            except:
                df = pd.read_csv(filepath, encoding='iso-8859-1', sep=sep, decimal=decimal)
            
            analysis = {
                'file': os.path.basename(filepath),
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'missing_analysis': {},
                'error_analysis': {},
                'duplicates': {},
                'constant_values': {},
                'data_gaps': []
            }
            
            # Analysiere fehlende Werte pro Spalte
            for col in df.columns:
                missing_count = df[col].isnull().sum()
                missing_percent = (missing_count / len(df)) * 100
                
                if missing_count > 0:
                    # Finde Zeilen mit fehlenden Werten
                    missing_rows = df[df[col].isnull()].index.tolist()
                    
                    # Begrenzte Anzahl von Beispielen
                    example_rows = missing_rows[:10] if len(missing_rows) > 10 else missing_rows
                    
                    analysis['missing_analysis'][col] = {
                        'missing_count': int(missing_count),
                        'missing_percent': round(missing_percent, 2),
                        'total_rows_affected': len(missing_rows),
                        'example_rows': example_rows,
                        'pattern': self.detect_missing_pattern(df, col)
                    }
            
            # Prüfe auf Duplikate
            duplicates = df.duplicated()
            if duplicates.any():
                dup_count = duplicates.sum()
                dup_rows = df[duplicates].index.tolist()
                analysis['duplicates'] = {
                    'count': int(dup_count),
                    'rows': dup_rows[:10] if len(dup_rows) > 10 else dup_rows
                }
            
            # Prüfe auf konstante Werte (potenzielle Sensorfehler)
            for col in df.columns:
                if df[col].dtype in ['float64', 'int64']:
                    unique_values = df[col].dropna().unique()
                    if len(unique_values) == 1:
                        analysis['constant_values'][col] = {
                            'value': float(unique_values[0]),
                            'interpretation': 'Sensor möglicherweise defekt oder inaktiv'
                        }
                    elif len(unique_values) < 5:
                        value_counts = df[col].value_counts()
                        if value_counts.iloc[0] > len(df) * 0.95:
                            analysis['constant_values'][col] = {
                                'dominant_value': float(value_counts.index[0]),
                                'percent': round((value_counts.iloc[0] / len(df)) * 100, 2),
                                'interpretation': 'Wert fast immer konstant'
                            }
            
            # Prüfe auf Datenlücken in Zeitreihen
            if 'Datum + Uhrzeit' in df.columns or 'timestamp' in df.columns.str.lower():
                time_col = 'Datum + Uhrzeit' if 'Datum + Uhrzeit' in df.columns else [c for c in df.columns if 'timestamp' in c.lower()][0]
                analysis['data_gaps'] = self.detect_time_gaps(df, time_col)
            
            # Prüfe auf unplausible Werte
            for col in df.columns:
                if df[col].dtype in ['float64', 'int64']:
                    errors = self.detect_implausible_values(df, col)
                    if errors:
                        analysis['error_analysis'][col] = errors
            
            return analysis
            
        except Exception as e:
            return {'error': str(e), 'file': os.path.basename(filepath)}
    
    def detect_missing_pattern(self, df, column):
        """Erkennt Muster in fehlenden Daten"""
        missing_mask = df[column].isnull()
        if not missing_mask.any():
            return "Keine fehlenden Werte"
        
        # Prüfe auf zusammenhängende Blöcke
        missing_blocks = []
        in_block = False
        block_start = None
        
        for i, is_missing in enumerate(missing_mask):
            if is_missing and not in_block:
                in_block = True
                block_start = i
            elif not is_missing and in_block:
                in_block = False
                missing_blocks.append((block_start, i-1))
        
        if in_block:
            missing_blocks.append((block_start, len(df)-1))
        
        if len(missing_blocks) > 0:
            if len(missing_blocks) == 1:
                return f"Ein zusammenhängender Block: Zeilen {missing_blocks[0][0]}-{missing_blocks[0][1]}"
            elif len(missing_blocks) < 5:
                return f"{len(missing_blocks)} Blöcke fehlender Daten"
            else:
                return f"Verteilt über {len(missing_blocks)} Bereiche"
        
        return "Zufällig verteilt"
    
    def detect_time_gaps(self, df, time_column):
        """Erkennt zeitliche Lücken in Zeitreihen"""
        try:
            # Parse Zeitstempel
            df[time_column] = pd.to_datetime(df[time_column], errors='coerce')
            df = df.sort_values(time_column)
            
            # Berechne Zeitdifferenzen
            time_diffs = df[time_column].diff()
            
            # Bestimme normale Intervalle (häufigster Wert)
            normal_interval = time_diffs.mode()[0] if len(time_diffs.mode()) > 0 else pd.Timedelta(minutes=5)
            
            # Finde Lücken (> 2x normales Intervall)
            gaps = []
            threshold = normal_interval * 2
            
            for i, diff in enumerate(time_diffs):
                if pd.notna(diff) and diff > threshold:
                    gaps.append({
                        'start_row': i-1,
                        'end_row': i,
                        'start_time': str(df.iloc[i-1][time_column]),
                        'end_time': str(df.iloc[i][time_column]),
                        'gap_duration': str(diff),
                        'missing_intervals': int(diff / normal_interval)
                    })
            
            return gaps[:10] if len(gaps) > 10 else gaps
            
        except Exception:
            return []
    
    def detect_implausible_values(self, df, column):
        """Erkennt unplausible Werte basierend auf Spaltennamen"""
        col_lower = column.lower()
        errors = {}
        
        # Definiere plausible Bereiche basierend auf Spaltentyp
        if 'temperatur' in col_lower or 'temp' in col_lower:
            # Temperaturen sollten zwischen -50 und +100°C liegen
            invalid = df[(df[column] < -50) | (df[column] > 100)]
            if len(invalid) > 0:
                errors['out_of_range'] = {
                    'count': len(invalid),
                    'rows': invalid.index.tolist()[:10],
                    'values': invalid[column].tolist()[:10],
                    'expected_range': '-50 to 100°C'
                }
        
        elif 'leistung' in col_lower or 'power' in col_lower:
            # Negative Leistungen könnten auf Fehler hinweisen
            negative = df[df[column] < 0]
            if len(negative) > 0:
                errors['negative_values'] = {
                    'count': len(negative),
                    'rows': negative.index.tolist()[:10],
                    'interpretation': 'Negative Leistungswerte detektiert'
                }
        
        elif 'durchfluss' in col_lower or 'flow' in col_lower:
            # Durchfluss sollte nicht negativ sein
            negative = df[df[column] < 0]
            if len(negative) > 0:
                errors['negative_flow'] = {
                    'count': len(negative),
                    'rows': negative.index.tolist()[:10],
                    'interpretation': 'Negativer Durchfluss physikalisch nicht möglich'
                }
        
        # Prüfe auf Ausreißer (> 3 Standardabweichungen)
        if df[column].dtype in ['float64', 'int64']:
            mean = df[column].mean()
            std = df[column].std()
            if pd.notna(mean) and pd.notna(std) and std > 0:
                outliers = df[np.abs(df[column] - mean) > 3 * std]
                if len(outliers) > 0:
                    errors['statistical_outliers'] = {
                        'count': len(outliers),
                        'rows': outliers.index.tolist()[:10],
                        'values': outliers[column].tolist()[:10],
                        'mean': round(mean, 2),
                        'std': round(std, 2)
                    }
        
        return errors
    
    def analyze_fis_inhauser(self):
        """Analysiert FIS_Inhauser Daten"""
        print("Analysiere FIS_Inhauser Daten...")
        
        fis_path = os.path.join(self.base_path, 'Daten', 'Monitoringdaten', 'FIS_Inhauser', 'Monitoring')
        
        # Hauptdateien für Analyse
        files_to_analyze = [
            ('250101-250331/export_1551_2024-12-31-00-00_2025-03-31-23-55.csv', ',', '.'),
            ('250101-250331/test/export_1551_2025-01-01-00-00_2025-03-31-23-55.csv', ',', '.'),
            ('250101-250331/test/V1_2501_EXPORT_1.CSV', ';', ',')
        ]
        
        results = {}
        for file_path, sep, decimal in files_to_analyze:
            full_path = os.path.join(fis_path, file_path)
            if os.path.exists(full_path):
                print(f"  Analysiere: {file_path}")
                results[file_path] = self.analyze_csv_file(full_path, sep=sep, decimal=decimal)
        
        # Excel-Dateien
        excel_files = [
            '2024-2025-05_AT.xlsx',
            '250101-250331/test/250123-250129_ok_250130.xlsx'
        ]
        
        for excel_file in excel_files:
            full_path = os.path.join(fis_path, excel_file)
            if os.path.exists(full_path):
                print(f"  Analysiere Excel: {excel_file}")
                try:
                    xl = pd.ExcelFile(full_path)
                    for sheet in xl.sheet_names[:3]:  # Analysiere erste 3 Sheets
                        df = pd.read_excel(full_path, sheet_name=sheet)
                        temp_csv = f"/tmp/temp_{sheet}.csv"
                        df.to_csv(temp_csv, index=False)
                        sheet_result = self.analyze_csv_file(temp_csv)
                        sheet_result['sheet_name'] = sheet
                        results[f"{excel_file}_{sheet}"] = sheet_result
                        os.remove(temp_csv)
                except Exception as e:
                    results[excel_file] = {'error': str(e)}
        
        self.results['FIS_Inhauser'] = results
        return results
    
    def analyze_erentrudisstr(self):
        """Analysiert Erentrudisstr Daten"""
        print("Analysiere Erentrudisstr Daten...")
        
        eren_path = os.path.join(self.base_path, 'Daten', 'Monitoringdaten', 'Erentrudisstr', 'Monitoring')
        
        # Hauptdateien für Analyse
        files_to_analyze = [
            ('export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv', ';', ','),
            ('Vp.csv', ';', ','),
            ('2024/Relevant_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (2).csv', ';', ','),
            ('2024/Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv', ';', ','),
            ('2024/All_24-07_export_2011_2024-07-01-00-00_2024-07-31-23-59.csv', ';', ','),
            ('2024/Durchfluß/export_2011_2024-01-01-00-00_2024-12-31-23-59.csv', ';', ',')
        ]
        
        results = {}
        for file_path, sep, decimal in files_to_analyze:
            full_path = os.path.join(eren_path, file_path)
            if os.path.exists(full_path):
                print(f"  Analysiere: {file_path}")
                results[file_path] = self.analyze_csv_file(full_path, sep=sep, decimal=decimal)
        
        # Excel-Dateien
        excel_files = [
            '2024/Monitoring_ERS.xlsx',
            '2024/Monitoring_ERS_2024_V2_250506.xlsx',
            '2024/Monitoring_ERS_24-07_all.xlsx'
        ]
        
        for excel_file in excel_files:
            full_path = os.path.join(eren_path, excel_file)
            if os.path.exists(full_path):
                print(f"  Analysiere Excel: {excel_file}")
                try:
                    xl = pd.ExcelFile(full_path)
                    # Analysiere nur das erste Datensheet
                    for sheet in xl.sheet_names[:1]:
                        df = pd.read_excel(full_path, sheet_name=sheet)
                        temp_csv = f"/tmp/temp_{sheet}.csv"
                        df.to_csv(temp_csv, index=False)
                        sheet_result = self.analyze_csv_file(temp_csv)
                        sheet_result['sheet_name'] = sheet
                        results[f"{excel_file}_{sheet}"] = sheet_result
                        os.remove(temp_csv)
                except Exception as e:
                    results[excel_file] = {'error': str(e)}
        
        self.results['Erentrudisstr'] = results
        return results
    
    def generate_summary(self):
        """Generiert eine Zusammenfassung der Analyse"""
        summary = {
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'FIS_Inhauser': {
                'files_analyzed': len(self.results['FIS_Inhauser']),
                'total_missing_values': 0,
                'total_constant_sensors': 0,
                'total_data_gaps': 0,
                'critical_issues': []
            },
            'Erentrudisstr': {
                'files_analyzed': len(self.results['Erentrudisstr']),
                'total_missing_values': 0,
                'total_constant_sensors': 0,
                'total_data_gaps': 0,
                'critical_issues': []
            }
        }
        
        # Zusammenfassung für FIS_Inhauser
        for file_key, analysis in self.results['FIS_Inhauser'].items():
            if 'error' not in analysis:
                if 'missing_analysis' in analysis:
                    for col, missing_info in analysis['missing_analysis'].items():
                        summary['FIS_Inhauser']['total_missing_values'] += missing_info['missing_count']
                        if missing_info['missing_percent'] > 50:
                            summary['FIS_Inhauser']['critical_issues'].append({
                                'file': file_key,
                                'column': col,
                                'issue': f"{missing_info['missing_percent']}% fehlende Werte"
                            })
                
                if 'constant_values' in analysis:
                    summary['FIS_Inhauser']['total_constant_sensors'] += len(analysis['constant_values'])
                
                if 'data_gaps' in analysis:
                    summary['FIS_Inhauser']['total_data_gaps'] += len(analysis['data_gaps'])
        
        # Zusammenfassung für Erentrudisstr
        for file_key, analysis in self.results['Erentrudisstr'].items():
            if 'error' not in analysis:
                if 'missing_analysis' in analysis:
                    for col, missing_info in analysis['missing_analysis'].items():
                        summary['Erentrudisstr']['total_missing_values'] += missing_info['missing_count']
                        if missing_info['missing_percent'] > 50:
                            summary['Erentrudisstr']['critical_issues'].append({
                                'file': file_key,
                                'column': col,
                                'issue': f"{missing_info['missing_percent']}% fehlende Werte"
                            })
                
                if 'constant_values' in analysis:
                    summary['Erentrudisstr']['total_constant_sensors'] += len(analysis['constant_values'])
                
                if 'data_gaps' in analysis:
                    summary['Erentrudisstr']['total_data_gaps'] += len(analysis['data_gaps'])
        
        self.results['summary'] = summary
        return summary
    
    def save_results(self):
        """Speichert die Analyseergebnisse"""
        output_path = os.path.join(self.base_path, 'scripts', 'missing_data_analysis_results.json')
        
        # Konvertiere für JSON-Serialisierung
        def convert_for_json(obj):
            if isinstance(obj, (np.integer, np.int64)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif pd.isna(obj):
                return None
            return obj
        
        # Rekursive Konvertierung
        def clean_dict(d):
            if isinstance(d, dict):
                return {k: clean_dict(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [clean_dict(item) for item in d]
            else:
                return convert_for_json(d)
        
        clean_results = clean_dict(self.results)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clean_results, f, indent=2, ensure_ascii=False)
        
        print(f"Ergebnisse gespeichert unter: {output_path}")
        return output_path

def main():
    base_path = '/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025'
    
    analyzer = MissingDataAnalyzer(base_path)
    
    # Analysiere beide Standorte
    analyzer.analyze_fis_inhauser()
    analyzer.analyze_erentrudisstr()
    
    # Generiere Zusammenfassung
    summary = analyzer.generate_summary()
    
    # Speichere Ergebnisse
    output_file = analyzer.save_results()
    
    print("\n=== ANALYSE ABGESCHLOSSEN ===")
    print(f"\nFIS_Inhauser:")
    print(f"  - Dateien analysiert: {summary['FIS_Inhauser']['files_analyzed']}")
    print(f"  - Fehlende Werte gesamt: {summary['FIS_Inhauser']['total_missing_values']}")
    print(f"  - Konstante Sensoren: {summary['FIS_Inhauser']['total_constant_sensors']}")
    print(f"  - Datenlücken: {summary['FIS_Inhauser']['total_data_gaps']}")
    print(f"  - Kritische Probleme: {len(summary['FIS_Inhauser']['critical_issues'])}")
    
    print(f"\nErentrudisstr:")
    print(f"  - Dateien analysiert: {summary['Erentrudisstr']['files_analyzed']}")
    print(f"  - Fehlende Werte gesamt: {summary['Erentrudisstr']['total_missing_values']}")
    print(f"  - Konstante Sensoren: {summary['Erentrudisstr']['total_constant_sensors']}")
    print(f"  - Datenlücken: {summary['Erentrudisstr']['total_data_gaps']}")
    print(f"  - Kritische Probleme: {len(summary['Erentrudisstr']['critical_issues'])}")
    
    return analyzer.results

if __name__ == "__main__":
    main()