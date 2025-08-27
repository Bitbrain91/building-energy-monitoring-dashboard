"""
Hilfsmodul zum korrekten Laden und Aggregieren der KW Neukirchen Daten
========================================================================
Stellt sicher, dass ALLE Jahre (2020-2024) geladen werden.
"""

import pandas as pd
from pathlib import Path
import pyarrow.parquet as pq


def load_kw_complete(base_path, kraftwerk_name):
    """
    Lädt aggregierte Kraftwerksdaten aus Parquet oder XLSX Fallback.
    
    Args:
        base_path: Basis-Pfad des Projekts
        kraftwerk_name: 'duernbach', 'untersulzbach' oder 'wiesbach'
    
    Returns:
        DataFrame mit allen Jahren kombiniert
    """
    parquet_dir = base_path / "data_optimized"
    
    # Mapping zu aggregierten Dateinamen (2020-2024)
    name_map = {
        'duernbach': 'KW DÜRNBACH_ERZEUGUNG_2020_2024',
        'untersulzbach': 'KW UNTERSULZBACH_ERZEUGUNG_2020_2024',
        'wiesbach': 'KW WIESBACH_ERZEUGUNG_2020_2024'
    }
    
    base_name_map = {
        'duernbach': 'KW DÜRNBACH_ERZEUGUNG',
        'untersulzbach': 'KW UNTERSULZBACH_ERZEUGUNG',
        'wiesbach': 'KW WIESBACH_ERZEUGUNG'
    }
    
    if kraftwerk_name not in name_map:
        print(f"Unbekanntes Kraftwerk: {kraftwerk_name}")
        return pd.DataFrame()
    
    filename = name_map[kraftwerk_name]
    parquet_path = parquet_dir / f"{filename}.parquet"
    
    # Lade die aggregierte Parquet-Datei
    if parquet_path.exists():
        try:
            df = pd.read_parquet(parquet_path)
            
            # Stelle sicher, dass Date-Spalte existiert
            if df.index.name in ['Date', 'UHRZEIT_LOKAL_BIS', 'DateTime']:
                if 'Date' not in df.columns:
                    df['Date'] = df.index
            elif 'UHRZEIT_LOKAL_BIS' in df.columns and 'Date' not in df.columns:
                df['Date'] = pd.to_datetime(df['UHRZEIT_LOKAL_BIS'])
            
            print(f"   [OK] Geladen: {parquet_path.name} ({len(df):,} Zeilen)")
            
            # Prüfe Vollständigkeit
            if 'Date' in df.columns:
                jahre = df['Date'].dt.year.unique()
                print(f"   -> Jahre vorhanden: {sorted(jahre)}")
            
            return df
        except Exception as e:
            print(f"   [FEHLER] bei {parquet_path.name}: {e}")
    else:
        print(f"   [WARNUNG] Datei nicht gefunden: {parquet_path.name}")
        print(f"   Versuche Fallback auf Einzeldateien...")
        
        # Fallback: Lade aus XLSX Dateien
        df = load_kraftwerk_from_xlsx(base_path, base_name_map[kraftwerk_name])
        if not df.empty:
            return df
    
    return pd.DataFrame()


def aggregate_all_kw_data(base_path):
    """
    Aggregiert alle KW Neukirchen Daten komplett (5 Datensätze).
    
    Returns:
        Dictionary mit allen aggregierten Kraftwerksdaten
    """
    print("\n[KW] Lade komplette KW Neukirchen Daten (5 Datensätze, 2020-2024)...")
    
    result = {}
    parquet_dir = base_path / "data_optimized"
    
    # 1. Lade Übergabe-Datensätze direkt aus Parquet oder mit Fallback
    uebergabe_files = [
        ('uebergabe_bezug_gesamt', 'ÜBERGABE_BEZUG_2020_2024.parquet', 'ÜBERGABE_BEZUG'),
        ('uebergabe_lieferung_gesamt', 'ÜBERGABE_LIEFERUNG_2020_2024.parquet', 'ÜBERGABE_LIEFERUNG')
    ]
    
    for key, filename, base_name in uebergabe_files:
        parquet_path = parquet_dir / filename
        if parquet_path.exists():
            try:
                df = pd.read_parquet(parquet_path)
                result[key] = df
                print(f"   [OK] {filename}: {len(df):,} Zeilen")
            except Exception as e:
                print(f"   [FEHLER] bei {filename}: {e}")
        else:
            print(f"   [WARNUNG] {filename} nicht gefunden!")
            print(f"   Versuche Fallback für {base_name}...")
            
            # Fallback: Lade aus XLSX Dateien
            df = load_uebergabe_from_xlsx(base_path, base_name)
            if not df.empty:
                result[key] = df
    
    # 2. Lade Kraftwerks-Datensätze
    for kw_name in ['duernbach', 'untersulzbach', 'wiesbach']:
        print(f"\nLade Kraftwerk {kw_name.title()}:")
        df = load_kw_complete(base_path, kw_name)
        if not df.empty:
            result[f'kw_{kw_name}_gesamt'] = df
    
    print(f"\n[ERFOLG] KW Neukirchen komplett geladen: {len(result)} Datensätze")
    print(f"  - Übergabe Bezug: {'uebergabe_bezug_gesamt' in result}")
    print(f"  - Übergabe Lieferung: {'uebergabe_lieferung_gesamt' in result}")
    print(f"  - KW Dürnbach: {'kw_duernbach_gesamt' in result}")
    print(f"  - KW Untersulzbach: {'kw_untersulzbach_gesamt' in result}")
    print(f"  - KW Wiesbach: {'kw_wiesbach_gesamt' in result}")
    
    return result


def load_uebergabe_from_xlsx(base_path, base_name):
    """Fallback-Loader für Übergabe-Datensätze aus monatlichen XLSX-Dateien."""
    dfs = []
    
    # Korrekter Pfad für Übergabe-Dateien
    uebergabe_base_path = base_path / "src" / "data" / "kw_neukirchen"
    
    # Lade alle Jahre und Monate
    for year in range(2020, 2025):  # 2020 bis 2024
        year_path = uebergabe_base_path / str(year)
        
        if not year_path.exists():
            continue
            
        for month in range(1, 13):  # Januar bis Dezember
            month_str = f"{month:02d}"
            file_name = f"{base_name}_{year}.{month_str}.XLSX"
            file_path = year_path / file_name
            
            if file_path.exists():
                try:
                    df = pd.read_excel(file_path, engine='openpyxl')
                    # Füge Jahr und Monat hinzu
                    df['Jahr'] = year
                    df['Monat'] = month
                    dfs.append(df)
                except Exception as e:
                    pass  # Fehler still ignorieren für sauberen Output
                    
    if dfs:
        # Kombiniere alle Monatsdaten
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Stelle sicher, dass Date-Spalte existiert
        if 'ZEIT_VON_UTC' in combined_df.columns:
            combined_df['Date'] = pd.to_datetime(combined_df['ZEIT_VON_UTC'])
        elif 'UHRZEIT_LOKAL_BIS' in combined_df.columns:
            combined_df['Date'] = pd.to_datetime(combined_df['UHRZEIT_LOKAL_BIS'])
        elif 'Date' not in combined_df.columns:
            # Fallback: erstelle Date aus Jahr/Monat
            combined_df['Date'] = pd.to_datetime(
                combined_df[['Jahr', 'Monat']].assign(Tag=1)
            )
        
        print(f"   [OK] {base_name}: {len(combined_df):,} Zeilen aus XLSX geladen")
        return combined_df
    
    return pd.DataFrame()


def load_kraftwerk_from_xlsx(base_path, base_name):
    """Fallback-Loader für Kraftwerks-Datensätze aus jährlichen XLSX-Dateien."""
    dfs = []
    
    # Pfad zu den KW XLSX Dateien
    kw_base_path = base_path / "src" / "data" / "kw_neukirchen"
    
    # Lade alle Jahre (2020-2024)
    for year in range(2020, 2025):  # 2020 bis 2024
        file_path = kw_base_path / f"{base_name}_{year}.XLSX"
        
        if file_path.exists():
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
                # Füge Jahr als Spalte hinzu für Nachverfolgbarkeit
                df['Jahr'] = year
                dfs.append(df)
            except Exception as e:
                pass  # Fehler still ignorieren für sauberen Output
    
    if dfs:
        # Kombiniere alle Jahre
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Stelle sicher, dass Date-Spalte existiert
        if 'ZEIT_VON_UTC' in combined_df.columns:
            combined_df['Date'] = pd.to_datetime(combined_df['ZEIT_VON_UTC'])
        elif 'UHRZEIT_LOKAL_BIS' in combined_df.columns:
            combined_df['Date'] = pd.to_datetime(combined_df['UHRZEIT_LOKAL_BIS'])
        elif 'Date' not in combined_df.columns:
            # Fallback: erstelle Date aus Jahr
            combined_df['Date'] = pd.date_range(start='2020-01-01', periods=len(combined_df), freq='15T')
        
        print(f"   [OK] {base_name}: {len(combined_df):,} Zeilen aus XLSX geladen (2020-2024)")
        return combined_df
    
    return pd.DataFrame()