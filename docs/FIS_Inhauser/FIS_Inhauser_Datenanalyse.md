# Analyse der Monitoringdaten Friedrich-Inhauser-Straße
## Umfassende Datenanalyse und Dokumentation

---

## 1. Übersicht der verfügbaren Daten

### 1.1 Datenumfang

Die Monitoringdaten der Friedrich-Inhauser-Straße umfassen ein komplexes Gebäudemonitoring-System für einen Wohnkomplex mit 8 Häusern (Haus 1, 3, 5, 7, 9, 11, 13, 15). Der Datensatz beinhaltet:

- **Gesamtdatenpunkte**: ~2,5 Millionen Messpunkte
- **Primärer Erfassungszeitraum**: 31.12.2024 - 31.03.2025 (3 Monate)
- **Erweiterte Daten**: 01.01.2024 - 16.05.2025 (Außentemperatur)
- **Messintervalle**: 5 Minuten (konsistent zu 87%)
- **Dateiformate**: CSV (3 Dateien) und Excel (2 Dateien)

### 1.2 Datenquellen und Systeme

**Gebäudemonitoring-System**: ECB/InSite
- **Export-ID**: 1551
- **Protokoll**: Proprietär mit CSV/XLSX Export
- **Schnittstelle**: Automatisierter Export mit 111 Messpunkten

### 1.3 Datenkategorien

Die erfassten Daten lassen sich in folgende Hauptkategorien einteilen:

1. **Elektrische Energie (24 Sensoren)**
   - Stromzähler für Lüftungsgeräte (alle Häuser)
   - Stromzähler für Heizung
   - Stromzähler für Abluft-Wärmepumpe (ABL-WP)
   - Leistungsmessungen und Energieverbräuche

2. **Kältesysteme (29 Sensoren)**
   - Kältezähler für Lüftungsgeräte (alle Häuser)
   - Durchflussmessungen
   - Leistungsmessungen
   - Energieverbräuche

3. **Temperatursensoren (41 Sensoren)**
   - Vor- und Rücklauftemperaturen Lüftungsgeräte
   - Außentemperatur (kontinuierliche Messreihe)
   - Wärmepumpen-Temperaturen (16 Messpunkte)
   - Systemtemperaturen

4. **Durchflussmessungen (6 Sensoren)**
   - KMZ Lüftung für verschiedene Häuser
   - Abluft-Wärmepumpe Durchfluss
   - Volumenstrom-Messungen

5. **Leistungsmessungen (10 Sensoren)**
   - DLE-Zähler
   - Pelletkessel
   - Diverse Leistungsaufnahmen

---

## 2. Datenqualität und Verfügbarkeit

### 2.1 Zeitliche Abdeckung

| Datensatz | Zeitraum | Auflösung | Datenpunkte | Abdeckung |
|-----------|----------|-----------|-------------|-----------|
| **Hauptdaten 2025** | 31.12.2024 - 31.03.2025 | 5 Min | 22.806 | 87.0% |
| **Wärmepumpen-Daten** | 01.01.2025 - 03.12.2025 | 5 Min | 21.138 | Variable |
| **Außentemperatur** | 01.01.2024 - 16.05.2025 | 5 Min | 54.154 | 87.2% |
| **Test-Woche** | 23.01.2025 - 29.01.2025 | 5 Min | 1.569 | 100% |

### 2.2 Datenqualität

**Positive Aspekte:**
- Konsistente 5-Minuten-Intervalle (87% der Zeitstempel)
- Umfassende Sensorabdeckung für alle 8 Häuser
- Vollständige Außentemperatur-Zeitreihe über 16 Monate
- Gleichmäßige Datenverfügbarkeit über alle Häuser (85.8%)

**Identifizierte Probleme:**
- **Datenlücken**: 3 größere Ausfälle identifiziert
  - 25.01. - 27.01.2025: 36 Stunden Ausfall
  - 04.02. - 05.02.2025: 19.5 Stunden Ausfall
  - 18.02. - 19.02.2025: 19.5 Stunden Ausfall
- **Fehlende Werte**: Durchschnittlich 14.2% über alle Sensoren
- **Inaktive Sensoren**: Einige Zähler zeigen konstant 0 (z.B. Stromzähler Heizung)

### 2.3 Statistiken zur Datenverfügbarkeit

| Sensortyp | Anzahl Sensoren | Datenverfügbarkeit | Qualität |
|-----------|-----------------|-------------------|----------|
| Stromzähler | 24 | 85.9% | Gut |
| Kältezähler | 29 | 85.9% | Gut |
| Temperatursensoren | 41 | 85.5% | Gut |
| Durchflussmessungen | 6 | 85.9% | Gut |
| Leistungsmessungen | 10 | 85.9% | Gut |

### 2.4 Hausspezifische Verfügbarkeit

| Haus | Sensoren | Datenvollständigkeit | Besonderheiten |
|------|----------|---------------------|----------------|
| 1 | 31 | 85.8% | Höchste Sensoranzahl |
| 3 | 7 | 85.8% | Standard-Ausstattung |
| 5 | 7 | 85.8% | Standard-Ausstattung |
| 7 | 7 | 85.8% | Standard-Ausstattung |
| 9 | 7 | 85.8% | Standard-Ausstattung |
| 11 | 7 | 85.8% | Standard-Ausstattung |
| 13 | 8 | 85.8% | Erweiterte Sensorik |
| 15 | 9 | 85.8% | Erweiterte Sensorik |

---

## 3. Detaillierte Dateiübersicht

### 3.1 Übersichtstabelle aller Monitoringdateien

| Dateiname | Beschreibung | Zeitraum | Datenpunkte | Spalten | Hauptinhalt |
|-----------|--------------|----------|-------------|---------|-------------|
| **CSV-Dateien** ||||||| 
| `export_1551_2024-12-31...2025-03-31.csv` | **Hauptdatensatz** | 31.12.24-31.03.25 | 22.806 | 111 | Alle Gebäudesensoren: Strom (24x), Kälte (29x), Temp (41x), Durchfluss (6x) |
| `export_1551_2025-01-01...2025-03-31.csv` | Wärmepumpen-Fokus | 01.01.25-03.12.25 | 21.138 | 26 | WP-Temperaturen (16x), Kondensator/Verdampfer-Daten |
| `V1_2501_EXPORT_1.CSV` | Test-Export | Januar 2025 | - | - | Validierungsdaten |
| **Excel-Dateien** ||||||| 
| `2024-2025-05_AT.xlsx` | Außentemperatur | 01.01.24-16.05.25 | 54.154 | 2 | Langzeit-Außentemperatur (-8°C bis +34°C) |
| `250123-250129_ok_250130.xlsx` | Test-Woche | 23.01.25-29.01.25 | 1.569 | 112 | Vollständige Sensordaten + Metadaten (113 Zeilen) |

### 3.2 Datenstruktur im Detail

#### Hauptdatensatz (export_1551_2024-12-31)
Dieser Datensatz bildet das Kernstück der Monitoring-Daten mit 111 Messpunkten:

**Elektrische Messungen (24 Spalten):**
- Stromzähler für jedes Haus (Lüftungsgeräte)
- Heizungsstromzähler
- ABL-WP Stromzähler
- Format: Energie (kWh) und Leistung (kW)

**Kältetechnik (29 Spalten):**
- Kältezähler für Lüftungsgeräte
- Durchfluss-, Energie- und Leistungsmessungen
- Wertebereich: -2.300 bis 29.700 kW

**Temperaturen (41 Spalten):**
- Vor-/Rücklauftemperaturen aller Systeme
- Typischer Bereich: 4°C bis 19°C
- Vollständige Abdeckung aller Häuser

**Durchflussmessungen (6 Spalten):**
- KMZ Lüftung Durchfluss
- ABL-WP Durchfluss
- Bereich: 0 bis 7 m³/h

#### Wärmepumpen-Datensatz
Spezialisierte Messungen für die Wärmepumpenanlage:
- 16 Temperaturmesspunkte
- Verdampfer/Kondensator-Temperaturen
- Abwasser-WP und Abluft-WP Daten
- Höhere Fehlwerte-Rate (43%)

#### Außentemperatur-Datensatz
Langzeit-Referenzdaten:
- Kontinuierliche Messreihe über 16 Monate
- 5-Minuten-Auflösung
- Temperaturbereich: -8°C bis +34°C
- Keine fehlenden Werte

---

## 4. Statistische Kennzahlen

### 4.1 Energieverbrauch

| Messgröße | Mittelwert | Minimum | Maximum | Einheit |
|-----------|------------|---------|---------|---------|
| Stromverbrauch Lüftung | 77.14 | 0 | 96 | kW |
| Kälteleistung | 2,921.72 | -2,300 | 29,700 | kW |
| Pelletkessel-Leistung | 48,336.13 | -19,200 | 141,300 | kW |

### 4.2 Temperaturstatistiken

| Parameter | Mittelwert | Minimum | Maximum | Std.Abw. |
|-----------|------------|---------|---------|----------|
| Außentemperatur | 9.94°C | -8.00°C | 34.00°C | 7.61°C |
| Rücklauf Lüftung | 10.24°C | 4.00°C | 19.00°C | - |
| Vorlauf Lüftung | 8.33°C | 4.00°C | 18.00°C | - |

### 4.3 Durchflussstatistiken

| System | Mittelwert | Maximum | Einheit |
|--------|------------|---------|---------|
| KMZ Lüftung | 0.29 | 2.00 | m³/h |
| ABL-WP | 0.80 | 5.00 | m³/h |
| Kältezähler | 0.24 | 7.00 | m³/h |

---

## 5. Besonderheiten und Auffälligkeiten

### 5.1 Systemspezifische Merkmale
- **Haus 1** verfügt über die umfangreichste Sensorausstattung (31 Messpunkte)
- **Häuser 13 und 15** haben erweiterte Überwachung
- **Wärmepumpenanlage** mit separatem, detailliertem Monitoring
- **Pelletkessel** als zusätzliche Wärmequelle erfasst

### 5.2 Datenqualität-Hinweise
- Konsistente Datenqualität über alle Häuser (85.8% Vollständigkeit)
- Regelmäßige Systemausfälle von 19-36 Stunden Dauer
- Einige Sensoren liefern konstant Nullwerte (prüfungsbedürftig)
- Wärmepumpen-Daten weisen höhere Fehlwerte auf (43%)

### 5.3 Empfehlungen für die Datennutzung
1. **Primärdaten verwenden**: Hauptdatensatz (export_1551_2024-12-31) für Gesamtanalysen
2. **Außentemperatur-Referenz**: Langzeitdaten für Korrelationsanalysen nutzen
3. **Datenlücken beachten**: Bei Analysen Ende Januar/Anfang Februar Ausfälle berücksichtigen
4. **Hausspezifische Analysen**: Gleichmäßige Datenqualität ermöglicht Vergleiche

---

## 6. Technische Dokumentation

### 6.1 Verfügbare Zusatzdokumente
- **Gebäudepläne**: EA_Pläne mit Architektur-Zeichnungen für alle Häuser
- **TGA-Dokumentation**: Technische Gebäudeausrüstung-Pläne (HSL-Schemata)
- **Regelungsbeschreibung**: FIS_Regelungsbeschreibung.pdf
- **Wissenschaftliche Arbeiten**: 3 Abschlussarbeiten zum Gebäudekomplex

### 6.2 Datenformat-Spezifikationen
- **CSV-Format**: Komma-separiert, UTF-8 Encoding
- **Zeitstempel**: Format "YYYY-MM-DD HH:MM:SS"
- **Dezimaltrennzeichen**: Punkt
- **Fehlwerte**: Leere Zellen oder NaN

### 6.3 Systemarchitektur
Der Gebäudekomplex Friedrich-Inhauser-Straße verfügt über:
- Zentrale Heizungsanlage mit Pelletkessel
- Dezentrale Lüftungsgeräte pro Haus
- Wärmepumpenanlage (Abluft/Abwasser)
- Kältesystem für Gebäudekühlung
- Umfassendes Monitoring über InSite-System

---

*Dokumentversion: 1.0*  
*Erstellungsdatum: 20.08.2025*  
*Analysezeitraum: Dezember 2024 - Mai 2025*