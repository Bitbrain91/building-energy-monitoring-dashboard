# Datenlandschaft-Übersicht MokiG Projekt
## Kompakte Übersicht aller verfügbaren Datenquellen

**Stand:** 20.08.2025  
**Projekt:** MokiG - Monitoring für klimaneutrale Gebäude (FFG 923166)

---

## Executive Summary

Das MokiG-Projekt verfügt über **5 Hauptdatenquellen** mit insgesamt **~3,4 Millionen Datenpunkten** aus verschiedenen Gebäuden und Energieerzeugungsanlagen im Raum Salzburg und Pinzgau. Die Daten umfassen Monitoring-Informationen von Gebäudetechnik, Energieerzeugung und Umweltbedingungen mit einer zeitlichen Auflösung von 5 Minuten bis zu Stundenwerten über einen Zeitraum von 2020 bis 2025.

---

## 1. Übersicht aller Datenquellen

| Datenquelle | Gebäude/Region | Datenzeitraum | Datenpunkte | Messintervall | Dateiformate | Qualität |
|-------------|----------------|---------------|-------------|---------------|--------------|----------|
| **Twin2Sim** | FH Salzburg Forschungsgebäude | Juni 2025 (Beispiel) | ~500 | 1 Stunde | CSV | 100% |
| **Erentrudisstraße** | Mehrfamilienhaus Salzburg | 2023-2025 | ~284.000 | 5 Minuten | CSV, XLSX | 95% |
| **Friedrich-Inhauser-Str.** | 8 Wohnhäuser (1,3,5,7,9,11,13,15) | 2024-2025 | ~2.500.000 | 5 Minuten | CSV, XLSX | 86% |
| **KW Dürnbach** | Wasserkraftwerk Neukirchen | 2020-2024 | ~175.000 | 15 Minuten | XLSX | 100% |
| **KW Untersulzbach** | Wasserkraftwerk Neukirchen | 2020-2024 | ~175.000 | 15 Minuten | XLSX | 100% |
| **KW Wiesbach** | Wasserkraftwerk Neukirchen | 2020-2024 | ~175.000 | 15 Minuten | XLSX | 100% |
| **Netzübergabe** | Neukirchen Stromnetz | 2020-2024 | ~352.000 | 15 Minuten | XLSX | 100% |

---

## 2. Detaillierte Datencharakteristik pro Quelle

### 2.1 Twin2Sim - Forschungsgebäude FH Salzburg

| Aspekt | Details |
|--------|---------|
| **Datensätze** | 5 CSV-Dateien |
| **Spaltennamen/Anzahl** | |
| - T2S_IntPV.csv | 9 Spalten: Leistung, Frequenz, Energie, Temperatur |
| - T2S_Wetterdaten.csv | 14 Spalten: Wind, Feuchte, Druck, Strahlung, Temperatur |
| - T2S_Lüftung.csv | 42 Spalten: Zuluft, Abluft, WRG, Ventilator-Parameter |
| - T2S_RAU006.csv | Raummonitoring-Parameter |
| - T2S_ManiPV.csv | PV-Monitoring-Parameter |
| **Datenpunkte** | ~100 Zeilen pro Datei (Beispielzeitraum) |
| **Aufnahmefrequenz** | Stündlich (60-Minuten-Intervalle) |
| **Fehlende Werte** | 0% - Vollständige Zeitreihen |
| **Qualität** | Exzellent - Lückenlose Messreihen |
| **Potenzielle Lücken** | Keine - nur Beispieldaten verfügbar |

### 2.2 Erentrudisstraße - Mehrfamilienhaus

| Aspekt | Details |
|--------|---------|
| **Gebäudestruktur** | UG, EG, 1-4 OG |
| **Datensätze** | 6 CSV + 3 XLSX Dateien |
| **Hauptdatei-Spalten** | 15-49 Spalten je nach Datei |
| **Kernparameter** | |
| - Temperaturen | 8-11 Messpunkte (VL/RL Fernwärme, Warmwasser, Kaltwasser) |
| - Durchflüsse | 3 Zähler (Fernwärme, TWE, Zirkulation) |
| - Leistungen | Fernwärme (-77 bis 252 kW), Zirkulation (0-15 kW) |
| - Zählerstände | Fernwärme, Zirkulation (kWh) |
| **Datenpunkte** | 89.202 (Jahr 2024) + 194.828 (weitere Zeiträume) |
| **Aufnahmefrequenz** | 5-Minuten-Intervalle (288 Werte/Tag) |
| **Fehlende Werte** | ~5% (hauptsächlich Nachtstunden) |
| **Qualität** | Sehr gut - kontinuierliche Aufzeichnung |
| **Potenzielle Lücken** | TWE Wasserzähler konstant 0 (defekt), Pumpensteuerung 90% fehlend |

### 2.3 Friedrich-Inhauser-Straße - Wohnkomplex

| Aspekt | Details |
|--------|---------|
| **Gebäudestruktur** | 8 Häuser (1, 3, 5, 7, 9, 11, 13, 15) |
| **Datensätze** | 3 CSV + 2 XLSX Dateien |
| **Hauptdatei-Spalten** | 111 Messpunkte gesamt |
| **Sensorverteilung** | |
| - Stromzähler | 24 Sensoren (Lüftung, Heizung, Wärmepumpe) |
| - Kältezähler | 29 Sensoren (alle Häuser) |
| - Temperaturen | 41 Sensoren (VL/RL, Außentemperatur) |
| - Durchflüsse | 6 Sensoren (0-7 m³/h) |
| - Leistungen | 10 Sensoren (Pelletkessel, DLE, etc.) |
| **Datenpunkte** | ~22.800 pro 3 Monate × 111 Parameter = 2,5 Mio. |
| **Aufnahmefrequenz** | 5-Minuten-Intervalle |
| **Fehlende Werte** | 14,2% (3 größere Ausfälle: 36h, 19,5h, 19,5h) |
| **Qualität** | Gut - gleichmäßige Verfügbarkeit (85,8%) |
| **Potenzielle Lücken** | Wärmepumpen-Daten 43% fehlend, einige Sensoren konstant 0 |

### 2.4 Kraftwerke Neukirchen - Wasserkraft

| Aspekt | KW Dürnbach | KW Untersulzbach | KW Wiesbach |
|--------|-------------|------------------|-------------|
| **Dateien** | 5 XLSX (2020-2024) | 5 XLSX (2020-2024) | 5 XLSX (2020-2024) |
| **Spalten** | 4: Zeit_Von, Zeit_Bis, Energie (kWh), Leistung (kW) | Identisch | Identisch |
| **Datenpunkte/Jahr** | ~35.040-35.137 | ~35.040-35.137 | ~35.040-35.137 |
| **Aufnahmefrequenz** | 15-Minuten-Intervalle (96 Werte/Tag) | 15 Minuten | 15 Minuten |
| **Fehlende Werte** | < 0,1% | < 0,1% | < 0,1% |
| **Mittl. Leistung** | 243 kW | Vergleichbar | Vergleichbar |
| **Max. Leistung** | 293 kW | Vergleichbar | Vergleichbar |
| **Jahreserzeugung** | ~2,14 GWh | Vergleichbar | Vergleichbar |
| **Qualität** | Exzellent | Exzellent | Exzellent |

### 2.5 Netzübergabe Neukirchen

| Aspekt | Bezug | Lieferung |
|--------|-------|-----------|
| **Dateien** | 60 XLSX (12 Monate × 5 Jahre) | 60 XLSX (12 Monate × 5 Jahre) |
| **Spalten** | 4: Zeit_Von, Zeit_Bis, Wert, Einheit | Identisch |
| **Datenpunkte/Monat** | ~2.880-2.980 | ~2.880-2.980 |
| **Aufnahmefrequenz** | 15-Minuten-Intervalle | 15 Minuten |
| **Fehlende Werte** | 0% | 0% |
| **Qualität** | Exzellent - lückenlos | Exzellent - lückenlos |

---

## 3. Zusammenfassende Qualitätsbewertung

### Datenvolumen gesamt

| Metrik | Wert |
|--------|------|
| **Gesamte Datenpunkte** | ~3,4 Millionen |
| **Zeitliche Abdeckung** | 2020-2025 |
| **Anzahl Gebäude/Anlagen** | 12 (8 Wohnhäuser, 1 MFH, 3 Kraftwerke) |
| **Anzahl Dateien** | ~155 Dateien |
| **Speicherbedarf** | ~335 MB |

### Qualitätsübersicht

| Datenquelle | Vollständigkeit | Konsistenz | Verfügbarkeit | Gesamtqualität |
|-------------|-----------------|------------|---------------|----------------|
| Twin2Sim | ⭐⭐⭐⭐⭐ 100% | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ (Beispiel) | Exzellent für Tests |
| Erentrudisstraße | ⭐⭐⭐⭐ 95% | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Sehr gut |
| F.-Inhauser-Str. | ⭐⭐⭐⭐ 86% | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Gut |
| Kraftwerke | ⭐⭐⭐⭐⭐ 100% | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Exzellent |
| Netzübergabe | ⭐⭐⭐⭐⭐ 100% | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Exzellent |

---

## 4. Kritische Datenlücken und Handlungsbedarf

### Identifizierte Probleme

| Priorität | Datenquelle | Problem | Auswirkung | Empfehlung |
|-----------|-------------|---------|------------|------------|
| **HOCH** | Erentrudisstraße | TWE Wasserzähler konstant 0 | Warmwasserverbrauch nicht messbar | Zähler prüfen/reparieren |
| **MITTEL** | F.-Inhauser-Str. | 3 Systemausfälle (75h gesamt) | Datenlücken Jan/Feb 2025 | Backup-System einrichten |
| **MITTEL** | F.-Inhauser-Str. | Wärmepumpen 43% fehlend | Eingeschränkte WP-Analyse | Sensoren prüfen |
| **NIEDRIG** | Erentrudisstraße | Pumpensteuerung 90% fehlend | Betriebsanalyse eingeschränkt | Optional nachrüsten |
| **NIEDRIG** | Alle | Unterschiedliche Formate | Erschwerte Integration | Harmonisierung |

### Positive Aspekte

- **Kraftwerksdaten**: Perfekte 5-Jahres-Zeitreihen ohne Lücken
- **Zeitliche Auflösung**: 5-15 Minuten ermöglicht detaillierte Analysen
- **Gebäudevielfalt**: Verschiedene Gebäudetypen für Vergleichsanalysen
- **Lange Zeiträume**: Bis zu 5 Jahre historische Daten verfügbar

---

## 5. Nutzungspotenziale für Analysen

| Analyseart | Geeignete Datenquellen | Mögliche Erkenntnisse |
|------------|------------------------|----------------------|
| **Energiebilanzierung** | Alle | Gesamtenergieverbrauch vs. Erzeugung |
| **Lastganganalysen** | Erentrudis, F.-Inhauser | Tages-/Wochenprofile, Spitzenlastzeiten |
| **Erzeugungsprognosen** | Kraftwerke, Twin2Sim PV | Produktionsvorhersagen |
| **Effizienzoptimierung** | F.-Inhauser (8 Häuser) | Vergleich identischer Gebäude |
| **Wetterkorrelation** | Twin2Sim + alle Gebäude | Heizlast vs. Außentemperatur |
| **Netzstabilität** | Kraftwerke + Netzübergabe | Einspeisung vs. Bezug |
| **Predictive Maintenance** | Alle kontinuierlichen Daten | Anomalieerkennung |

---

## 6. Technische Hinweise für Datennutzung

### Empfohlene Verarbeitungstools
- **Python**: pandas, openpyxl für Excel-Dateien
- **Zeitreihenanalyse**: 5-15 Minuten Auflösung ideal
- **Speicherbedarf**: ~2 GB RAM für Gesamtanalyse

### Datenintegration
1. **Zeitstempel harmonisieren**: ISO 8601 Format
2. **Einheiten standardisieren**: kW/kWh einheitlich
3. **Dezimaltrennzeichen**: Punkt vs. Komma beachten
4. **Encoding**: UTF-8 oder ISO-8859-1

---

*Dokumentversion: 1.0 | Erstellt für Projektmeeting | Stand: 20.08.2025*