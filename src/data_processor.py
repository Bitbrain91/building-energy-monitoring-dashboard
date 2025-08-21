"""
Datenverarbeitungsmodul für Twin2Sim Dashboard
Stellt Funktionen zur Datenaufbereitung und -analyse bereit
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

class DataProcessor:
    """Klasse zur Verarbeitung der Twin2Sim Daten"""
    
    def __init__(self, data_path):
        self.data_path = Path(data_path)
        self.data = {}
        
    def load_all_data(self):
        """Lädt alle verfügbaren CSV-Dateien"""
        files = {
            'pv_int': 'T2S_IntPV.csv',
            'pv_mani': 'T2S_ManiPV.csv',
            'ventilation': 'T2S_Lüftung.csv',
            'room': 'T2S_RAU006.csv',
            'weather': 'T2S_Wetterdaten.csv'
        }
        
        for key, filename in files.items():
            file_path = self.data_path / filename
            if file_path.exists():
                try:
                    df = pd.read_csv(file_path, sep=';', decimal=',')
                    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y %H:%M:%S,%f')
                    self.data[key] = df
                    print(f"✓ Geladen: {filename} ({len(df)} Zeilen)")
                except Exception as e:
                    print(f"✗ Fehler beim Laden von {filename}: {e}")
                    self.data[key] = pd.DataFrame()
            else:
                print(f"✗ Datei nicht gefunden: {filename}")
                self.data[key] = pd.DataFrame()
        
        return self.data
    
    def calculate_statistics(self):
        """Berechnet statistische Kennzahlen für alle Datenquellen"""
        stats = {}
        
        for name, df in self.data.items():
            if not df.empty:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                
                stats[name] = {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'date_range': f"{df['Date'].min()} bis {df['Date'].max()}",
                    'numeric_columns': len(numeric_cols),
                    'missing_values': df[numeric_cols].isnull().sum().sum(),
                    'completeness': f"{(1 - df[numeric_cols].isnull().sum().sum() / (len(df) * len(numeric_cols))) * 100:.1f}%"
                }
        
        return stats
    
    def get_pv_metrics(self):
        """Berechnet PV-spezifische Metriken"""
        metrics = {}
        
        if 'pv_int' in self.data and not self.data['pv_int'].empty:
            df = self.data['pv_int']
            
            # Growatt Metriken
            metrics['growatt'] = {
                'max_power': df['Growatt_MIC_600TL_X_0.read_output_power'].max(),
                'total_energy': df['Growatt_MIC_600TL_X_0.read_total_generate_energy'].max(),
                'today_energy': df['Growatt_MIC_600TL_X_0.read_today_generate_energy'].max(),
                'avg_efficiency': (df['Growatt_MIC_600TL_X_0.read_output_power'] / 
                                  df['Growatt_MIC_600TL_X_0.read_input_power'].replace(0, np.nan)).mean() * 100,
                'operating_hours': df['Growatt_MIC_600TL_X_0.read_work_time_total'].max(),
                'avg_temperature': df['Growatt_MIC_600TL_X_0.read_inverter_temperature'].mean()
            }
        
        if 'pv_mani' in self.data and not self.data['pv_mani'].empty:
            df = self.data['pv_mani']
            
            # Manipulation PV Metriken
            metrics['manipulation'] = {
                'max_power': df['PV_WR.read_akt_ges_P'].max() if 'PV_WR.read_akt_ges_P' in df.columns else 0,
                'total_energy': df['PV_WR.read_total_ges_E'].max() if 'PV_WR.read_total_ges_E' in df.columns else 0,
                'year_energy': df['PV_WR.read_jahr_ges_E'].max() if 'PV_WR.read_jahr_ges_E' in df.columns else 0
            }
        
        return metrics
    
    def get_climate_metrics(self):
        """Berechnet Klima-Metriken"""
        metrics = {}
        
        if 'room' in self.data and not self.data['room'].empty:
            df = self.data['room']
            
            metrics['room'] = {
                'avg_temperature': df['RAU006.ERR_TE_MW'].mean() if 'RAU006.ERR_TE_MW' in df.columns else 0,
                'avg_humidity': df['RAU006.ERR_FE_MW'].mean() if 'RAU006.ERR_FE_MW' in df.columns else 0,
                'avg_co2': df['RAU006.ABL_LQ.MS'].mean() if 'RAU006.ABL_LQ.MS' in df.columns else 0,
                'temp_range': (df['RAU006.ERR_TE_MW'].min(), df['RAU006.ERR_TE_MW'].max()) if 'RAU006.ERR_TE_MW' in df.columns else (0, 0)
            }
        
        if 'weather' in self.data and not self.data['weather'].empty:
            df = self.data['weather']
            
            metrics['weather'] = {
                'avg_temperature': df['MSR02_WST_ALLG.akt_Lufttemperatur'].mean() if 'MSR02_WST_ALLG.akt_Lufttemperatur' in df.columns else 0,
                'avg_humidity': df['MSR02_WST_ALLG.akt_rel_LuftFeuchte'].mean() if 'MSR02_WST_ALLG.akt_rel_LuftFeuchte' in df.columns else 0,
                'avg_pressure': df['MSR02_WST_ALLG.akt_abs_LuftDruck'].mean() if 'MSR02_WST_ALLG.akt_abs_LuftDruck' in df.columns else 0,
                'max_radiation': df['MSR02_WST_ALLG.akt_Globalstrahlung'].max() if 'MSR02_WST_ALLG.akt_Globalstrahlung' in df.columns else 0,
                'avg_wind_speed': df['MSR02_WST_ALLG.akt_Windgeschwindigkeit'].mean() if 'MSR02_WST_ALLG.akt_Windgeschwindigkeit' in df.columns else 0
            }
        
        return metrics
    
    def get_ventilation_metrics(self):
        """Berechnet Lüftungsanlagen-Metriken"""
        metrics = {}
        
        if 'ventilation' in self.data and not self.data['ventilation'].empty:
            df = self.data['ventilation']
            
            # Identifiziere relevante Spalten
            supply_fan_col = 'RLT001.ZVE.MO.Value' if 'RLT001.ZVE.MO.Value' in df.columns else None
            exhaust_fan_col = 'RLT001.FVE.MO.Value' if 'RLT001.FVE.MO.Value' in df.columns else None
            
            metrics = {
                'avg_supply_fan': df[supply_fan_col].mean() if supply_fan_col else 0,
                'avg_exhaust_fan': df[exhaust_fan_col].mean() if exhaust_fan_col else 0,
                'operating_hours': len(df[df[supply_fan_col] > 0]) if supply_fan_col else 0,
                'night_reduction': len(df[(df[supply_fan_col] == 0) & (df['Date'].dt.hour.between(0, 6))]) if supply_fan_col and 'Date' in df.columns else 0
            }
        
        return metrics
    
    def check_data_quality(self):
        """Prüft die Datenqualität und identifiziert Probleme"""
        issues = []
        
        for name, df in self.data.items():
            if df.empty:
                issues.append(f"⚠ {name}: Keine Daten vorhanden")
                continue
            
            # Prüfe auf fehlende Werte
            missing = df.isnull().sum()
            if missing.any():
                cols_with_missing = missing[missing > 0]
                for col, count in cols_with_missing.items():
                    if count > len(df) * 0.1:  # Mehr als 10% fehlend
                        issues.append(f"⚠ {name}.{col}: {count} fehlende Werte ({count/len(df)*100:.1f}%)")
            
            # Prüfe auf Zeitlücken
            if 'Date' in df.columns:
                time_diff = df['Date'].diff()
                expected_interval = pd.Timedelta(hours=1)
                gaps = time_diff[time_diff > expected_interval * 1.5]
                if not gaps.empty:
                    issues.append(f"⚠ {name}: {len(gaps)} Zeitlücken gefunden")
        
        return issues
    
    def export_summary(self, output_path=None):
        """Exportiert eine Zusammenfassung der Datenanalyse"""
        if output_path is None:
            output_path = self.data_path.parent / 'data_summary.xlsx'
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Statistiken
            stats_df = pd.DataFrame(self.calculate_statistics()).T
            stats_df.to_excel(writer, sheet_name='Statistiken')
            
            # PV Metriken
            pv_metrics = self.get_pv_metrics()
            if pv_metrics:
                pv_df = pd.DataFrame(pv_metrics).T
                pv_df.to_excel(writer, sheet_name='PV Metriken')
            
            # Klima Metriken
            climate_metrics = self.get_climate_metrics()
            if climate_metrics:
                climate_df = pd.DataFrame(climate_metrics).T
                climate_df.to_excel(writer, sheet_name='Klima Metriken')
            
            # Lüftung Metriken
            vent_metrics = self.get_ventilation_metrics()
            if vent_metrics:
                vent_df = pd.DataFrame([vent_metrics])
                vent_df.to_excel(writer, sheet_name='Lüftung Metriken')
            
            # Datenqualität
            issues = self.check_data_quality()
            if issues:
                issues_df = pd.DataFrame({'Probleme': issues})
                issues_df.to_excel(writer, sheet_name='Datenqualität', index=False)
        
        print(f"✓ Zusammenfassung exportiert nach: {output_path}")
        return output_path

if __name__ == "__main__":
    # Test der Datenverarbeitung
    processor = DataProcessor("../Daten/Beispieldaten")
    processor.load_all_data()
    
    print("\n=== Statistiken ===")
    stats = processor.calculate_statistics()
    for name, stat in stats.items():
        print(f"\n{name}:")
        for key, value in stat.items():
            print(f"  {key}: {value}")
    
    print("\n=== PV Metriken ===")
    pv_metrics = processor.get_pv_metrics()
    for system, metrics in pv_metrics.items():
        print(f"\n{system}:")
        for key, value in metrics.items():
            print(f"  {key}: {value:.2f}" if isinstance(value, (int, float)) else f"  {key}: {value}")
    
    print("\n=== Datenqualität ===")
    issues = processor.check_data_quality()
    for issue in issues:
        print(issue)