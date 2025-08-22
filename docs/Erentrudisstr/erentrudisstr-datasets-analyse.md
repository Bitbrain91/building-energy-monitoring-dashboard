# Erentrudisstraße - Datasets Analyse

**Analysedatum:** 21.08.2025  
**Datenstandort:** `/Daten/Monitoringdaten/Erentrudisstr`

## 📊 Übersicht der Datensätze

Die Erentrudisstraße-Monitoringdaten umfassen **9 Hauptdatensätze** (6 CSV-Dateien und 3 Excel-Dateien) mit Gebäudemonitoring- und Energiedaten. Zusätzlich befinden sich Gebäudepläne und technische Dokumentationen in separaten Ordnern.

## 📁 Dateistruktur

```
Erentrudisstr/
├── EA_Pläne/           # Energieausweis und Gebäudepläne (8 PDF-Dateien)
├── TGA/                # Technische Gebäudeausrüstung (4 Dateien)
└── Monitoring/         # Hauptdatenordner
    ├── 2024/           # Jahresspezifische Daten
    │   └── Durchfluß/  # Durchflussmessungen
    └── [Hauptdateien]
```

## 📈 Detaillierte Dateianalyse

### 1. **export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv**
- **Zeitraum:** Dezember 2023 bis März 2025
- **Datensätze:** 484 Zeilen
- **Parameter:** Umfassende Gebäudedaten (48 Parameter)
  - Pumpensteuerung (Zirkulation primär/sekundär)
  - Puffertemperaturen (2.01 bis 2.08)
  - Heizkreise (HK1 Ost, HK2 West)
  - Fernwärmedaten (Durchfluss, Leistung, Zählerstand)
  - Warmwassersystem
- **Besonderheit:** Komplettdatensatz mit allen Systemparametern

### 2. **Vp.csv**
- **Datensätze:** 7.618 Zeilen
- **Parameter:** Nur Durchflussmessungen
  - Durchfluss Zähler Fernwärme (m³/h)
  - Durchfluss Wasserzähler TWE (m³/h)
  - Durchfluss Zähler Zirkulation (m³/h)
- **Besonderheit:** Fokussiert auf Volumenstromdaten

### 3. **All_24-07_export_2011_2024-07-01-00-00_2024-07-31-23-59.csv**
- **Zeitraum:** Juli 2024
- **Datensätze:** 8.322 Zeilen
- **Parameter:** 44 Messgrößen
  - Ventilstellungen (%)
  - Drehzahlen Pumpen (%)
  - Alle Temperaturmessungen
  - Energieverbrauchsdaten
- **Besonderheit:** Detaildaten für Sommermonat

### 4. **Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv**
- **Zeitraum:** Gesamtes Jahr 2024
- **Datensätze:** 89.202 Zeilen
- **Parameter:** 23 ausgewählte Kenngrößen
  - Heizkreistemperaturen
  - Ventilstellungen und Status
  - Fernwärme- und Zirkulationsdaten
- **Besonderheit:** Reduzierter Parametersatz mit Fokus auf Heizung

### 5. **Relevant_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (2).csv**
- **Zeitraum:** Gesamtes Jahr 2024
- **Datensätze:** 89.202 Zeilen
- **Parameter:** 15 Kernparameter
  - Warmwassersystem
  - Energiezähler
  - Durchflussmessungen
- **Besonderheit:** Minimaler Parametersatz, Fokus auf Warmwasser

### 6. **export_2011_2024-01-01-00-00_2024-12-31-23-59.csv** (im Unterordner Durchfluß)
- **Zeitraum:** Gesamtes Jahr 2024
- **Datensätze:** 89.202 Zeilen
- **Parameter:** Nur 4 Durchflussparameter
- **Besonderheit:** Identisch mit Vp.csv-Struktur

### 7. **Monitoring_ERS.xlsx**
- **Blätter:** 2 (Daten, Analyse)
- **Datenblatt:** 8.325 Zeilen, 46 Spalten
- **Zeitraum:** 30.01.1900 bis 31.07.2024 (inkl. Fehldaten)
- **Analyseblatt:** Nur 2 Zeilen mit 5 Spalten
- **Besonderheit:** Hauptdatenquelle mit vollständiger Parameterübersicht

### 8. **Monitoring_ERS_2024_V2_250506.xlsx**
- **Blätter:** 4 (Auswahl, Schema, All 01.12.23-31.03.25, All 01.12.22-06.05.25)
- **Auswahl:** 487 Zeilen, 16 Parameter
- **Schema:** Leer (vermutlich für Systemdiagramm vorgesehen)
- **Hauptdaten:** 486 Zeilen, 49 Parameter
- **Besonderheit:** Erweiterte Version mit Auswahlmöglichkeiten

### 9. **Monitoring_ERS_24-07_all.xlsx**
- **Blätter:** 5 (24-07_All, 2024, HEB, Temp, Grundriss_EA)
- **Juli-Daten:** 8.325 Zeilen, 46 Parameter
- **Jahresdaten 2024:** 89.202 Zeilen, 25 Parameter
- **HEB:** Nur 3 Zeilen (vermutlich Heizenergiebilanz)
- **Besonderheit:** Kombiniert Monats- und Jahresdaten

## 🔄 Vergleich der Datasets

### Strukturidentität
**Vollständig identische Struktur** haben alle CSV-Dateien. Dies deutet auf ein fehlerhaftes Einlesen hin, da alle Parameter in einer einzigen Spalte zusammengefasst wurden (Trennzeichen-Problem).

### Parameter-Überschneidungen

#### Hohe Übereinstimmung (>90%)
- **Monitoring_ERS.xlsx (Daten)** ↔ **Monitoring_ERS_24-07_all.xlsx (2024)**: 91,7% Übereinstimmung
  - Gemeinsame Parameter: 22 von 24
  - Fokus: Leistungsdaten, Ventilstellungen, Temperaturen

#### Mittlere Übereinstimmung (50-90%)
- **Monitoring_ERS.xlsx (Daten)** ↔ **Monitoring_ERS_2024_V2_250506.xlsx (All)**: 64,4%
  - Gemeinsame Parameter: 29
  - Hauptsächlich Temperatur- und Pufferdaten

- **Monitoring_ERS_2024_V2_250506.xlsx (All)** ↔ **Monitoring_ERS_24-07_all.xlsx (2024)**: 58,3%
  - Gemeinsame Parameter: 14
  - Kernparameter wie Zählerstände und Haupttemperaturen

### Zeitliche Überschneidungen
- **Monitoring_ERS.xlsx** ↔ **Monitoring_ERS_24-07_all.xlsx**: 
  - Überlappung: 01.01.2024 bis 31.07.2024

### Subset-Beziehungen
- **Monitoring_ERS.xlsx (Analyse)** ist eine Teilmenge von **Monitoring_ERS.xlsx (Daten)**
  - Nur 4 Parameter von 46

## 🎯 Empfehlungen

### Datenbereinigung erforderlich:
1. **CSV-Dateien:** Trennzeichen-Problem beheben (Semikolon statt Komma)
2. **Zeitstempel:** Einheitliches Format etablieren
3. **Duplikate:** Redundante Dateien identifizieren

### Primäre Datenquellen:
- **Für Gesamtanalyse:** Monitoring_ERS_24-07_all.xlsx (Sheet "2024")
- **Für Detailanalyse:** Monitoring_ERS.xlsx (Sheet "Daten")
- **Für Durchflussanalyse:** Nach Korrektur der CSV-Dateien

### Datenintegration:
- Excel-Dateien enthalten korrekt strukturierte Daten
- CSV-Dateien müssen neu eingelesen werden
- Subset-Beziehungen zur Datenreduktion nutzen

## 📌 Technische Hinweise

**Problem mit CSV-Dateien:** Alle CSV-Dateien wurden mit falschen Trennzeichen eingelesen, wodurch alle Spalten in einer einzigen Spalte zusammengefasst wurden. Für eine korrekte Analyse müssen diese mit `;` als Trennzeichen und `,` als Dezimaltrennzeichen neu eingelesen werden.

**Zeitraumabdeckung:**
- Historische Daten: Ab 2011 (laut Dateinamen)
- Aktuelle Daten: Bis März 2025
- Hauptfokus: Jahr 2024

**Datenvolumen:**
- Größte Datensätze: ~89.000 Zeilen (Jahresdaten)
- Kleinste Datensätze: ~500 Zeilen (Ausschnitte)
- Gesamtparameter: Bis zu 49 verschiedene Messgrößen