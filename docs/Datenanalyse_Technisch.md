# Technische Datenanalyse MokiG
## Detaillierte technische Dokumentation der Datenquellen

---

## 1. Datenquellen-Matrix

### 1.1 Gebäudemonitoring-Systeme

| System | Hersteller/Typ | Protokoll | Datenformat | Schnittstelle |
|--------|---------------|-----------|-------------|---------------|
| **Twin²Sim** | Forschungsanlage FHS | CSV-Export | CSV (;) | Direkt |
| **Erentrudisstraße** | ECB/InSite | Proprietär | CSV/XLSX | Export |
| **Friedrich-Inhauser** | Unbekannt | Proprietär | CSV | Export ID 1551 |
| **Wetterstation** | MSR02 | Modbus | CSV | Gateway |

### 1.2 Energieerzeugung

| Anlage | Typ | Leistung | Datenerfassung |
|--------|-----|----------|----------------|
| **KW Dürnbach** | Wasserkraft | k.A. | XLSX Monatsexport |
| **KW Untersulzbach** | Wasserkraft | k.A. | XLSX Monatsexport |
| **KW Wiesbach** | Wasserkraft | k.A. | XLSX Monatsexport |
| **PV Haus 15** | Photovoltaik | k.A. | 5-Min-Werte |
| **Growatt MIC 600TL-X** | PV-Wechselrichter | 600W | Stundenwerte |

---

## 2. Detaillierte Parameteranalyse

### 2.1 Twin²Sim Photovoltaik (Growatt)

**Datei:** T2S_IntPV.csv  
**Parameter:** 9 Messgrößen

```
1. read_input_power          - Eingangsleistung DC (W)
2. read_output_power         - Ausgangsleistung AC (W)
3. read_grid_frequency       - Netzfrequenz (Hz)
4. read_today_generate_energy - Tageserzeugung (kWh)
5. read_total_generate_energy - Gesamterzeugung (kWh)
6. read_work_time_total      - Betriebsstunden gesamt
7. read_inverter_temperature - Wechselrichtertemperatur (°C)
8. read_inside_ipm_inverter_temperature - IPM Temperatur (°C)
```

**Datenqualität:**
- Vollständige Zeitreihe ohne Lücken
- Plausible Werte (Nacht: 0W, Tag: bis 400W)
- Temperaturwerte realistisch (27-47°C)

### 2.2 Twin²Sim Wetterstation

**Datei:** T2S_Wetterdaten.csv  
**Parameter:** 14 Messgrößen

```
Key-Parameter:
- Globalstrahlung: 0-500 W/m²
- Außentemperatur: 18-32°C (Sommerperiode)
- Rel. Luftfeuchte: 36-88%
- Windgeschwindigkeit: 0-4 m/s
- Niederschlagsintensität: 0 mm/h (Trockenperiode)
```

### 2.3 Twin²Sim Lüftungsanlage

**Datei:** T2S_Lüftung.csv  
**Parameter:** 42 Messgrößen

**Hauptkomponenten:**
- Zuluftventilator (ZVE)
- Fortluftventilator (FVE)
- Wärmerückgewinnung (WRG)
- Kühlregister (KRG)
- Heizregister (HRG)

**Betriebszustände:**
- Nachtabsenkung: 00:00-06:00 (0% Ventilatorleistung)
- Tagbetrieb: 06:00-21:00 (45-50% Ventilatorleistung)
- WRG-Betrieb: Bypass-Klappe 0-100%

### 2.4 Erentrudisstraße Fernwärme

**Messstellenübersicht:**
```
Fernwärme:
- Zähler Fernwärme: Durchfluss, Leistung, Zählerstand
- Temperaturen: VL/RL Primär

Warmwasser:
- Frischwassermodul: VL/RL Temperaturen
- Zirkulation: Primär/Sekundär
- TWE Wasserzähler: Durchfluss

Kennzahlen:
- Fernwärmeleistung: 0-120 kW
- Vorlauftemperatur: 57-65°C
- Rücklauftemperatur: 32-57°C
```

### 2.5 Friedrich-Inhauser-Straße Komplexanlage

**Gebäudestruktur:**
- 8 Häuser (1, 3, 5, 7, 9, 11, 13, 15)
- Je Haus: Lüftungsgerät mit Stromzähler und Kältezähler
- Zentrale Wärmeerzeugung

**Wärmeerzeugung:**
```
1. Pelletkessel
   - Leistung: 0-112 kW
   - VL-Temperatur: 56-82°C
   
2. Abwasser-Wärmepumpe (ABW-WP)
   - Leistung: Variable
   - Primär/Sekundär-Kreise
   
3. Abluft-Wärmepumpe (ABL-WP)
   - Leistung: Variable
   - Kältekreis überwacht
```

**Besonderheiten:**
- Durchladeerhitzer (DLE) als Backup
- PV-Anlage auf Haus 15
- Warmwasserspeicher mit Schichtung (WST)

---

## 3. Datenqualitätsmetriken

### 3.1 Vollständigkeit

| Datenquelle | Vollständigkeit | Fehlende Werte | Kommentar |
|-------------|----------------|----------------|-----------|
| Twin²Sim PV | 100% | 0% | Perfekte Zeitreihe |
| Twin²Sim Wetter | 100% | 0% | Lückenlos |
| Twin²Sim Lüftung | 100% | 0% | Komplett |
| Erentrudisstraße | ~95% | 5% | Nachtstunden teilweise |
| F.-Inhauser-Str. | ~70% | 30% | Viele leere Temperaturfelder |

### 3.2 Plausibilität

**Temperaturwerte:**
- Außentemperatur: ✓ Plausibel (Sommer/Winter)
- Vorlauftemperaturen: ✓ Typisch für Systeme
- Rücklauftemperaturen: ✓ Physikalisch korrekt

**Leistungswerte:**
- PV-Erzeugung: ✓ Tagesprofil erkennbar
- Fernwärme: ✓ Lastprofil plausibel
- Lüftung: ✓ Tag/Nacht-Rhythmus

### 3.3 Konsistenz

**Zeitstempel:**
- Format 1: `DD.MM.YYYY HH:MM:SS,fff` (Twin²Sim)
- Format 2: `DD.MM.YYYY HH:MM` (Erentrudisstraße)
- Format 3: `DD.MM.YYYY HH:MM` (F.-Inhauser)

**Einheiten:**
- Inkonsistent zwischen Systemen
- Leistung: W, kW gemischt
- Energie: kWh einheitlich

---

## 4. Datenintegration Herausforderungen

### 4.1 Technische Herausforderungen

1. **Heterogene Datenformate**
   - CSV mit unterschiedlichen Trennzeichen
   - XLSX binär (Kraftwerke)
   - Verschiedene Encoding (UTF-8, ISO-8859-1)

2. **Zeitliche Auflösung**
   - 5-Minuten vs. Stundenwerte
   - Aggregation erforderlich

3. **Namenskonventionen**
   - Deutsch/Englisch gemischt
   - Lange, technische Bezeichnungen
   - Inkonsistente Abkürzungen

### 4.2 Semantische Herausforderungen

1. **Parameterbezeichnungen**
   - Gleiche Größe, verschiedene Namen
   - Mehrdeutige Abkürzungen

2. **Einheitenkonversion**
   - W ↔ kW
   - m³/h für verschiedene Medien

3. **Zeitzonenproblematik**
   - Lokale Zeit vs. UTC
   - Sommer-/Winterzeit

---

## 5. Empfohlene Datenarchitektur

### 5.1 DataMesh-Struktur

```
Domain 1: Gebäudemonitoring
├── Twin²Sim
├── Erentrudisstraße
└── Friedrich-Inhauser-Straße

Domain 2: Energieerzeugung
├── Wasserkraftwerke
└── PV-Anlagen

Domain 3: Umweltdaten
└── Wetterstationen

Domain 4: Netzinteraktion
├── Einspeisung
└── Bezug
```

### 5.2 Datenmodell (vorgeschlagen)

```sql
-- Zeitreihen-Tabelle
CREATE TABLE measurements (
    timestamp TIMESTAMP,
    location_id VARCHAR(50),
    parameter_id VARCHAR(50),
    value FLOAT,
    unit VARCHAR(20),
    quality_flag INT
);

-- Metadaten-Tabelle
CREATE TABLE parameters (
    parameter_id VARCHAR(50),
    name_de VARCHAR(200),
    name_en VARCHAR(200),
    unit VARCHAR(20),
    min_value FLOAT,
    max_value FLOAT,
    description TEXT
);

-- Standort-Tabelle
CREATE TABLE locations (
    location_id VARCHAR(50),
    building_name VARCHAR(100),
    address VARCHAR(200),
    coordinates POINT,
    building_type VARCHAR(50)
);
```

---

## 6. Automatisierungsansätze

### 6.1 Datenimport

```python
# Beispiel Import-Pipeline
import pandas as pd
from pathlib import Path

def import_twin2sim_data(file_path):
    """Import Twin²Sim CSV data"""
    df = pd.read_csv(
        file_path,
        sep=';',
        decimal=',',
        parse_dates=['Date'],
        date_format='%d.%m.%Y %H:%M:%S,%f'
    )
    return df

def harmonize_timestamps(df):
    """Vereinheitlichung auf ISO 8601"""
    df['timestamp'] = pd.to_datetime(df['Date'])
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    return df
```

### 6.2 Qualitätsprüfung

```python
def check_data_quality(df, parameter_config):
    """Datenqualitätsprüfung"""
    issues = []
    
    # Bereichsprüfung
    for param, config in parameter_config.items():
        if param in df.columns:
            out_of_range = df[
                (df[param] < config['min']) | 
                (df[param] > config['max'])
            ]
            if not out_of_range.empty:
                issues.append(f"{param}: {len(out_of_range)} Werte außerhalb Bereich")
    
    # Lückenprüfung
    time_diff = df['timestamp'].diff()
    gaps = time_diff[time_diff > expected_interval]
    if not gaps.empty:
        issues.append(f"Zeitlücken: {len(gaps)} gefunden")
    
    return issues
```

---

## 7. Visualisierungskonzepte

### 7.1 Dashboard-Struktur

**Ebene 1: Übersicht**
- Gesamtenergiebilanz
- CO2-Emissionen
- Einsparungspotenziale

**Ebene 2: Gebäudedetails**
- Einzelgebäude-Performance
- Vergleich Soll/Ist
- Anomalieerkennung

**Ebene 3: Technische Details**
- Anlagenparameter
- Zeitreihen-Analyse
- Fehlerdiagnose

### 7.2 KPI-Definitionen

```
Energieeffizienz = Nutzenergie / Endenergie
CO2-Intensität = CO2-Emissionen / Nutzfläche
Autarkiegrad = Eigenerzeugung / Gesamtverbrauch
Performance Ratio = Ist-Erzeugung / Soll-Erzeugung
```

---

## 8. Sicherheit und Datenschutz

### 8.1 Klassifizierung

| Sicherheitsstufe | Datentyp | Zugriff |
|------------------|----------|---------|
| **Öffentlich** | Aggregierte Kennzahlen | Alle |
| **Intern** | Gebäudedaten anonymisiert | Projektteam |
| **Vertraulich** | Erzeugungsdaten | Partner only |
| **Geheim** | Personenbezogene Daten | Keine vorhanden |

### 8.2 Anonymisierung

- Gebäude-IDs statt Adressen
- Keine Rückschlüsse auf Bewohner
- Aggregation bei < 5 Einheiten

---

## 9. Wartung und Betrieb

### 9.1 Monitoring

- Dateneingang überwachen
- Qualitätsmetriken tracken
- Alarme bei Ausfällen

### 9.2 Backup-Strategie

- Tägliche Backups Rohdaten
- Wöchentliche Backups prozessierte Daten
- Monatliche Archivierung

---

## 10. Roadmap

### Phase 1 (Q3 2025)
- Datenharmonisierung
- Metadaten-Katalog
- Basis-Import-Pipelines

### Phase 2 (Q4 2025)
- DataMesh-Implementation
- Echtzeit-Streaming
- Erste digitale Zwillinge

### Phase 3 (Q1 2026)
- KI-Modelle Training
- Predictive Analytics
- Dashboard Go-Live

### Phase 4 (Q2 2026)
- Skalierung auf 1000 Gebäude
- Federated Learning
- Publikation Ergebnisse

---

*Technische Dokumentation Version 1.0*  
*Stand: 18.08.2025*  
*MokiG Entwicklungsteam*