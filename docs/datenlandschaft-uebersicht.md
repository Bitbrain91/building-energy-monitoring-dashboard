# Aggregierte Datenübersicht - Meeting-Präsentation

**Stand:** 27.08.2025  
**Zweck:** Übersicht der verfügbaren Datenquellen für MokiG-Projekt

## Inhaltsverzeichnis

1. [Twin2Sim - Digitaler Zwilling (Simulationsdaten)](#twin2sim---digitaler-zwilling-simulationsdaten)
2. [Erentrudisstr - Gebäudemonitoring](#erentrudisstr---gebäudemonitoring)
3. [FIS_Inhauser - Mehrfamilienhaus-Komplex mit PV](#fis_inhauser---mehrfamilienhaus-komplex-mit-pv)
4. [KW-Neukirchen - Wasserkraftwerke Erzeugungsdaten](#kw-neukirchen---wasserkraftwerke-erzeugungsdaten)

---

## Twin2Sim - Digitaler Zwilling (Simulationsdaten)

**Beschreibung:** Simulationsdaten eines digitalen Gebäudezwillings. Die im Dashboard verfügbaren Daten sind nur ein kleiner Ausschnitt der tatsächlich vorhandenen Daten.

### Verfügbare Datensätze im Dashboard:
- **T2S_IntPV** - Interne PV-Anlage (Growatt Wechselrichter)
- **T2S_Lüftung** - RLT-Anlagendaten 
- **T2S_ManiPV** - Manipulierte PV-Daten
- **T2S_RAU006** - Raumautomation
- **T2S_Wetterdaten** - Wetterstation

### Parameterübersicht:
- **Tatsächlich verfügbar:** Über 1.000 Parameter
- **Im Dashboard-Auszug:** 106 Parameter
- **Relevante Parameter für MokiG:** _[Wird von Kollegen ergänzt]_

### Zeitauflösung (Messintervall):
- **Tatsächliche Aufzeichnung:** 1-5 Sekunden (variabel)
- **Dashboard-Testdaten:** 1 Stunde (nur Beispieldaten Juni 2025)

### Zu klären im Meeting:
- [ ] Ab wann beginnt die Datenaufzeichnung?
- [ ] Sind historische Daten ebenfalls in 1-5 Sekunden Auflösung verfügbar?
- [ ] Welche der 1.000+ Parameter sind für MokiG relevant?

**Zusätzliche Dokumente:** Energieausweis vorhanden

### Übersichtstabelle Twin2Sim:
| Kriterium | Aus Analyse (Dashboard) | Tatsächlich verfügbar | MokiG-Relevant |
|-----------|-------------------------|----------------------|----------------|
| **Anzahl Parameter** | 106 | >1.000 | _[Im Meeting klären]_ |
| **Zeitauflösung** | 1 Stunde (Testdaten) | 1-5 Sekunden | _[Im Meeting klären]_ |
| **Zeitraum** | Juni 2025 (Test) | _[Im Meeting klären]_ | _[Im Meeting klären]_ |
| **Historische Daten in gleicher Auflösung** | Ja (1h durchgehend) | _[Im Meeting klären]_ | - |

---

## Erentrudisstr - Gebäudemonitoring

**Beschreibung:** Monitoring eines einzelnen Gebäudes mit Fokus auf Energieeffizienz und Gebäudeautomation

### Verfügbare Datensätze:
- **Langzeitdaten 2023-2025** - Tägliche Aggregation (49 Parameter)
- **Komplettdaten Juli 2024** - 5-Minuten-Auflösung (45 Parameter)
- **Relevante Parameter 2024** - 5-Minuten-Auflösung (23 ausgewählte Parameter)

### Parameterübersicht Langzeitdaten (49 Parameter):

**Kategorisierung der 49 Parameter:**
- **Temperaturmessungen:** 18 Parameter
  - Vor-/Rücklauf verschiedener Kreise (HK1 Ost, HK2 West, EV primär/sekundär)
  - Warmwasser, Kaltwasser, Zirkulation
- **Pufferspeicher:** 9 Parameter (Puffer 2.01 bis 2.08 + Außenfühler)
- **Pumpensteuerung:** 12 Parameter
  - Zirkulation primär/sekundär (Status, Dauer, Zwang)
  - Pufferladung, HK1/HK2 Status
- **Energie/Zähler:** 5 Parameter
  - Fernwärme (Zählerstand, Leistung)
  - Zirkulation (Zählerstand, Leistung)
  - Wasserzähler TWE
- **Durchflussmessungen:** 3 Parameter (Fernwärme, TWE, Zirkulation)
- **Status/Betrieb:** 1 Parameter (KWZ EIN/AUS)

**Vergleich zu anderen Datensätzen:**
- **Juli 2024 (45 Parameter):** Fehlen 4 Pumpensteuerungsparameter
- **Relevante 2024 (23 Parameter):** Ausgewählte Teilmenge für Energieanalyse

**Relevante Parameter für MokiG:** _[Wird von Kollegen ergänzt]_

### Zeitauflösung (Messintervall):
- **2023-2025 Langzeit:** Tägliche Datenpunkte
- **2024 Detaildaten:** 5 Minuten

### Zu klären im Meeting:
- [ ] Sind Daten vor 2024 auch in 5-Minuten-Auflösung archiviert?
- [ ] Ist 5 Minuten die maximale Auflösung oder gibt es höhere Auflösungen?
- [ ] Wie weit reichen die historischen Daten zurück (vor 2023)?
- [ ] Anzahl der überwachten Gebäude/Einheiten?

**Zusätzliche Dokumente:** Energieausweis vorhanden

### Übersichtstabelle Erentrudisstr:
| Kriterium | Aus Analyse (Dashboard) | Tatsächlich verfügbar | MokiG-Relevant |
|-----------|-------------------------|----------------------|----------------|
| **Anzahl Parameter** | 49 (Langzeit), 45 (Juli), 23 (Relevant) | _[Im Meeting klären]_ | _[Im Meeting klären]_ |
| **Zeitauflösung** | 1 Tag (2023-2025), 5 Min (2024) | _[Im Meeting klären]_ | _[Im Meeting klären]_ |
| **Zeitraum** | Ab 01.12.2023 | _[Im Meeting klären]_ | _[Im Meeting klären]_ |
| **Historische Daten in gleicher Auflösung** | Nein (täglich vs. 5 Min) | _[Im Meeting klären]_ | - |

---

## FIS_Inhauser - Mehrfamilienhaus-Komplex mit PV

**Beschreibung:** Monitoring von 8 Mehrfamilienhäusern (Hausnummern: 1, 3, 5, 7, 9, 11, 13, 15) mit integrierten Photovoltaikanlagen und moderner Gebäudetechnik.

### Verfügbare Datensätze:
1. **Außentemperatur 2024-2025** - Nur 2 Spalten (Datum + Außentemperatur)
2. **Quartalsdaten Q1/2025** - Kompletter Datensatz mit allen 111 Parametern

### Parameterübersicht Q1/2025 (111 Parameter):

**Kategorisierung der 111 Parameter:**
- **Gebäudespezifisch:** 52 Parameter
  - Verteilt auf 8 Häuser (1, 3, 5, 7, 9, 11, 13, 15)
  - Lüftungsgeräte, individuelle Messungen pro Haus
- **Energie/Zähler:** 39 Parameter
  - Stromzähler (Heizung, Lüftung, PV)
  - Kältezähler, Leistungsmessungen
- **Wärmepumpen:** 29 Parameter
  - ABL-WP und ABW-WP Systeme
  - Durchfluss, Energie, Temperaturen
- **Temperaturmessungen:** 15 Parameter
  - Vor-/Rücklauf verschiedener Systeme
  - Pelletkessel, DLE
- **Durchflussmessungen:** 10 Parameter
  - Kältezähler der Lüftungsgeräte
- **PV-Anlage:** 1 Parameter (Stromzähler PV Haus 15)

**Relevante Parameter für MokiG:** _[Wird von Kollegen ergänzt]_

### Zeitauflösung (Messintervall):
- **Aktuell:** 5 Minuten
- **Historisch:** Nur Q1 2025

### Zu klären im Meeting:
- [ ] Ist 5-Minuten die maximale Auflösung oder gibt es sekundengenaue Daten?
- [ ] Gibt es noch mehr Parameter als im vorhandenen Datensatz?
- [ ] Historische Daten vor Q1 verfügbar? -> Wenn ja, in welcher Auflösung?

**Zusätzliche Dokumente:** Energieausweis vorhanden

### Übersichtstabelle FIS_Inhauser:
| Kriterium | Aus Analyse (Dashboard) | Tatsächlich verfügbar | MokiG-Relevant |
|-----------|-------------------------|----------------------|----------------|
| **Anzahl Parameter** | 111 (Q1 2025), 2 (Außentemp) | _[Im Meeting klären]_ | _[Im Meeting klären]_ |
| **Zeitauflösung** | 5 Minuten | _[Im Meeting klären]_ | _[Im Meeting klären]_ |
| **Zeitraum** | Q1 2025 (31.12.2024 - 31.03.2025) | _[Im Meeting klären]_ | _[Im Meeting klären]_ |
| **Historische Daten in gleicher Auflösung** | Ja (5 Min durchgehend) | _[Im Meeting klären]_ | - |

---

## KW-Neukirchen - Wasserkraftwerke Erzeugungsdaten

**Beschreibung:** Erzeugungsdaten von drei Wasserkraftwerken sowie Netzübergabepunkte. Kritische Infrastruktur für regionale Energieversorgung.

### Kraftwerke:
1. **KW Dürnbach** - Laufwasserkraftwerk
2. **KW Untersulzbach** - Laufwasserkraftwerk
3. **KW Wiesbach** - Laufwasserkraftwerk

### Verfügbare Datensätze:
- **Erzeugungsdaten pro Kraftwerk** (2020-2024, jahresweise Excel-Dateien)
  - Parameter: WERT ENERGIE [kWh], WERT LEISTUNG [kW]
- **Übergabe Bezug** - Netzbezug bei Unterdeckung
  - Parameter: WERT [kWh]
- **Übergabe Lieferung** - Netzeinspeisung bei Überproduktion  
  - Parameter: WERT [kWh]

### Parameterübersicht:
- **Pro Kraftwerk (Erzeugung):** 2 Parameter
  - WERT ENERGIE [kWh]
  - WERT LEISTUNG [kW]
- **Übergabe Bezug:** 1 Parameter (WERT [kWh])
- **Übergabe Lieferung:** 1 Parameter (WERT [kWh])
- **Gesamt:** 8 eindeutige Parameter (3×2 + 2×1)

**Relevante Parameter für MokiG:** _[Wird von Kollegen ergänzt]_

### Zeitauflösung (Messintervall):
- **Durchgehend 2020-2024:** 15 Minuten

### Zu klären im Meeting:
- [ ] Gibt es Daten in höherer Auflösung als 15 Minuten?
- [ ] Historische Daten vor 2020 verfügbar?
- [ ] Weitere Parameter/Datensätze die für uns relevant sein könnten?

### Übersichtstabelle KW-Neukirchen:
| Kriterium | Aus Analyse (Dashboard) | Tatsächlich verfügbar | MokiG-Relevant |
|-----------|-------------------------|----------------------|----------------|
| **Anzahl Parameter** | 8 (3×2 Kraftwerke + 2 Übergabe) | _[Im Meeting klären]_ | _[Im Meeting klären]_ |
| **Zeitauflösung** | 15 Minuten | _[Im Meeting klären]_ | _[Im Meeting klären]_ |
| **Zeitraum** | 01.01.2020 - 31.12.2024 | _[Im Meeting klären]_ | _[Im Meeting klären]_ |
| **Historische Daten in gleicher Auflösung** | Ja (15 Min durchgehend) | _[Im Meeting klären]_ | - |

