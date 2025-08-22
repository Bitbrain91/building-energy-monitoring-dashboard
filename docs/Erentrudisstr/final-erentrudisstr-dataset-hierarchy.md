# Erentrudisstraße - Finale Datensatz-Hierarchie

**Analysedatum:** 21.08.2025  
**Gesamtanzahl CSV-Dateien:** 6 Hauptdateien

## 📊 Vollständige Datensatz-Übersicht

### Hierarchie nach Parameter-Umfang

```
┌─────────────────────────────────────────────────────────────┐
│ export_ERS_2023-12: 49 Parameter (UMFASSENDSTER DATENSATZ)  │
│ ├─ Zeitraum: Dez 2023 - März 2025 (484 Datenpunkte)        │
│ ├─ Besonderheit: Längster Zeitraum, wenige Datenpunkte      │
│ └─ Inhalt: Komplettes System inkl. aller Pufferspeicher     │
└─────────────────────────────────────────────────────────────┘
                            ⬇
┌─────────────────────────────────────────────────────────────┐
│ All_24-07: 45 Parameter                                     │
│ ├─ Zeitraum: Juli 2024 (8.322 Datenpunkte)                 │
│ ├─ Besonderheit: Detailreichster Sommermonat                │
│ └─ Inhalt: Vollständiges System ohne einige Pumpenparameter │
└─────────────────────────────────────────────────────────────┘
                            ⬇
┌─────────────────────────────────────────────────────────────┐
│ Relevant-1_2024: 23 Parameter                               │
│ ├─ Zeitraum: Jan-Dez 2024 (89.202 Datenpunkte)            │
│ ├─ Besonderheit: Erweitertes Jahres-Set                     │
│ └─ Inhalt: Heizkreise + Basis-Parameter                     │
└─────────────────────────────────────────────────────────────┘
                            ⬇
┌─────────────────────────────────────────────────────────────┐
│ Relevant_2024: 15 Parameter                                 │
│ ├─ Zeitraum: Jan-Dez 2024 (89.202 Datenpunkte)            │
│ ├─ Besonderheit: Basis-Jahres-Set                          │
│ └─ Inhalt: Warmwasser + Energie + Durchfluss               │
└─────────────────────────────────────────────────────────────┘
                            ⬇
┌─────────────────────────────────────────────────────────────┐
│ Durchfluss_2024 ≡ Vp.csv: 4 Parameter                      │
│ ├─ Durchfluss: Jan-Dez 2024 (89.202 Datenpunkte)          │
│ ├─ Vp.csv: Dez 2024-Jan 2025 (7.618 Datenpunkte)          │
│ └─ Inhalt: NUR Durchflussmessungen                         │
└─────────────────────────────────────────────────────────────┘
```

## 📈 Detaillierter Vergleich

| Datei | Parameter | Datenpunkte | Zeitraum | Datenqualität | Verwendungszweck |
|-------|-----------|-------------|----------|---------------|------------------|
| **export_ERS_2023-12** | 49 | 484 | Dez 2023 - März 2025 | Wenige Punkte, aber vollständig | Langzeit-Systemübersicht |
| **All_24-07** | 45 | 8.322 | Juli 2024 | Vollständig, hohe Auflösung | Sommer-Detailanalyse |
| **Relevant-1_2024** | 23 | 89.202 | Jahr 2024 | Vollständig | Jahres-Heizungsanalyse |
| **Relevant_2024** | 15 | 89.202 | Jahr 2024 | Vollständig | Jahres-Energieanalyse |
| **Durchfluss_2024** | 4 | 89.202 | Jahr 2024 | Vollständig | Hydraulische Analyse |
| **Vp.csv** | 4 | 7.618 | Dez 2024 - Jan 2025 | Unvollständig | Durchfluss-Snapshot |

## 🔑 Wichtige Erkenntnisse

### 1. **Einzigartige Parameter in export_ERS_2023-12:**
- Pumpen-Zwangsteuerung (AUS/Auto)
- Pumpen-Dauerbetrieb (EIN/AUS)
- Status KWZ (Kaltwasserzähler)
- Erweiterte Pumpenstatusparameter
- **Besonderheit:** Einzige Datei mit Langzeitdaten über 2023-2025

### 2. **Einzigartige Parameter in All_24-07:**
- Alle 8 Pufferspeicher-Temperaturen (2.01 - 2.08)
- Pumpen-Drehzahlen (%)
- EV-System Vor-/Rücklauf (primär & sekundär)
- Außenfühler-Temperatur
- **Besonderheit:** Höchste zeitliche Auflösung für Juli

### 3. **Datenbeziehungen:**
- Alle Dateien teilen einen gemeinsamen Kern von 4 Durchfluss-Parametern
- Relevant_2024 ⊂ Relevant-1_2024 (100% Subset)
- Durchfluss_2024 ⊂ Alle anderen Dateien (minimales Subset)
- export_ERS und All_24-07 haben jeweils einzigartige Parameter

### 4. **Zeitliche Abdeckung:**
```
2023    2024                                          2025
 |       |                                             |
 └──[export_ERS]──────────────────────────────────────┘
         └─────────[Relevant/Durchfluss]──────────────┘
                    └──[All_24-07]──┘
                                      └─[Vp.csv]──────┘
```

## 💡 Empfehlungen für die Datennutzung

### Nach Analysezweck:

| Zweck | Empfohlene Datei(en) | Begründung |
|-------|---------------------|------------|
| **Langzeittrends** | export_ERS_2023-12 | 16 Monate Daten, alle Parameter |
| **Jahresanalyse 2024** | Relevant-1_2024 | Vollständiges Jahr, erweiterte Parameter |
| **Sommeranalyse** | All_24-07 | Detailreichste Juli-Daten |
| **Energiebilanz** | Relevant_2024 | Fokussierte Energie-Parameter |
| **Hydraulik** | Durchfluss_2024 | Spezialisiert auf Volumenströme |
| **Systemübersicht** | export_ERS + All_24-07 | Kombination für vollständiges Bild |

### Nach Detailgrad:

1. **Maximum Detail:** All_24-07 (45 Parameter, aber nur Juli)
2. **Beste Balance:** Relevant-1_2024 (23 Parameter, ganzes Jahr)
3. **Effiziente Analyse:** Relevant_2024 (15 Kern-Parameter)
4. **Minimal:** Durchfluss_2024 (nur Durchflüsse)

## 📝 Technische Hinweise

### Datenqualität:
- ✅ **Beste Qualität:** Relevant-Dateien und Durchfluss_2024 (konsistent, vollständig)
- ⚠️ **Mittlere Qualität:** All_24-07 (vollständig, aber nur 1 Monat)
- ⚠️ **Niedrige Datendichte:** export_ERS (nur 484 Punkte für 16 Monate)
- ❌ **Unvollständig:** Vp.csv (nur Teilzeitraum)

### Datenkonsistenz:
- Gemeinsame Parameter haben **identische Werte** über alle Dateien
- Zeitstempel sind synchron für überlappende Zeiträume
- Keine Widersprüche zwischen Dateien gefunden

## 🎯 Fazit

Die Erentrudisstraße-Datensätze bilden eine klare Hierarchie von minimal (4 Parameter) bis maximal (49 Parameter). Für umfassende Analysen empfiehlt sich die Kombination von:
- **export_ERS** für Langzeittrends
- **Relevant-1_2024** für Jahresanalysen
- **All_24-07** für Detailstudien

Die Durchfluss-Dateien sind perfekte Subsets für spezialisierte hydraulische Berechnungen.