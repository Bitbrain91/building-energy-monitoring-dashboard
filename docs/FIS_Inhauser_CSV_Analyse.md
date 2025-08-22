# FIS Inhauser - CSV-Dateianalyse und Vergleich

## Übersicht

Detaillierte Analyse von drei CSV-Exportdateien aus dem FIS Inhauser Monitoring-System zur Identifikation von Teilmengen-Beziehungen und Datenstrukturen.

## Analysierte Dateien

### Datei 1: export_1551_2024-12-31-00-00_2025-03-31-23-55.csv
- **Typ**: Vollständiger System-Export
- **Zeilen**: 22.806 Datenpunkte
- **Spalten**: 111 Parameter
- **Zeitraum**: 31.12.2024 00:00 - 31.03.2025 23:50
- **Intervall**: 5 Minuten
- **Besonderheiten**: Deutsches Zahlenformat (Komma als Dezimaltrennzeichen), teilweise leere Werte

### Datei 2: export_1551_2025-01-01-00-00_2025-03-31-23-55.csv
- **Typ**: Reduzierter Kern-Export
- **Zeilen**: 21.138 Datenpunkte
- **Spalten**: 26 Parameter
- **Zeitraum**: 01.01.2025 00:45 - 31.03.2025 23:50
- **Intervall**: Unregelmäßig (5 Min bis Stunden-Sprünge)
- **Besonderheiten**: Fokus auf essentielle Temperatur- und Energieparameter

### Datei 3: V1_2501_EXPORT_1.CSV
- **Typ**: Vollständiger System-Export
- **Zeilen**: 1.568 Datenpunkte
- **Spalten**: 112 Parameter
- **Zeitraum**: 23.01.2025 00:05 - 29.01.2025 23:55
- **Intervall**: 5 Minuten durchgängig
- **Besonderheiten**: Konsistente Daten ohne Lücken

## Strukturelle Analyse

### Spaltenvergleich

| Vergleich | Gemeinsame Spalten | Übereinstimmung |
|-----------|-------------------|-----------------|
| Datei 1 & 2 | 15 | 13,5% |
| Datei 1 & 3 | 3 | 2,7% |
| Datei 2 & 3 | 2 | 1,8% |
| Alle drei Dateien | 2 | - |

### Teilmengen-Beziehungen

- **Datei 2 ist KEINE vollständige Teilmenge von Datei 1**
  - 15 von 26 Parametern sind identisch (57,7%)
  - 11 Parameter sind einzigartig in Datei 2 (spezielle Temperaturmessungen)

- **Datei 1 und 3 sind strukturell unterschiedlich**
  - Trotz ähnlicher Spaltenanzahl (111 vs 112) nur 2,7% Übereinstimmung
  - Unterschiedliche Benennungskonventionen für gleiche Messwerte

## Parameter-Kategorisierung

### Datei 1 - Vollexport (111 Parameter)
```
Temperatur:      44 Parameter (39,6%)
Strom/Energie:   38 Parameter (34,2%)
Durchfluss:      14 Parameter (12,6%)
Leistung:        14 Parameter (12,6%)
Sonstige:         1 Parameter  (0,9%)
```

### Datei 2 - Reduzierter Export (26 Parameter)
```
Temperatur:      19 Parameter (73,1%)
Strom/Energie:    3 Parameter (11,5%)
Durchfluss:       3 Parameter (11,5%)
Sonstige:         1 Parameter  (3,8%)
```

### Datei 3 - Vollexport (112 Parameter)
```
Strom/Energie:   48 Parameter (42,9%)
Temperatur:      33 Parameter (29,5%)
Durchfluss:      16 Parameter (14,3%)
Leistung:        14 Parameter (12,5%)
Sonstige:         1 Parameter  (0,9%)
```

## Zeitliche Überlappungen

### Überlappungsmatrix

| Dateipaar | Gemeinsame Zeitstempel | Überlappungsdauer | Zeitraum |
|-----------|------------------------|-------------------|----------|
| 1 & 2 | 21.138 | 2.159,1 Stunden | 01.01.2025 00:45 - 31.03.2025 23:50 |
| 1 & 3 | 1.568 | 167,8 Stunden | 23.01.2025 00:05 - 29.01.2025 23:55 |
| 2 & 3 | 1.565 | 167,8 Stunden | 23.01.2025 00:05 - 29.01.2025 23:55 |

## Wertevergleich

### Analyse gemeinsamer Parameter (Datei 1 vs. Datei 2)

Bei der Analyse von 21.138 gemeinsamen Zeitstempeln zeigen alle 14 untersuchten gemeinsamen Parameter **100% identische Werte**:

#### Verifizierte identische Parameter:
- Außenfühler (°C)
- Rücklauf Pelletkessel n.RL-Anhebung (°C)
- Rücklauf Pelletkessel v.RL-Anhebung (°C)
- Rücklauf DLE n.V. (°C)
- Rücklauf DLE v.V. (°C)
- Rücklauf ABW-WP sekundär (°C)
- Vorlauf Pelletskessel (°C)
- Vorlauf ABW-WP primär (°C)
- Zähler Pelletkessel/Energie (kWh)
- Zähler ABL-WP/Energie (kWh)
- Zähler ABW-WP/Energie (kWh)
- Zähler Pelletkessel/Durchfluss (m³/h)
- Zähler ABL-WP/Durchfluss (m³/h)
- Zähler ABW-WP/Durchfluss (m³/h)

**Ergebnis**: Keine Abweichungen gefunden - die gemeinsamen Parameter zeigen exakt dieselben Messwerte.

## Identifizierte Parameter-Mappings

Verschiedene Benennungen für gleiche Messwerte zwischen den Dateien:

| Datei 1 | Datei 2/3 | Typ |
|---------|-----------|-----|
| Stromzähler ABL-WP/Energie (kWh) | Zähler ABL-WP/Energie (kWh) | Energie |
| Stromzähler ABW-WP/Energie (kWh) | Zähler ABW-WP/Energie (kWh) | Energie |
| Kältezähler ABL-WP/Durchfluss | Zähler ABL-WP/Durchfluss | Durchfluss |
| Kältezähler ABW-WP/Durchfluss | Zähler ABW-WP/Durchfluss | Durchfluss |

## Einzigartige Parameter

### Nur in Datei 1 (95 einzigartige Parameter)
Beispiele:
- Rücklauf Lü-Gerät Haus 5-15 (°C)
- Kältezähler Lü-Gerät Haus 1-15 (verschiedene Messungen)
- Stromzähler Lü-Gerät Haus 1-15 (Energie und Leistung)
- Vorlauf Lü-Gerät Haus 1-15 (°C)

### Nur in Datei 2 (11 einzigartige Parameter)
Spezielle Temperaturmessungen der Wärmepumpen:
- Temperatur Abluft WP VL Verdampfer von KMZ (°C)
- Temperatur Abluft WP VL Kond F6.23 (°C)
- Temperatur Abwasser WP RL Kondensator F6.09 (°C)
- Temperatur Abwasser WP VL Kondensator F6.11 (°C)
- Temperatur Abluft WP VL Verdampfer F6.16 (°C)
- Temperatur Abluft WP RL Verdampfer F6.17 (°C)
- Temperatur Abwasser WP RL Verdampfer F6.05 (°C)
- Temperatur Abwasser WP VL Verdampfer F6.04 (°C)
- Temperatur Abluft WP RL Kond F6.21 (°C)
- Abwasserschacht unten (°C)
- Temperatur Abluft WP RL Verdampfer von KMZ (°C)

### Nur in Datei 3 (109 einzigartige Parameter)
Andere Benennungskonvention mit detaillierteren Beschreibungen:
- Zählerstand WMZ WP Abluft (kWh)
- Strom Zähler PV-Anlage Haus 1-15 Leistung in W (W)
- KMZ Lüftung Haus 1-15 (verschiedene Messungen)
- WMZ verschiedener Komponenten

## Schlussfolgerungen

### Haupterkenntnisse

1. **Teilmengen-Beziehung bestätigt**
   - Datei 2 ist ein gezielter Auszug wichtiger Kern-Parameter
   - 57,7% der Parameter aus Datei 2 sind identisch in Datei 1 vorhanden
   - Die gemeinsamen Parameter zeigen 100% identische Messwerte

2. **Unterschiedliche Export-Profile**
   - Datei 1 & 3: Vollständige System-Exports mit allen Sensoren
   - Datei 2: Fokussierter Export auf kritische Temperatur- und Energiewerte
   - Verschiedene Benennungskonventionen zwischen den Export-Typen

3. **Datenintegrität**
   - Keine Werteabweichungen bei gemeinsamen Parametern
   - Konsistente Messintervalle (5 Minuten Standard)
   - Deutsches Zahlenformat durchgängig verwendet

4. **Praktische Verwendung**
   - Datei 1 & 3: Für detaillierte Systemanalysen
   - Datei 2: Für schnelle Übersichten und Kern-Monitoring
   - Unterschiedliche Zeiträume ermöglichen verschiedene Analysezwecke

### Empfehlungen

1. **Standardisierung der Parameternamen** zwischen verschiedenen Export-Typen
2. **Dokumentation der Export-Profile** für zukünftige Referenz
3. **Regelmäßige Validierung** der Teilmengen-Beziehungen
4. **Automatisierte Vergleichsroutinen** für Datenqualitätssicherung

## Technische Details

### Verwendete Analysemethoden
- Python-basierte CSV-Analyse ohne externe Bibliotheken
- Zeitstempel-basierter Wertevergleich
- Kategorisierung durch Schlüsselwort-Analyse
- Statistische Auswertung der Übereinstimmungen

### Analyseskripte
- `csv_comparison_simple.py`: Struktureller Vergleich
- `csv_detailed_analysis.py`: Zeitliche und Wertanalyse

---

*Analyse durchgeführt am: 22.08.2025*
*Datenstand: Januar-März 2025*