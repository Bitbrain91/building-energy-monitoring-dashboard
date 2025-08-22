"""
Konvertiert FIS_Inhauser Excel-Datei zu CSV im selben Ordner
und prüft die Vollständigkeit der Datenübernahme
"""
import pandas as pd
from pathlib import Path
import numpy as np

# Pfade definieren
base_path = Path(__file__).parent.parent
monitoring_path = base_path / "Daten" / "Monitoringdaten" / "FIS_Inhauser" / "Monitoring"
excel_file = monitoring_path / "2024-2025-05_AT.xlsx"
csv_file = monitoring_path / "2024-2025-05_AT.csv"

print("="*60)
print("FIS_Inhauser Excel zu CSV Konvertierung")
print("="*60)
print(f"Quell-Datei: {excel_file}")
print(f"Ziel-Datei:  {csv_file}")
print("-"*60)

try:
    # Excel-Datei einlesen
    print("\n1. Lese Excel-Datei...")
    df_excel = pd.read_excel(excel_file, engine='openpyxl')
    
    # Informationen über Excel-Daten
    print(f"   ✓ Excel geladen: {len(df_excel)} Zeilen, {len(df_excel.columns)} Spalten")
    print(f"   ✓ Spalten: {', '.join(df_excel.columns.tolist())}")
    
    # Prüfe auf leere Werte
    null_counts = df_excel.isnull().sum()
    if null_counts.sum() > 0:
        print(f"\n   ⚠ Leere Werte gefunden:")
        for col, count in null_counts[null_counts > 0].items():
            print(f"      - {col}: {count} leere Werte")
    
    # Datentypen prüfen
    print(f"\n2. Datentypen:")
    for col in df_excel.columns:
        dtype = df_excel[col].dtype
        non_null = df_excel[col].notna().sum()
        print(f"   - {col}: {dtype} ({non_null} gültige Werte)")
    
    # Als CSV speichern
    print(f"\n3. Speichere als CSV...")
    df_excel.to_csv(csv_file, index=False, encoding='utf-8')
    print(f"   ✓ CSV gespeichert: {csv_file}")
    
    # CSV wieder einlesen zur Verifikation
    print(f"\n4. Verifiziere CSV...")
    df_csv = pd.read_csv(csv_file, encoding='utf-8')
    print(f"   ✓ CSV geladen: {len(df_csv)} Zeilen, {len(df_csv.columns)} Spalten")
    
    # Vergleiche Excel und CSV
    print(f"\n5. Datenvergleich Excel vs CSV:")
    if len(df_excel) == len(df_csv):
        print(f"   ✓ Zeilenanzahl stimmt überein: {len(df_excel)}")
    else:
        print(f"   ✗ FEHLER: Unterschiedliche Zeilenanzahl!")
        print(f"     Excel: {len(df_excel)}, CSV: {len(df_csv)}")
    
    if len(df_excel.columns) == len(df_csv.columns):
        print(f"   ✓ Spaltenanzahl stimmt überein: {len(df_excel.columns)}")
    else:
        print(f"   ✗ FEHLER: Unterschiedliche Spaltenanzahl!")
    
    # Wertebereich prüfen (für numerische Spalten)
    print(f"\n6. Wertebereich-Analyse:")
    for col in df_excel.columns:
        if col in df_csv.columns:
            # Versuche numerische Analyse
            try:
                if pd.api.types.is_numeric_dtype(df_excel[col]):
                    excel_min = df_excel[col].min()
                    excel_max = df_excel[col].max()
                    excel_mean = df_excel[col].mean()
                    
                    csv_min = pd.to_numeric(df_csv[col], errors='coerce').min()
                    csv_max = pd.to_numeric(df_csv[col], errors='coerce').max()
                    csv_mean = pd.to_numeric(df_csv[col], errors='coerce').mean()
                    
                    print(f"\n   {col}:")
                    print(f"     Excel: Min={excel_min:.2f}, Max={excel_max:.2f}, Mittel={excel_mean:.2f}")
                    print(f"     CSV:   Min={csv_min:.2f}, Max={csv_max:.2f}, Mittel={csv_mean:.2f}")
                    
                    # Prüfe auf Abweichungen
                    if abs(excel_mean - csv_mean) > 0.01:
                        print(f"     ⚠ Warnung: Mittelwert-Abweichung > 0.01")
            except:
                pass  # Nicht-numerische Spalte
    
    # Stichproben-Vergleich
    print(f"\n7. Stichproben-Vergleich (erste 5 Zeilen):")
    print("\nExcel:")
    print(df_excel.head())
    print("\nCSV:")
    print(df_csv.head())
    
    # Zusammenfassung
    print("\n" + "="*60)
    print("ZUSAMMENFASSUNG:")
    print("="*60)
    print(f"✓ Konvertierung erfolgreich abgeschlossen")
    print(f"✓ {len(df_csv)} Datensätze in CSV gespeichert")
    print(f"✓ Datei gespeichert unter: {csv_file}")
    
    # Alte CSV in docs löschen (falls vorhanden)
    old_csv = base_path / "docs" / "FIS_Inhauser_2024-2025-05_AT.csv"
    if old_csv.exists():
        old_csv.unlink()
        print(f"✓ Alte CSV in docs/ gelöscht")
    
except Exception as e:
    print(f"\n✗ FEHLER bei der Konvertierung: {e}")
    import traceback
    traceback.print_exc()