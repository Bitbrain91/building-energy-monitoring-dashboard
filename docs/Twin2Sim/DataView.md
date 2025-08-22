# Daten-Landschaftskarte MokiG Projekt
## Monitoring für klimaneutrale Gebäude

**Stand:** 18.08.2025  
**Projektname:** MokiG - Monitoring für klimaneutrale Gebäude  
**FFG Projektnummer:** 923166  
**Projektträger:** Fachhochschule Salzburg

---

## 1. Projektübersicht

Das Forschungsprojekt "Monitoring für klimaneutrale Gebäude" (MokiG) zielt darauf ab, den Energieverbrauch und die CO2-Emissionen von Gebäuden durch moderne Monitoring- und Analysetechnologien signifikant zu senken. Das Projekt verfolgt einen innovativen Low-Tech-Ansatz, bei dem vorhandene Sensorik und Gebäudedaten genutzt werden, um digitale Zwillinge zu erstellen und Einsparungspotenziale aufzuzeigen.

### Hauptziele:
- Schaffung einer einheitlichen Datenbasis für KI-Anwendungen
- Aufzeigen von Einsparungspotentialen mit KI-Unterstützung
- Implementierung von Use-Cases an Partner-Gebäuden
- Entwicklung eines Datenraums für Energiedaten
- Wissenstransfer durch Workshops und Publikationen

---

## 2. Datenlandschaft Übersicht

### 2.1 Datenquellen und Anbieter

| Kategorie | Anbieter/Quelle | Region | Datenzeitraum | Datenmenge |
|-----------|-----------------|--------|---------------|------------|
| **Beispieldaten** | Twin²Sim Forschungsgebäude | FH Salzburg | Juni 2025 | 5 CSV-Dateien |
| **Monitoringdaten Gebäude** | | | | |
| - Erentrudisstraße | ECB energy consult | Salzburg Stadt | 2023-2025 | >10 Dateien |
| - Friedrich-Inhauser-Straße | Heimat Österreich | Salzburg Stadt | 2024-2025 | >5 Dateien |
| **Energieerzeugung** | | | | |
| - KW Dürnbach | Lichtgenossenschaft | Neukirchen | 2020-2024 | 5 Jahre |
| - KW Untersulzbach | Lichtgenossenschaft | Neukirchen | 2020-2024 | 5 Jahre |
| - KW Wiesbach | Lichtgenossenschaft | Neukirchen | 2020-2024 | 5 Jahre |
| **Netzübergabe** | Lichtgenossenschaft | Neukirchen | 2020-2024 | Monatsdaten |

---

## 3. Detaillierte Datenanalyse

### 3.1 Beispieldaten (Twin²Sim Forschungsgebäude)

#### Dateiübersicht:
- `T2S_IntPV.csv` - Photovoltaik-Monitoring (Growatt Wechselrichter)
- `T2S_ManiPV.csv` - PV-Anlage Monitoring
- `T2S_Lüftung.csv` - Lüftungsanlage Monitoring
- `T2S_RAU006.csv` - Raummonitoring
- `T2S_Wetterdaten.csv` - Wetterstation Daten

#### Datenstruktur PV-Anlage (T2S_IntPV.csv):
- **Zeitauflösung:** Stündliche Werte
- **Zeitraum:** 23.06.2025 - 24.06.2025 (Beispielzeitraum)
- **Messgrößen:**
  - Eingangsleistung (W)
  - Ausgangsleistung (W)
  - Netzfrequenz (Hz)
  - Tageserzeugung (kWh)
  - Gesamterzeugung (kWh)
  - Betriebsstunden
  - Wechselrichtertemperatur (°C)

#### Datenstruktur Wetterstation (T2S_Wetterdaten.csv):
- **Zeitauflösung:** Stündliche Werte
- **Messgrößen:**
  - Windgeschwindigkeit (m/s, km/h)
  - Relative Luftfeuchte (%)
  - Luftdruck (hPa)
  - Windrichtung (°)
  - Niederschlagsart und -intensität
  - Globalstrahlung (W/m²)
  - Lufttemperatur (°C)
  - Taupunkt (°C)

#### Datenstruktur Lüftungsanlage (T2S_Lüftung.csv):
- **Zeitauflösung:** Stündliche Werte
- **Messgrößen:** 42 Parameter
  - Temperaturen (Zuluft, Abluft, Außenluft, Fortluft)
  - Feuchtigkeitswerte
  - Druckwerte
  - Ventilatorbetrieb
  - Wärmerückgewinnung
  - Heiz-/Kühlregister

### 3.2 Monitoringdaten Erentrudisstraße

#### Gebäudedaten:
- **Gebäudetyp:** Mehrfamilienhaus
- **Stockwerke:** UG, EG, 1-4 OG
- **Energieversorgung:** Fernwärme, Warmwasserbereitung
- **Dokumentation:** Energieausweis vorhanden (gültig bis 04.06.2025)

#### Monitoring 2024:
- **Datei:** `Relevant_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59.csv`
- **Zeitauflösung:** 5-Minuten-Intervalle
- **Messgrößen:**
  - Durchfluss Fernwärme (m³/h)
  - Temperaturen (Vorlauf/Rücklauf)
  - Zählerstände (kWh)
  - Leistung (W)
  - Zirkulation
  - Warmwasser
  - Kaltwasser

#### Datenqualität:
- Kontinuierliche Aufzeichnung
- Teilweise Datenlücken in Nachtstunden
- Plausible Wertebereiche

### 3.3 Monitoringdaten Friedrich-Inhauser-Straße

#### Gebäudekomplex:
- **Häuser:** 1, 3, 5, 7, 9, 11, 13, 15
- **Besonderheit:** Innovationsgebäude "Wir-InHAUSer"
- **Monitoring:** Umfangreiches Monitoring-System

#### Dateistruktur (export_1551):
- **Zeitauflösung:** 5-Minuten-Intervalle
- **Zeitraum:** 31.12.2024 - 31.03.2025
- **Messgrößen:** >100 Parameter
  - Stromzähler je Haus und Lüftungsgerät
  - Kältezähler je Haus
  - Wärmepumpen (Abwasser-WP, Abluft-WP)
  - Pelletkessel
  - PV-Anlage Haus 15
  - Temperaturen (Vor-/Rücklauf)
  - Durchflussmengen

#### Datenqualität:
- Sehr umfangreiches Monitoring
- Teilweise fehlende Werte (leere Zellen)
- Unterschiedliche Zeitstempel-Formate

### 3.4 Energieerzeugungsdaten Kraftwerke

#### Kraftwerke:
1. **KW Dürnbach**
2. **KW Untersulzbach** 
3. **KW Wiesbach**

#### Datenstruktur:
- **Format:** Excel-Dateien (.XLSX)
- **Zeitraum:** 2020-2024 (5 Jahre komplett)
- **Auflösung:** Vermutlich Stundenwerte
- **Inhalt:** Erzeugungsdaten (kWh)

#### Netzübergabedaten:
- **ÜBERGABE_BEZUG:** Strombezug aus dem Netz
- **ÜBERGABE_LIEFERUNG:** Stromeinspeisung ins Netz
- **Auflösung:** Monatliche Dateien
- **Zeitraum:** 2020-2024

---

## 4. Datenfrequenzen und Intervalle

| Datenquelle | Messintervall | Aggregation | Verfügbarkeit |
|-------------|---------------|-------------|---------------|
| Twin²Sim PV-Anlage | 1 Stunde | Stundenwerte | Kontinuierlich |
| Twin²Sim Wetterstation | 1 Stunde | Stundenwerte | Kontinuierlich |
| Twin²Sim Lüftung | 1 Stunde | Stundenwerte | Kontinuierlich |
| Erentrudisstraße | 5 Minuten | 5-Min-Werte | Kontinuierlich |
| Friedrich-Inhauser-Str. | 5 Minuten | 5-Min-Werte | Mit Lücken |
| Kraftwerke | Vermutlich 1 Stunde | Monatsdateien | Monatlich |

---

## 5. Datenqualität und Vollständigkeit

### 5.1 Identifizierte Herausforderungen:

#### Fehlende Werte:
- Friedrich-Inhauser-Straße: Viele Parameter zeigen zeitweise keine Werte
- Teilweise nur Temperaturwerte ohne korrespondierende Leistungswerte
- Nachtstunden oft mit reduzierten Datensätzen

#### Datenformate:
- Unterschiedliche CSV-Trennzeichen (Semikolon vs. Komma)
- Verschiedene Datumsformate
- Dezimaltrennzeichen inkonsistent

#### Plausibilität:
- Temperaturwerte im erwarteten Bereich (0-40°C)
- Leistungswerte plausibel
- Wetterstation zeigt realistische Werte

### 5.2 Empfehlungen zur Datenharmonisierung:

1. **Vereinheitlichung der Zeitstempel**
   - ISO 8601 Format empfohlen
   - Einheitliche Zeitzone (UTC oder lokale Zeit)

2. **Standardisierung der Einheiten**
   - Leistung: kW
   - Energie: kWh
   - Temperatur: °C
   - Durchfluss: m³/h

3. **Behandlung fehlender Werte**
   - Kennzeichnung mit einheitlichem NULL-Wert
   - Interpolation bei kurzen Lücken
   - Dokumentation von Ausfällen

---

## 6. Datenvolumen und Speicherbedarf

### Geschätztes Datenvolumen:

| Kategorie | Anzahl Dateien | Geschätztes Volumen |
|-----------|----------------|---------------------|
| Beispieldaten | 5 CSV | ~5 MB |
| Monitoring Erentrudisstraße | >15 Dateien | ~50 MB |
| Monitoring F.-Inhauser-Str. | >10 Dateien | ~30 MB |
| Kraftwerksdaten | 60 XLSX | ~200 MB |
| **Gesamt** | **~90 Dateien** | **~285 MB** |

### Wachstumsrate:
- Täglicher Zuwachs: ~1-2 MB
- Monatlicher Zuwachs: ~30-60 MB
- Jährlicher Zuwachs: ~400-700 MB

---

## 7. Technische Integration

### 7.1 DataMesh-Architektur

Das Projekt nutzt eine innovative DataMesh-Architektur zur Organisation der heterogenen Datenquellen:

- **Domänen:** Gebäudemonitoring, Energieerzeugung, Wetterda |
- **Dezentrale Datenautonomie**
- **Self-Service-Zugriff**
- **Metadatenmanagement**

### 7.2 Digitaler Zwilling

Entwicklung digitaler Zwillinge für:
- Einzelgebäude
- Gebäudekomplexe
- Energieerzeugungsanlagen

### 7.3 KI-Integration

- Federated Learning für datenschutzkonforme Analysen
- Vorhersagemodelle für Energieverbrauch
- Anomalieerkennung
- Optimierungsvorschläge

---

## 8. Datenschutz und Sicherheit

### Vertrauliche Daten:
- Energieerzeugungsdaten sind als "vertraulich" gekennzeichnet
- Personenbezogene Daten sind anonymisiert
- Gebäudespezifische Daten nur für Projektpartner

### Zugriffsrechte:
- Projektpartner: Vollzugriff
- Assoziierte Partner: Zugriff auf eigene Gebäudedaten
- Öffentlichkeit: Nur aggregierte, anonymisierte Daten

---

## 9. Nutzungspotenziale

### Forschung:
- Entwicklung von Vorhersagemodellen
- Benchmarking von Gebäuden
- Identifikation von Einsparpotenzialen

### Praxis:
- Echtzeit-Monitoring für Gebäudebetreiber
- Frühwarnsystem für Anlagenausfälle
- Optimierung der Betriebsführung

### Wissenstransfer:
- Best-Practice-Beispiele
- Schulungen für Facility Manager
- Publikationen und Workshops

---

## 10. Nächste Schritte

1. **Datenharmonisierung**
   - Entwicklung einheitlicher Datenstandards
   - Implementierung von Datenvalidierung

2. **Datenraum-Entwicklung**
   - Aufbau der DataMesh-Infrastruktur
   - Integration aller Datenquellen

3. **Digitale Zwillinge**
   - Modellierung der Pilotgebäude
   - Kalibrierung mit Realdaten

4. **Dashboard-Entwicklung**
   - Visualisierung der Energieflüsse
   - Echtzeit-Monitoring
   - Alarmfunktionen

---

## Anhang: Technische Details

### CSV-Struktur Beispiel (Trennzeichen: Semikolon)
```csv
Date;Parameter1;Parameter2;...
23.06.2025 00:00:00,000;Wert1;Wert2;...
```

### Koordinaten Projektgebiet
- Region: Salzburg und Pinzgau
- Hauptstandorte: Salzburg Stadt, Neukirchen

### Projektpartner
- Fachhochschule Salzburg (Projektleitung)
- Meshmakers GmbH
- Unbuzz Consulting
- ECB energy consult business gmbh
- Heimat Österreich (assoziiert)
- Lichtgenossenschaft Neukirchen (assoziiert)

---

*Dokumentversion: 1.0*  
*Erstellt: 18.08.2025*  
*Autor: MokiG Projektteam*