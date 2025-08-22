# Erentrudisstraße - Dokumentation

## 🏠 Übersicht

Monitoring-Daten für das Gebäude Erentrudisstraße 19, Salzburg. Umfassende Gebäudetechnik-Überwachung mit Fokus auf Heizung, Warmwasser und Energieverbrauch.

## 📁 Verfügbare Dokumente

### Hauptanalysen
1. **final-erentrudisstr-dataset-hierarchy.md** ⭐  
   - Vollständige Datensatz-Hierarchie
   - Beziehungen zwischen allen Dateien
   - Empfehlungen für Datennutzung

2. **erentrudisstr-datasets-analyse.md**  
   - Detaillierte Analyse aller Datensätze
   - Parameter-Übersicht
   - Zeitliche Abdeckung

### Vergleichsanalysen
3. **all-vs-relevant-comparison.md**  
   - Vergleich zwischen All_24-07 und Relevant-Dateien
   - Unterschiede in Parameterumfang

4. **relevant-files-comparison.md**  
   - Detailvergleich Relevant vs Relevant-1
   - Subset-Beziehungen

5. **durchfluss-complete-comparison.md**  
   - Analyse der Durchflussdaten
   - Minimalster Datensatz

6. **complete-dataset-comparison.md**  
   - Gesamtvergleich aller 6 CSV-Dateien

### Erste Analysen
7. **Monitoringdaten_Erentrudisstr_Analyse.md**  
   - Initiale Datenexploration
   - Erste Erkenntnisse

## 🔑 Datensatz-Hierarchie

```
export_ERS (49 Parameter, 16 Monate)
    ⊃ All_24-07 (45 Parameter, Juli)
        ⊃ Relevant-1 (23 Parameter, Jahr)
            ⊃ Relevant (15 Parameter, Jahr)
                ⊃ Durchfluss/Vp (4 Parameter)
```

## 📊 Hauptdatensätze

| Datei | Parameter | Zeitraum | Verwendung |
|-------|-----------|----------|------------|
| export_ERS_2023-12 | 49 | Dez 2023 - März 2025 | Langzeitanalyse |
| All_24-07 | 45 | Juli 2024 | Detailanalyse Sommer |
| Relevant-1_2024 | 23 | Jahr 2024 | Jahresanalyse erweitert |
| Relevant_2024 | 15 | Jahr 2024 | Jahresanalyse Basis |
| Durchfluss | 4 | Jahr 2024 | Hydraulische Analyse |

## 💡 Besonderheiten

- **Pufferspeicher:** 8 Temperaturfühler (Puffer 2.01 - 2.08)
- **Heizkreise:** HK1 Ost, HK2 West
- **Fernwärme:** Vollständige Übergabestation
- **Warmwasser:** Frischwassermodul mit Zirkulation

## ⚠️ Bekannte Probleme

- CSV-Dateien export_ERS und Vp.csv benötigen Semikolon als Trennzeichen
- export_ERS hat nur 484 Datenpunkte für 16 Monate (spärliche Aufzeichnung)

---
*Ordner erstellt: 22.08.2025*