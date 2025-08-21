#!/usr/bin/env python3
"""
Analyse der Monitoringdaten Erentrudisstraße
Erstellt: 2025-08-20
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Basis-Pfad für Monitoringdaten
BASE_PATH = '/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025/Daten/Monitoringdaten/Erentrudisstr/Monitoring'

def analyze_csv_file(filepath, filename):
    """Analysiert eine CSV-Datei und gibt Statistiken zurück"""
    try:
        # Versuche verschiedene Encodings
        for encoding in ['utf-8', 'iso-8859-1', 'cp1252']:
            try:
                df = pd.read_csv(filepath, encoding=encoding, sep=None, engine='python')
                break
            except:
                continue
        
        analysis = {
            'filename': filename,
            'filepath': filepath,
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'missing_percentage': (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # in MB
            'date_range': None,
            'temporal_resolution': None,
            'description': []
        }
        
        # Versuche Zeitstempel zu identifizieren
        for col in df.columns:
            if 'time' in col.lower() or 'date' in col.lower() or 'zeit' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                    if df[col].dtype == 'datetime64[ns]':
                        analysis['date_range'] = f"{df[col].min()} bis {df[col].max()}"
                        # Berechne zeitliche Auflösung
                        if len(df) > 1:
                            time_diffs = df[col].diff().dropna()
                            most_common = time_diffs.value_counts().head(1)
                            if not most_common.empty:
                                analysis['temporal_resolution'] = str(most_common.index[0])
                        break
                except:
                    pass
        
        # Identifiziere Inhalt basierend auf Spaltennamen
        col_lower = [c.lower() for c in df.columns]
        if any('temperatur' in c or 'temp' in c for c in col_lower):
            analysis['description'].append('Temperaturdaten')
        if any('flow' in c or 'durchfluss' in c or 'durchfluß' in c for c in col_lower):
            analysis['description'].append('Durchflussdaten')
        if any('power' in c or 'leistung' in c for c in col_lower):
            analysis['description'].append('Leistungsdaten')
        if any('energie' in c or 'energy' in c for c in col_lower):
            analysis['description'].append('Energiedaten')
        if any('druck' in c or 'pressure' in c for c in col_lower):
            analysis['description'].append('Druckdaten')
        
        # Numerische Statistiken für die ersten 5 numerischen Spalten
        numeric_cols = df.select_dtypes(include=[np.number]).columns[:5]
        if len(numeric_cols) > 0:
            analysis['numeric_stats'] = {}
            for col in numeric_cols:
                analysis['numeric_stats'][col] = {
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'mean': df[col].mean(),
                    'std': df[col].std(),
                    'median': df[col].median()
                }
        
        return analysis
        
    except Exception as e:
        return {
            'filename': filename,
            'filepath': filepath,
            'error': str(e),
            'readable': False
        }

def analyze_excel_file(filepath, filename):
    """Analysiert eine Excel-Datei und gibt Statistiken zurück"""
    try:
        # Lade Excel-Datei
        xl_file = pd.ExcelFile(filepath)
        
        analysis = {
            'filename': filename,
            'filepath': filepath,
            'sheet_names': xl_file.sheet_names,
            'num_sheets': len(xl_file.sheet_names),
            'sheets_analysis': {},
            'description': []
        }
        
        # Analysiere jedes Sheet
        for sheet_name in xl_file.sheet_names[:5]:  # Maximal 5 Sheets analysieren
            try:
                df = pd.read_excel(filepath, sheet_name=sheet_name)
                
                sheet_analysis = {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': list(df.columns)[:20],  # Erste 20 Spalten
                    'missing_percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100) if len(df) > 0 else 0
                }
                
                # Identifiziere Inhalt
                col_lower = [str(c).lower() for c in df.columns]
                content_types = []
                if any('temperatur' in c or 'temp' in c for c in col_lower):
                    content_types.append('Temperaturdaten')
                if any('flow' in c or 'durchfluss' in c or 'durchfluß' in c for c in col_lower):
                    content_types.append('Durchflussdaten')
                if any('power' in c or 'leistung' in c for c in col_lower):
                    content_types.append('Leistungsdaten')
                
                sheet_analysis['content_types'] = content_types
                analysis['sheets_analysis'][sheet_name] = sheet_analysis
                
            except Exception as e:
                analysis['sheets_analysis'][sheet_name] = {'error': str(e)}
        
        return analysis
        
    except Exception as e:
        return {
            'filename': filename,
            'filepath': filepath,
            'error': str(e),
            'readable': False
        }

def main():
    """Hauptfunktion zur Analyse aller Monitoringdaten"""
    
    print("=" * 80)
    print("ANALYSE DER MONITORINGDATEN ERENTRUDISSTRASSE")
    print("=" * 80)
    print(f"Analysezeitpunkt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Basis-Pfad: {BASE_PATH}")
    print()
    
    # Sammle alle Dateien
    all_files = []
    csv_files = []
    excel_files = []
    
    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, BASE_PATH)
            
            if file.endswith('.csv'):
                csv_files.append((filepath, file, rel_path))
            elif file.endswith(('.xlsx', '.xls')):
                excel_files.append((filepath, file, rel_path))
            
            all_files.append((filepath, file, rel_path))
    
    print(f"Gefundene Dateien:")
    print(f"- CSV-Dateien: {len(csv_files)}")
    print(f"- Excel-Dateien: {len(excel_files)}")
    print(f"- Andere Dateien: {len(all_files) - len(csv_files) - len(excel_files)}")
    print()
    
    # Analysiere CSV-Dateien
    print("=" * 80)
    print("ANALYSE DER CSV-DATEIEN")
    print("=" * 80)
    
    csv_analyses = []
    for filepath, filename, rel_path in csv_files:
        print(f"\nAnalysiere: {rel_path}")
        analysis = analyze_csv_file(filepath, filename)
        csv_analyses.append(analysis)
        
        if 'error' not in analysis:
            print(f"  - Zeilen: {analysis['rows']:,}")
            print(f"  - Spalten: {analysis['columns']}")
            if analysis['date_range']:
                print(f"  - Zeitraum: {analysis['date_range']}")
            if analysis['temporal_resolution']:
                print(f"  - Zeitliche Auflösung: {analysis['temporal_resolution']}")
            if analysis['description']:
                print(f"  - Inhalt: {', '.join(analysis['description'])}")
            print(f"  - Fehlende Werte: {sum(analysis['missing_values'].values()):,}")
        else:
            print(f"  - FEHLER: {analysis['error']}")
    
    # Analysiere Excel-Dateien
    print("\n" + "=" * 80)
    print("ANALYSE DER EXCEL-DATEIEN")
    print("=" * 80)
    
    excel_analyses = []
    for filepath, filename, rel_path in excel_files:
        print(f"\nAnalysiere: {rel_path}")
        analysis = analyze_excel_file(filepath, filename)
        excel_analyses.append(analysis)
        
        if 'error' not in analysis:
            print(f"  - Anzahl Sheets: {analysis['num_sheets']}")
            print(f"  - Sheet-Namen: {', '.join(analysis['sheet_names'][:3])}")
            for sheet_name, sheet_data in list(analysis['sheets_analysis'].items())[:3]:
                if 'error' not in sheet_data:
                    print(f"  - Sheet '{sheet_name}': {sheet_data['rows']} Zeilen, {sheet_data['columns']} Spalten")
                    if sheet_data.get('content_types'):
                        print(f"    Inhalt: {', '.join(sheet_data['content_types'])}")
        else:
            print(f"  - FEHLER: {analysis['error']}")
    
    # Zusammenfassung
    print("\n" + "=" * 80)
    print("ZUSAMMENFASSUNG")
    print("=" * 80)
    
    # Berechne Gesamtstatistiken
    total_rows = sum(a.get('rows', 0) for a in csv_analyses if 'error' not in a)
    total_columns = sum(a.get('columns', 0) for a in csv_analyses if 'error' not in a)
    
    print(f"\nDatenumfang:")
    print(f"- Gesamtanzahl Datenpunkte (CSV): ~{total_rows:,} Zeilen")
    print(f"- Durchschnittliche Spaltenanzahl (CSV): {total_columns/len(csv_files):.1f}" if csv_files else "")
    
    # Identifizierte Datentypen
    all_descriptions = []
    for a in csv_analyses:
        if 'description' in a:
            all_descriptions.extend(a['description'])
    
    if all_descriptions:
        print(f"\nIdentifizierte Datentypen:")
        for dtype in set(all_descriptions):
            count = all_descriptions.count(dtype)
            print(f"- {dtype}: {count} Datei(en)")
    
    # Zeitliche Abdeckung
    print(f"\nZeitliche Abdeckung:")
    for a in csv_analyses:
        if 'date_range' in a and a['date_range']:
            print(f"- {a['filename']}: {a['date_range']}")
    
    return csv_analyses, excel_analyses

if __name__ == "__main__":
    csv_analyses, excel_analyses = main()