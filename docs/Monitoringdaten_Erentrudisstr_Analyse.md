# Analyse der Monitoringdaten Erentrudisstraße
## Umfassende Datenanalyse und Dokumentation

---

## 1. Übersicht der verfügbaren Daten

### 1.1 Datenumfang

Die Monitoringdaten der Erentrudisstraße umfassen ein umfangreiches Messsystem zur Erfassung von Gebäudetechnik-Parametern. Der Datensatz beinhaltet:

- **Gesamtdatenpunkte**: ~284.030 Zeilen über verschiedene Zeiträume
- **Primärer Erfassungszeitraum**: 01.01.2024 - 31.12.2024 (vollständiges Jahr)
- **Erweiterte Daten**: 01.12.2023 - 31.03.2025
- **Messintervalle**: 5 Minuten (Hauptdaten), teilweise Tagesdaten
- **Dateiformate**: CSV (6 Dateien) und Excel (3 Dateien)

### 1.2 Datenquellen und Systeme

**Gebäudemonitoring-System**: ECB/InSite
- **Export-ID**: 2011
- **Protokoll**: Proprietär mit CSV/XLSX Export
- **Schnittstelle**: Automatisierter Export

### 1.3 Datenkategorien

Die erfassten Daten lassen sich in folgende Hauptkategorien einteilen:

1. **Fernwärmeversorgung**
   - Durchflussmessungen
   - Leistungsmessungen
   - Zählerstände
   - Temperaturen (Vor-/Rücklauf)

2. **Warmwasserversorgung**
   - Frischwassermodul
   - Zirkulationssystem
   - Wasserzähler TWE

3. **Heizkreise**
   - HK1 Ost
   - HK2 West
   - Ventilstellungen
   - Pumpensteuerung

---

## 2. Datenqualität und Verfügbarkeit

### 2.1 Zeitliche Abdeckung

| Datensatz | Zeitraum | Auflösung | Datenpunkte |
|-----------|----------|-----------|-------------|
| **Hauptdaten 2024** | 01.01.2024 - 31.12.2024 | 5 Min | 89.202 |
| **Durchflussdaten** | 01.01.2024 - 31.12.2024 | 5 Min | 89.202 |
| **Aktuelle Daten** | 17.12.2024 - 15.01.2025 | 5 Min | 7.618 |
| **Erweiterte Periode** | 01.12.2023 - 31.03.2025 | Täglich | 484 |
| **Juli 2024 Detail** | 01.07.2024 - 31.07.2024 | 5 Min | 8.322 |

### 2.2 Datenqualität

**Positive Aspekte:**
- Konsistente 5-Minuten-Intervalle (99.1% der Zeitstempel)
- Vollständige Zeitreihen ohne größere Lücken
- Plausible Messwerte in erwarteten Bereichen

**Identifizierte Probleme:**
- **Fehlende Werte**: Besonders in erweiterten Datensätzen
  - Tagesdaten (484 Zeilen): 90% der Spalten mit 100% fehlenden Werten
  - Juli-Daten: ~10% fehlende Werte über alle Spalten
- **Datenformat-Inkonsistenzen**: Gemischte Dezimaltrennzeichen (Punkt/Komma)
- **Nullwerte**: Durchfluss Wasserzähler TWE konstant bei 0

### 2.3 Statistiken zur Datenverfügbarkeit

| Parameter | Verfügbarkeit | Qualität |
|-----------|---------------|----------|
| Fernwärme-Durchfluss | 100% | Gut |
| Fernwärme-Leistung | 100% | Gut |
| Temperaturen | 100% | Gut |
| Zählerstände | 100% | Gut |
| Pumpensteuerung | 10% | Mangelhaft |
| Ventilstellungen | 95% | Gut |

---

## 3. Kompakte Dateiübersicht

### Übersichtstabelle aller Monitoringdateien

| Dateiname | Beschreibung | Zeitraum | Datenpunkte | Spalten | Größe | Hauptinhalt |
|-----------|--------------|----------|-------------|---------|-------|-------------|
| **CSV-Dateien** ||||||| 
| `export_ERS_2023-12-01...2025-03-31.csv` | Tagesdaten Übersicht | 01.12.23-31.03.25 | 484 | 49 | 0.97 MB | Temperaturen (11x), Durchflüsse, Pumpen/Ventile (90% Lücken) |
| `Vp.csv` | Aktuelle Durchflüsse | 17.12.24-15.01.25 | 7.618 | 4 | 1.29 MB | Durchfluss FW/TWE/Zirk. (5-Min, vollständig) |
| `2024/Relevant_2024..._(2).csv` | **Hauptdatensatz 2024** | 01.01.24-31.12.24 | 89.202 | 15 | 22.6 MB | Kernparameter: Temp(8x), Durchfluss(3x), Leistung, Zählerstände |
| `2024/Relevant-1_2024..._(3).csv` | Erweiterte Parameter | 01.01.24-31.12.24 | 89.202 | 23 | - | Zusätzliche Messpunkte (30% Lücken) |
| `2024/All_24-07...csv` | Juli Detaildaten | 01.07.24-31.07.24 | 8.322 | 45 | - | Alle Parameter Juli (10% Lücken) |
| `2024/Durchfluß/export_2011...csv` | Durchfluss-Fokus | 01.01.24-31.12.24 | 89.202 | 4 | 15.1 MB | Nur Durchflüsse FW/TWE/Zirk. (vollständig) |
| **Excel-Dateien** ||||||| 
| `Monitoring_ERS.xlsx` | Basis-Monitoring | Juli 2024 | 8.325 | 46 | - | 2 Sheets: Daten + Analyse |
| `Monitoring_ERS_2024_V2_250506.xlsx` | Konsolidierte Auswertung | 01.12.23-06.05.25 | 486 | 49 | - | 4 Sheets: Auswahl, Schema, Daten |
| `Monitoring_ERS_24-07_all.xlsx` | **Jahresauswertung 2024** | 01.01.24-31.12.24 | 89.202 | 25 | - | 5 Sheets inkl. HEB (Heizenergiebilanz) |

### Legende
- **FW** = Fernwärme, **TWE** = Trinkwassererwärmung, **Zirk.** = Zirkulation, **HEB** = Heizenergiebilanz
- **Fett markiert** = Hauptdatensätze mit bester Qualität
- **Lücken %** = Anteil fehlender Werte in den Datensätzen

---

## 4. Detaillierte Datei-Zuordnung

### 3.1 CSV-Dateien

#### **export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv**
- **Umfang**: 484 Zeilen × 49 Spalten
- **Zeitraum**: 01.12.2023 - 31.03.2025 (Tagesdaten)
- **Inhalt**:
  - Systemstatus (Pumpen, Ventile)
  - Temperaturen (11 Messpunkte)
  - Durchflüsse (3 Zähler)
  - Leistung Fernwärme
- **Besonderheit**: Viele fehlende Werte (90% der Spalten)

#### **Vp.csv**
- **Umfang**: 7.618 Zeilen × 4 Spalten
- **Zeitraum**: 17.12.2024 - 15.01.2025
- **Zeitauflösung**: 5 Minuten
- **Inhalt**:
  - Durchfluss Zähler Fernwärme (m³/h)
  - Durchfluss Wasserzähler TWE (m³/h)
  - Durchfluss Zähler Zirkulation (m³/h)
- **Qualität**: Vollständig, keine fehlenden Werte

#### **2024/Relevant_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (2).csv**
- **Umfang**: 89.202 Zeilen × 15 Spalten
- **Zeitraum**: Gesamtes Jahr 2024
- **Inhalt**: Kernparameter
  - Durchflüsse (3 Zähler)
  - Temperaturen (8 Messpunkte)
  - Zählerstände (Fernwärme, Zirkulation)
  - Leistung (Fernwärme, Zirkulation)
- **Besonderheit**: Hauptdatensatz mit bester Qualität

#### **2024/Durchfluß/export_2011_2024-01-01-00-00_2024-12-31-23-59.csv**
- **Umfang**: 89.202 Zeilen × 4 Spalten
- **Inhalt**: Fokus auf Durchflussmessungen
  - Durchfluss Zähler Fernwärme
  - Durchfluss Wasserzähler TWE
  - Durchfluss Zähler Zirkulation

### 3.2 Excel-Dateien

#### **2024/Monitoring_ERS_2024_V2_250506.xlsx**
- **Sheets**: 4 (Auswahl, Schema, All 01.12.23 - 31.03.25, All 01.12.22 - 06.05.25)
- **Hauptsheet**: 486 Zeilen × 49 Spalten
- **Inhalt**: Konsolidierte Übersicht mit Auswertungen

#### **2024/Monitoring_ERS_24-07_all.xlsx**
- **Sheets**: 5 (24-07_All, 2024, HEB, Temp, Grundriss_EA)
- **Hauptsheet "2024"**: 89.202 Zeilen × 25 Spalten
- **Besonderheit**: Enthält Heizenergiebilanz (HEB)

---

## 4. Messparameter-Übersicht

### 4.1 Temperatursensoren

| Messpunkt | Bereich | Einheit | Beschreibung |
|-----------|---------|---------|--------------|
| Vorlauf Fernwärme primär | 57-65°C | °C | Eingang Fernwärme |
| Rücklauf Fernwärme primär | 32-57°C | °C | Rückführung Fernwärme |
| Vorlauf Frischwassermodul | 55-65°C | °C | Warmwasserbereitung |
| Rücklauf Frischwassermodul | 45-55°C | °C | Nach Wärmeabgabe |
| Warmwasser vor Zirkulation | 55-60°C | °C | Vor Verteilung |
| Warmwasser nach Zirkulation | 50-55°C | °C | Nach Rückführung |
| Kaltwasser | 8-15°C | °C | Frischwasser Eingang |

### 4.2 Durchflussmessungen

| Zähler | Bereich | Einheit | Auflösung |
|--------|---------|---------|-----------|
| Fernwärme | 0-6 m³/h | m³/h | 0,01 |
| Zirkulation | 0-2 m³/h | m³/h | 0,01 |
| TWE Wasserzähler | 0 m³/h | m³/h | Defekt/Inaktiv |

### 4.3 Leistungsmessungen

| Parameter | Bereich | Einheit | Beschreibung |
|-----------|---------|---------|--------------|
| Leistung Fernwärme | -77 bis 252 kW | W | Thermische Leistung |
| Leistung Zirkulation | 0-15 kW | W | Zirkulationsverluste |

### 4.4 Zählerstände

| Zähler | Startstand | Endstand | Verbrauch 2024 |
|--------|------------|----------|----------------|
| Fernwärme | 1.012.510 kWh | 1.278.330 kWh | 265.820 kWh |
| Zirkulation | 120.858 kWh | 155.929 kWh | 35.071 kWh |

---

## 5. Erkenntnisse und Auffälligkeiten

### 5.1 Positive Aspekte

1. **Hohe Datenqualität**: Die Hauptdatensätze für 2024 sind vollständig und konsistent
2. **Gute zeitliche Auflösung**: 5-Minuten-Intervalle ermöglichen detaillierte Analysen
3. **Umfassende Messpunkte**: Alle relevanten Gebäudetechnik-Parameter werden erfasst
4. **Plausible Messwerte**: Temperaturen und Leistungen im erwarteten Bereich

### 5.2 Identifizierte Probleme

1. **TWE Wasserzähler**: Konstant 0 m³/h - vermutlich defekt oder nicht angeschlossen
2. **Pumpensteuerung**: Viele fehlende Werte in Steuerungssignalen
3. **Datenformat**: Inkonsistente Dezimaltrennzeichen erschweren automatisierte Verarbeitung
4. **Tagesdaten-Export**: Aggregierte Tagesdaten haben hohen Anteil fehlender Werte

### 5.3 Empfehlungen

1. **Wasserzähler TWE**: Prüfung und ggf. Reparatur/Austausch
2. **Datenexport**: Standardisierung der Dezimaltrennzeichen
3. **Qualitätssicherung**: Regelmäßige Plausibilitätsprüfungen implementieren
4. **Dokumentation**: Einheitliche Benennung der Messpunkte

---

## 6. Technische Spezifikationen

### 6.1 Datenerfassung

- **System**: ECB/InSite Gebäudeleittechnik
- **Export-ID**: 2011
- **Intervall**: 5 Minuten (Standard), 1 Tag (Aggregation)
- **Format**: CSV mit Semikolon-Trennung, UTF-8/ISO-8859-1
- **Zeitstempel**: DD.MM.YYYY HH:MM oder YYYY-MM-DD HH:MM:SS

### 6.2 Speicherbedarf

| Datensatz | Dateigröße | Zeilen | Spalten |
|-----------|------------|--------|---------|
| Jahredaten 2024 | 22.6 MB | 89.202 | 15 |
| Durchflussdaten | 15.1 MB | 89.202 | 4 |
| Monatsdaten Juli | 8.3 MB | 8.322 | 45 |
| Aktuelle Daten | 1.3 MB | 7.618 | 4 |

### 6.3 Verarbeitungshinweise

```python
# Empfohlene Einleseparameter für Python/Pandas:
pd.read_csv(
    filepath,
    sep=';',           # Semikolon als Trenner
    encoding='utf-8',  # oder 'iso-8859-1'
    decimal=',',       # Komma als Dezimalzeichen
    parse_dates=['Datum + Uhrzeit'],
    dayfirst=True      # DD.MM.YYYY Format
)
```

---

## 7. Zusammenfassung

Die Monitoringdaten der Erentrudisstraße bieten eine umfassende Grundlage für energetische Analysen und Optimierungen. Mit über 280.000 Datenpunkten und einer 5-Minuten-Auflösung sind detaillierte Untersuchungen von Lastprofilen, Verbrauchsmustern und Systemeffizienz möglich.

**Kernstärken:**
- Vollständige Jahredaten 2024
- Hohe zeitliche Auflösung
- Umfassende Systemabdeckung
- Gute Datenqualität bei Hauptparametern

**Verbesserungspotenzial:**
- Reparatur/Aktivierung TWE Wasserzähler
- Standardisierung Datenformate
- Vervollständigung Pumpensteuerungsdaten

Die Daten eignen sich hervorragend für:
- Energiebilanzierung
- Lastganganalysen
- Effizienzoptimierung
- Predictive Maintenance
- Benchmarking

---

*Erstellt: 2025-08-20*  
*Datenstand: 2024-01-01 bis 2025-03-31*