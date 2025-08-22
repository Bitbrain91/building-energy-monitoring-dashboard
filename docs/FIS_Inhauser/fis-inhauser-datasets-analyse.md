# FIS_Inhauser - Datensatz-Analyse

**Analysedatum:** 21.08.2025  
**Datenstandort:** `/Daten/Monitoringdaten/FIS_Inhauser/Monitoring`

## 📊 Übersicht der Datensätze

Die Friedrich-Inhauser-Straße Monitoring-Daten umfassen **5 Hauptdatensätze** mit Gebäudemonitoring für 8 Häuser (1, 3, 5, 7, 9, 11, 13, 15). Die Daten decken Heizung, Kühlung, Lüftung, Wärmepumpen und PV-Anlagen ab.

## 📁 Dateistruktur

```
FIS_Inhauser/Monitoring/
├── 2024-2025-05_AT.xlsx           # Hauptdatei (aggregiert)
└── 250101-250331/                 # Q1 2025 Exporte
    ├── export_1551_2024-12-31...csv  # Vollexport
    └── test/
        ├── export_1551_2025-01...csv  # Reduzierter Export
        ├── V1_2501_EXPORT_1.CSV       # Testdaten
        └── 250123-250129_ok.xlsx      # Wochendaten
```

## 📈 Detaillierte Dateianalyse

### 1. **2024-2025-05_AT.xlsx** (Hauptdatei)
- **Zeitraum:** 01.01.2024 - 16.05.2025
- **Datensätze:** 54.154 Zeilen × 2 Spalten
- **Besonderheit:** Aggregierte/prozessierte Daten
- **Verwendung:** Langzeitübersicht und Trends

### 2. **export_1551_2024-12-31-00-00_2025-03-31-23-55.csv** ⭐ UMFASSENDSTER
- **Zeitraum:** 31.12.2024 - 31.03.2025
- **Datensätze:** 22.806 Zeilen × 111 Parameter
- **Intervall:** 5 Minuten
- **Inhalt:**
  - 🌡️ 41 Temperaturparameter
  - 💧 15 Durchflussmessungen
  - ⚡ 54 Energie/Leistungsparameter
- **Abdeckung:** Alle 8 Häuser mit individuellen Messungen
- **Systeme:** 
  - Kältezähler für jedes Haus
  - Stromzähler Lüftungsgeräte
  - Heizung/Kühlung/Lüftung komplett

### 3. **export_1551_2025-01-01-00-00_2025-03-31-23-55.csv** (Reduziert)
- **Zeitraum:** 01.01.2025 - 31.03.2025
- **Datensätze:** 21.138 Zeilen × 26 Parameter
- **Fokus:** Wärmepumpen und Kernsysteme
- **Inhalt:**
  - 🌡️ 19 Temperaturparameter (hauptsächlich WP)
  - 💧 3 Durchflussmessungen
  - ⚡ 3 Energieparameter
- **Besonderheit:** Konzentration auf Abluft-/Abwasser-Wärmepumpen

### 4. **V1_2501_EXPORT_1.CSV** (Testwoche)
- **Zeitraum:** 23.01.2025 - 29.01.2025 (7 Tage)
- **Datensätze:** 1.568 Zeilen × 112 Parameter
- **Besonderheit:** Ähnlicher Umfang wie Vollexport, aber nur 1 Woche
- **Zusätzlich:** PV-Anlagen-Daten (Haus 1 & 15)
- **Verwendung:** Validierung/Testdaten

### 5. **250123-250129_ok_250130.xlsx**
- **Zeitraum:** 23.01.2025 - 29.01.2025
- **Struktur:** 2 Sheets (Tabelle1: 1.569 Zeilen, Tabelle2: 113 Zeilen)
- **Verwendung:** Wochenbericht/Analyse

## 🔄 Vergleich der Datensätze

### Parameter-Übersicht

| Datei | Parameter | Datenpunkte | Zeitraum | Schwerpunkt |
|-------|-----------|-------------|----------|-------------|
| **export_2024-12** | 111 | 22.806 | 3 Monate | Vollständiges Monitoring |
| **V1_Export** | 112 | 1.568 | 1 Woche | Test + PV-Anlagen |
| **export_2025-01** | 26 | 21.138 | 3 Monate | Wärmepumpen-Fokus |
| **Main Excel** | 2 | 54.154 | 16 Monate | Aggregierte Daten |

### Gemeinsame Parameter

**Nur 2 Parameter in ALLEN Dateien:**
- Datum + Uhrzeit
- Vorlauf Pelletskessel (°C)

**Überschneidungen:**
- Export_2024-12 & Export_2025-01: 13 gemeinsame Parameter
- Export_2024-12 & V1_Export: 1 gemeinsamer Parameter
- Export_2025-01 & V1_Export: 0 gemeinsame Parameter

### Einzigartige Inhalte

**Export_2024-12 (95 exklusive Parameter):**
- Individuelle Hausüberwachung (Haus 1-15)
- 24 Stromzähler-Parameter
- 29 Kältezähler-Parameter
- Lüftungsgeräte für jedes Haus

**Export_2025-01 (11 exklusive Parameter):**
- Fokus auf Wärmepumpen-Temperaturen
- Abluft-WP Vor-/Rücklauf
- Abwasser-WP Parameter
- Kondensator/Verdampfer-Temperaturen

**V1_Export (109 exklusive Parameter):**
- PV-Anlagen Haus 1 & 15
- Durchlauferhitzer-Monitoring
- Zirkulations-Zähler
- Detaillierte Wärmemengenzähler

## 🏠 Gebäudeabdeckung

**Überwachte Häuser:** 1, 3, 5, 7, 9, 11, 13, 15 (8 Gebäude)

**Systeme pro Haus:**
- Lüftungsgerät mit Kältezähler
- Stromzähler
- Heizkreise
- Teilweise PV-Anlagen (Haus 1 & 15)

## 📊 Datenhierarchie

```
┌─────────────────────────────────────────────────────────┐
│ V1_Export: 112 Parameter (TESTDATENSATZ)                │
│ ├─ Nur 7 Tage, aber fast vollständige Abdeckung        │
│ └─ Inklusive PV-Anlagen                                 │
└─────────────────────────────────────────────────────────┘
                            ≈
┌─────────────────────────────────────────────────────────┐
│ export_2024-12: 111 Parameter (PRODUKTIVDATEN)          │
│ ├─ 3 Monate vollständige Überwachung                    │
│ └─ Alle Häuser und Systeme                              │
└─────────────────────────────────────────────────────────┘
                            ⊃
┌─────────────────────────────────────────────────────────┐
│ export_2025-01: 26 Parameter (KERNSYSTEM)               │
│ ├─ Reduziert auf Wärmepumpen                           │
│ └─ Subset von export_2024-12                           │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Empfehlungen

### Nach Analysezweck:

| Zweck | Empfohlene Datei | Begründung |
|-------|-----------------|------------|
| **Gesamtanalyse** | export_2024-12 | Vollständige Systemabdeckung |
| **Wärmepumpen-Analyse** | export_2025-01 | Fokussierte WP-Parameter |
| **PV-Analyse** | V1_Export | Einzige Datei mit PV-Daten |
| **Langzeittrends** | 2024-2025-05_AT.xlsx | 16 Monate Daten |
| **Validierung** | V1_Export vs export_2024-12 | Gleicher Zeitraum verfügbar |

### Datenqualität:
- ✅ **Konsistente 5-Minuten-Intervalle** in allen CSV-Dateien
- ✅ **Identische Werte** für gemeinsame Parameter (Vorlauf Pelletskessel)
- ✅ **Vollständige Zeitreihen** ohne größere Lücken
- ⚠️ **Sehr wenige gemeinsame Parameter** zwischen Dateien

## 💡 Besonderheiten

1. **Unterschiedliche Parametersätze:** Die Dateien haben überraschend wenig Überschneidung (nur 2 gemeinsame Parameter)
2. **V1_Export als Testdatensatz:** Enthält die meisten Parameter (112), aber nur für 1 Woche
3. **Wärmepumpen-Fokus:** Export_2025-01 konzentriert sich ausschließlich auf WP-System
4. **Multi-Gebäude-Monitoring:** 8 Häuser mit individueller Überwachung
5. **PV-Integration:** Nur in V1_Export enthalten

## 📝 Technische Hinweise

- **Dateiformat:** CSV mit Komma-Separator, UTF-8 Encoding
- **Zeitformat:** DD.MM.YYYY HH:MM
- **Sampling-Rate:** Einheitlich 5 Minuten
- **Namenskonvention:** export_[ID]_[StartDatum]_[EndDatum].csv
- **ID 1551:** Vermutlich System- oder Standort-ID