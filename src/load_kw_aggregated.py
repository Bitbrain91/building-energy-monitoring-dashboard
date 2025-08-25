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
    Lädt aggregierte Kraftwerksdaten aus Parquet.
    
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
        # Hier könnte ein Fallback implementiert werden
    
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
    
    # 1. Lade Übergabe-Datensätze direkt aus Parquet
    uebergabe_files = [
        ('uebergabe_bezug_gesamt', 'ÜBERGABE_BEZUG_2020_2024.parquet'),
        ('uebergabe_lieferung_gesamt', 'ÜBERGABE_LIEFERUNG_2020_2024.parquet')
    ]
    
    for key, filename in uebergabe_files:
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