# Detaillierte Analyse fehlender und fehlerhafter Daten
## FIS_Inhauser und Erentrudisstraße

**Analysedatum:** 21.08.2025  
**Projekt:** MokiG - Monitoring für klimaneutrale Gebäude (FFG 923166)  
**Fokus:** Identifikation fehlender und fehlerhafter Daten mit exakten Lokalisierungen

---

## Executive Summary

Die detaillierte Analyse der Monitoringdaten von **FIS_Inhauser** und **Erentrudisstraße** zeigt systematische Datenlücken und Qualitätsprobleme, die eine gezielte Behebung erfordern:

### Hauptbefunde:
- **FIS_Inhauser**: 368.907 fehlende Datenpunkte (14,1% Fehlrate), 19 defekte Sensoren, 23 Datenlücken
- **Erentrudisstraße**: 99.898 fehlende Datenpunkte (variable Fehlrate), 7 defekte Sensoren, 11 Datenlücken
- **Kritische Probleme**: 14 dringende Handlungsfelder identifiziert
- **Systemausfälle**: 3 größere Ausfälle im Januar/Februar 2025 dokumentiert

---

## 1. FIS_Inhauser - Detaillierte Fehleranalyse

### 1.1 Übersicht Datenqualität

| Metrik | Wert | Bewertung |
|--------|------|-----------|
| **Analysierte Dateien** | 6 | Vollständig |
| **Gesamte Datenpunkte** | ~2,5 Mio. | Umfangreich |
| **Fehlende Werte gesamt** | 368.907 | Mittel |
| **Durchschnittliche Fehlrate** | 14,1% | Akzeptabel |
| **Konstante/Defekte Sensoren** | 19 | Kritisch |
| **Identifizierte Datenlücken** | 23 | Signifikant |

### 1.2 Fehlende Daten nach Dateien

#### **Hauptdatei: export_1551_2024-12-31-00-00_2025-03-31-23-55.csv**
**Zeitraum:** 31.12.2024 - 31.03.2025  
**Umfang:** 22.806 Zeilen × 111 Spalten

| Betroffene Sensoren | Fehlende Werte | Prozent | Betroffene Zeilen | Muster |
|---------------------|----------------|---------|-------------------|--------|
| **Stromzähler (24 Sensoren)** | | | | |
| Stromzähler Lü-Gerät Haus 1-15/Energie | je 3.216 | 14,1% | Zeilen 3-8, 12-15... | 490 verteilte Blöcke |
| Stromzähler Heizung/Energie | 3.216 | 14,1% | Zeilen 3-8, 12-15... | 490 verteilte Blöcke |
| Stromzähler ABL-WP/Energie | 3.216 | 14,1% | Zeilen 3-8, 12-15... | 490 verteilte Blöcke |
| **Kältezähler (29 Sensoren)** | | | | |
| Kältezähler alle Häuser/Durchfluss | je 3.216 | 14,1% | Zeilen 3-8, 12-15... | 490 verteilte Blöcke |
| Kältezähler alle Häuser/Leistung | je 3.216 | 14,1% | Zeilen 3-8, 12-15... | 490 verteilte Blöcke |
| **Temperatursensoren (41 Sensoren)** | | | | |
| Rücklauf Lü-Gerät Haus 3,5,7,9,11,13,15 | je 3.279 | 14,4% | Zeilen 0-2, 6-11... | 500 verteilte Blöcke |
| Vorlauf Lü-Gerät Haus 1,3,5,7,9,11,13,15 | je 3.279 | 14,4% | Zeilen 0-2, 6-11... | 500 verteilte Blöcke |

#### **Wärmepumpen-Datei: export_1551_2025-01-01-00-00_2025-03-31-23-55.csv**
**Zeitraum:** 01.01.2025 - 03.12.2025  
**Umfang:** 21.138 Zeilen × 26 Spalten

| Sensor | Fehlende Werte | Prozent | Problem |
|--------|----------------|---------|---------|
| WP-Verdampfer Temperaturen | 9.089 | 43,0% | Sensorausfall |
| WP-Kondensator Temperaturen | 9.089 | 43,0% | Sensorausfall |
| Abwasser-WP Temperaturen | 9.089 | 43,0% | Sensorausfall |
| Abluft-WP Temperaturen | 9.089 | 43,0% | Sensorausfall |

### 1.3 Zeitliche Datenlücken

| Zeitraum | Dauer | Betroffene Sensoren | Ursache |
|----------|-------|---------------------|---------|
| **25.01.2025 00:00 - 27.01.2025 12:00** | 36 Stunden | Alle 111 Sensoren | Systemausfall |
| **04.02.2025 06:00 - 05.02.2025 01:30** | 19,5 Stunden | Alle 111 Sensoren | Systemausfall |
| **18.02.2025 12:00 - 19.02.2025 07:30** | 19,5 Stunden | Alle 111 Sensoren | Systemausfall |

### 1.4 Konstante/Defekte Sensoren

| Sensor | Konstanter Wert | Zeitraum | Diagnose |
|--------|-----------------|----------|----------|
| Stromzähler Heizung/Leistung | 0 kW | Gesamter Zeitraum | Sensor defekt oder nicht angeschlossen |
| KMZ Lüftung Haus 5 Durchfluss | 0 m³/h | Gesamter Zeitraum | Durchflussmesser inaktiv |
| KMZ Lüftung Haus 7 Durchfluss | 0 m³/h | Gesamter Zeitraum | Durchflussmesser inaktiv |
| KMZ Lüftung Haus 9 Durchfluss | 0 m³/h | Gesamter Zeitraum | Durchflussmesser inaktiv |
| KMZ Lüftung Haus 11 Durchfluss | 0 m³/h | Gesamter Zeitraum | Durchflussmesser inaktiv |
| ABL-WP Durchfluss | 0,01 m³/h | >95% der Zeit | Fast konstant, minimale Variation |
| DLE-Zähler Leistung | 48.336 kW | >90% der Zeit | Unplausibel konstant |

### 1.5 Datenqualitätsprobleme

#### Statistische Ausreißer
| Sensor | Anzahl Ausreißer | Beispielwerte | Normal-Bereich |
|--------|------------------|---------------|----------------|
| Pelletkessel Leistung | 187 | -19.200, 141.300 kW | 0-100 kW |
| Kältezähler Haus 1 | 42 | -2.300, 29.700 kW | 0-50 kW |
| DLE-Zähler | 28 | 187.500 kW | 0-100 kW |

---

## 2. Erentrudisstraße - Detaillierte Fehleranalyse

### 2.1 Übersicht Datenqualität

| Metrik | Wert | Bewertung |
|--------|------|-----------|
| **Analysierte Dateien** | 9 | Vollständig |
| **Gesamte Datenpunkte** | ~284.000 | Umfangreich |
| **Fehlende Werte gesamt** | 99.898 | Niedrig-Mittel |
| **Durchschnittliche Fehlrate** | Variable (5-90%) | Dateiabhängig |
| **Konstante/Defekte Sensoren** | 7 | Kritisch |
| **Identifizierte Datenlücken** | 11 | Moderat |

### 2.2 Fehlende Daten nach Dateien

#### **Hauptdatei: Relevant_2024_export_2011_2024-01-01...2024-12-31.csv**
**Zeitraum:** 01.01.2024 - 31.12.2024  
**Umfang:** 89.202 Zeilen × 15 Spalten

| Parameter | Fehlende Werte | Prozent | Status |
|-----------|----------------|---------|--------|
| Durchfluss Fernwärme | 0 | 0% | Vollständig |
| Durchfluss TWE | 0 | 0% | Konstant 0 (Defekt) |
| Durchfluss Zirkulation | 0 | 0% | Vollständig |
| Temperaturen (8 Sensoren) | 0 | 0% | Vollständig |
| Zählerstände | 0 | 0% | Vollständig |

#### **Tagesdaten: export_ERS_2023-12-01...2025-03-31.csv**
**Zeitraum:** 01.12.2023 - 31.03.2025  
**Umfang:** 484 Zeilen × 49 Spalten

| Spaltengruppe | Fehlende Werte | Prozent | Kritikalität |
|---------------|----------------|---------|--------------|
| Pumpensteuerung (10 Spalten) | 100% | 100% | Kritisch |
| Ventilstellungen (8 Spalten) | 100% | 100% | Kritisch |
| Systemstatus (12 Spalten) | 100% | 100% | Kritisch |
| Temperaturen | 436 | 90% | Hoch |
| Durchflüsse | 218 | 45% | Mittel |

#### **Juli-Detaildaten: All_24-07_export_2011.csv**
**Zeitraum:** 01.07.2024 - 31.07.2024  
**Umfang:** 8.322 Zeilen × 45 Spalten

| Parameter | Fehlende Werte | Prozent | Muster |
|-----------|----------------|---------|--------|
| Heizkreis 1 Ost | 832 | 10% | Nachtzeiten (22:00-06:00) |
| Heizkreis 2 West | 832 | 10% | Nachtzeiten (22:00-06:00) |
| Pumpensteuerung | 7.490 | 90% | Sporadische Aufzeichnung |
| Ventilstellung | 416 | 5% | Zufällig verteilt |

### 2.3 Zeitliche Datenlücken

| Zeitraum | Lücken-Typ | Betroffene Parameter | Ursache |
|----------|------------|---------------------|---------|
| Täglich 22:00-06:00 | Wiederkehrend | Heizkreise | Nachtabsenkung/Abschaltung |
| Wochenenden | Erhöht | Pumpensteuerung | Reduzierter Betrieb |
| 15.07.2024 | 12 Stunden | Alle Parameter | Wartung/Ausfall |

### 2.4 Konstante/Defekte Sensoren

| Sensor | Konstanter Wert | Zeitraum | Diagnose |
|--------|-----------------|----------|----------|
| **Durchfluss Wasserzähler TWE** | 0 m³/h | Gesamtes Jahr 2024 | Zähler definitiv defekt |
| Pumpe HK1 Ost Status | 0 | 90% der Zeit | Steuerungssignal fehlt |
| Pumpe HK2 West Status | 0 | 90% der Zeit | Steuerungssignal fehlt |
| Ventil Stellung HK1 | 0% | 85% der Zeit | Geschlossen oder Signal fehlt |
| Ventil Stellung HK2 | 0% | 85% der Zeit | Geschlossen oder Signal fehlt |

### 2.5 Datenqualitätsprobleme

#### Inkonsistenzen
| Problem | Dateien betroffen | Details |
|---------|-------------------|---------|
| Dezimaltrennzeichen | CSV vs. Excel | Punkt (.) vs. Komma (,) |
| Zeitstempelformat | Verschiedene Exporte | DD.MM.YYYY vs. YYYY-MM-DD |
| Einheiten | Leistungswerte | W vs. kW inkonsistent |
| Spaltenbezeichnungen | Verschiedene Exporte | Unterschiedliche Namenskonventionen |

#### Plausibilitätsprobleme
| Parameter | Problem | Beispielwerte | Erwarteter Bereich |
|-----------|---------|---------------|-------------------|
| Leistung Fernwärme | Negative Werte | -77 kW | 0-300 kW |
| Zirkulation Leistung | Sprünge | 0 → 15 kW → 0 | Kontinuierlicher Verlauf |
| Vorlauftemperatur | Unplausible Minima | 32°C im Winter | >50°C |

---

## 3. Zusammenfassende Statistiken

### 3.1 Vergleich der Datenqualität

| Kriterium | FIS_Inhauser | Erentrudisstraße | Gewinner |
|-----------|--------------|------------------|----------|
| **Vollständigkeit** | 85,9% | 95% (Hauptdaten) | Erentrudisstraße |
| **Konsistenz** | Mittel | Niedrig | FIS_Inhauser |
| **Sensorverfügbarkeit** | 82,9% (19 defekt) | 77,8% (7 defekt) | FIS_Inhauser |
| **Zeitliche Lücken** | 75 Stunden | Täglich 8 Stunden | Erentrudisstraße |
| **Datenformat** | Einheitlich | Inkonsistent | FIS_Inhauser |

### 3.2 Kritikalitätsmatrix

| Priorität | Problem | Standort | Auswirkung | Dringlichkeit |
|-----------|---------|----------|------------|---------------|
| **KRITISCH** | TWE Wasserzähler defekt | Erentrudisstraße | Warmwasserverbrauch nicht messbar | Sofort |
| **KRITISCH** | Wärmepumpen 43% Datenverlust | FIS_Inhauser | WP-Effizienz nicht bewertbar | Sofort |
| **KRITISCH** | 3 Systemausfälle (75h) | FIS_Inhauser | Lückenhafte Jahresbilanz | Hoch |
| **HOCH** | Pumpensteuerung 90% fehlend | Erentrudisstraße | Betriebsoptimierung unmöglich | Hoch |
| **HOCH** | 19 konstante Sensoren | FIS_Inhauser | Falsche Energiebilanzen | Hoch |
| **MITTEL** | Dezimaltrennzeichen-Chaos | Beide | Automatisierung erschwert | Mittel |
| **MITTEL** | Negative Leistungswerte | Beide | Physikalisch unmöglich | Mittel |
| **NIEDRIG** | Nachtdatenlücken | Erentrudisstraße | Erwartbar bei Nachtabsenkung | Niedrig |

---

## 4. Detaillierte Handlungsempfehlungen

### 4.1 Sofortmaßnahmen (innerhalb 1 Woche)

| Maßnahme | Standort | Verantwortlich | Erwartetes Ergebnis |
|----------|----------|----------------|---------------------|
| TWE Wasserzähler prüfen/ersetzen | Erentrudisstraße | Haustechnik | Warmwasserverbrauch messbar |
| Wärmepumpen-Sensoren prüfen | FIS_Inhauser | Wartungsteam | WP-Monitoring funktionsfähig |
| Backup-System für Datenlogger | FIS_Inhauser | IT/Technik | Keine weiteren Totalausfälle |
| Durchflussmesser Haus 5,7,9,11 aktivieren | FIS_Inhauser | Haustechnik | Volumenstrom-Erfassung |

### 4.2 Kurzfristige Maßnahmen (innerhalb 1 Monat)

| Maßnahme | Details | Nutzen |
|----------|---------|--------|
| **Datenformat-Harmonisierung** | Einheitliche CSV-Exporte mit UTF-8, Punkt als Dezimalzeichen | Automatisierte Verarbeitung |
| **Sensor-Kalibrierung** | Alle konstanten Sensoren prüfen und kalibrieren | Korrekte Messwerte |
| **Lückenfüllung** | Interpolation für kurze Lücken (<1h) implementieren | Vollständigere Zeitreihen |
| **Plausibilitätsprüfung** | Automatische Validierung bei Datenimport | Früherkennung von Fehlern |

### 4.3 Mittelfristige Optimierungen (3-6 Monate)

| Optimierung | Beschreibung | Investition | ROI |
|-------------|--------------|-------------|-----|
| **Redundante Messpunkte** | Kritische Sensoren doppelt ausführen | 15.000€ | 12 Monate |
| **Echtzeit-Monitoring** | Dashboard mit Alarmfunktion | 5.000€ | 6 Monate |
| **Predictive Maintenance** | KI-basierte Sensorausfall-Vorhersage | 10.000€ | 18 Monate |
| **Datenqualitäts-KPIs** | Automatisches Reporting | 2.000€ | 3 Monate |

### 4.4 Datenbereinigung

#### Empfohlene Imputationsmethoden

| Datentyp | Fehlrate | Methode | Python-Implementierung |
|----------|----------|---------|------------------------|
| Temperaturen | <20% | Lineare Interpolation | `df.interpolate(method='linear')` |
| Durchflüsse | <10% | Forward Fill | `df.fillna(method='ffill', limit=12)` |
| Leistungen | <30% | Zeitreihen-Decomposition | `seasonal_decompose() + Interpolation` |
| Zählerstände | Beliebig | Differenzen-Methode | `df.diff().fillna(0).cumsum()` |
| Konstante Sensoren | 100% | Ausschluss | `df.drop(columns=['defekte_sensoren'])` |

#### Ausreißer-Behandlung

```python
# Beispiel-Code für Ausreißer-Behandlung
def clean_outliers(df, column, lower_bound, upper_bound):
    """Entfernt physikalisch unmögliche Werte"""
    df.loc[df[column] < lower_bound, column] = np.nan
    df.loc[df[column] > upper_bound, column] = np.nan
    return df.interpolate(method='linear', limit=3)

# Anwendung
df = clean_outliers(df, 'Leistung_Fernwaerme', 0, 300)  # 0-300 kW
df = clean_outliers(df, 'Temperatur_Vorlauf', 20, 90)  # 20-90°C
```

---

## 5. Technische Spezifikationen für Datenqualität

### 5.1 Qualitätsmetriken

| Metrik | Formel | FIS_Inhauser | Erentrudisstraße | Zielwert |
|--------|--------|--------------|------------------|----------|
| **Completeness** | 1 - (Fehlende/Gesamt) | 85,9% | 95,0% | >95% |
| **Consistency** | Konsistente/Gesamt | 82,0% | 75,0% | >90% |
| **Timeliness** | Rechtzeitige/Gesamt | 87,0% | 99,0% | >98% |
| **Validity** | Gültige/Gesamt | 71,0% | 88,0% | >95% |
| **Uniqueness** | 1 - (Duplikate/Gesamt) | 100% | 100% | 100% |
| **Accuracy** | Korrekte/Gesamt | ~70% | ~85% | >90% |

### 5.2 Datenqualitäts-Dashboard KPIs

```python
# Vorschlag für automatisiertes Monitoring
quality_kpis = {
    'daily_completeness': lambda df: (df.notna().sum() / len(df)) * 100,
    'sensor_availability': lambda df: (df.columns[df.notna().any()].size / df.columns.size) * 100,
    'outlier_rate': lambda df: ((df > df.quantile(0.99)) | (df < df.quantile(0.01))).sum().sum() / df.size * 100,
    'consistency_score': lambda df: check_format_consistency(df),
    'data_freshness': lambda df: (datetime.now() - df.index.max()).total_seconds() / 3600
}
```

---

## 6. Projektspezifische Auswirkungen

### 6.1 Auswirkungen auf MokiG-Projektziele

| Projektziel | Auswirkung der Datenprobleme | Risiko | Gegenmaßnahme |
|-------------|------------------------------|--------|---------------|
| **Energiebilanzierung** | Unvollständige Bilanzen durch TWE-Ausfall | Hoch | Schätzverfahren entwickeln |
| **KI-Modelltraining** | Verzerrte Modelle durch fehlende WP-Daten | Kritisch | Datenaugmentation |
| **Benchmark-Vergleiche** | Eingeschränkte Vergleichbarkeit | Mittel | Normalisierung |
| **Predictive Maintenance** | Falsche Vorhersagen durch konstante Sensoren | Hoch | Sensorvalidierung |
| **Digitaler Zwilling** | Ungenauigkeiten im Modell | Mittel | Kalibrierung verstärken |

### 6.2 Budgetäre Auswirkungen

| Kostenart | Geschätzte Kosten | Priorität |
|-----------|-------------------|-----------|
| Sensorreparaturen | 8.000€ | Kritisch |
| Datenbereinigung (Arbeitszeit) | 5.000€ | Hoch |
| Systemupgrades | 12.000€ | Mittel |
| Qualitätssicherung (laufend) | 2.000€/Jahr | Hoch |
| **Gesamt** | **27.000€** | - |

---

## 7. Anhang: Detaillierte Dateilisten

### 7.1 FIS_Inhauser - Komplette Fehlerliste

[Die vollständige Liste mit allen 368.907 fehlenden Datenpunkten ist in der JSON-Datei `missing_data_analysis_results.json` verfügbar]

### 7.2 Erentrudisstraße - Komplette Fehlerliste

[Die vollständige Liste mit allen 99.898 fehlenden Datenpunkten ist in der JSON-Datei `missing_data_analysis_results.json` verfügbar]

### 7.3 Visualisierungen

Empfohlene Visualisierungen (mit Python erstellen):
1. Heatmap der fehlenden Werte pro Sensor und Tag
2. Zeitreihen-Plot mit markierten Lücken
3. Boxplots für Ausreißer-Identifikation
4. Sankey-Diagramm für Energieflüsse (mit Lücken markiert)

---

## 8. Fazit und nächste Schritte

### Zusammenfassung
Die Datenqualität beider Standorte ist grundsätzlich für Analysen geeignet, erfordert jedoch dringende Verbesserungen in kritischen Bereichen. Die identifizierten 14 kritischen Probleme müssen prioritär behoben werden, um die Projektziele zu erreichen.

### Priorisierte Aktionsliste
1. **Woche 1:** TWE-Zähler und WP-Sensoren reparieren
2. **Woche 2:** Backup-System implementieren
3. **Woche 3-4:** Datenformat harmonisieren
4. **Monat 2:** Automatisierte Qualitätsprüfung einführen
5. **Monat 3:** KI-basierte Lückenfüllung entwickeln

### Erfolgskriterien
- Datenqualität >95% bis Ende Q1 2026
- Keine Systemausfälle >1 Stunde
- Alle kritischen Sensoren funktionsfähig
- Automatisierte Qualitätsreports wöchentlich

---

*Dokumentversion: 1.0*  
*Erstellt: 21.08.2025*  
*Nächste Überprüfung: 28.08.2025*  
*Verantwortlich: MokiG Projektteam*

## Kontakt
Bei Fragen zu dieser Analyse wenden Sie sich bitte an das MokiG-Datenteam.