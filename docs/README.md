# 📚 Projektdokumentation - Übersicht

**Projekt:** Gebäudemonitoring und Energiedatenanalyse  
**Stand:** 22.08.2025

## 📁 Dokumentationsstruktur

Die Dokumentation ist nach den vier Hauptstandorten gegliedert:

### 🏢 [Twin2Sim](./Twin2Sim/)
Simulationsdaten und Dashboard-Entwicklung
- `DataView.md` - Datenvisualisierung und -struktur
- `Datenanalyse_Technisch.md` - Technische Analyse der Twin2Sim-Daten
- `Dashboard_Hauptversion_Dokumentation.md` - Dashboard-Dokumentation

### 🏠 [Erentrudisstr](./Erentrudisstr/)
Monitoring-Daten Erentrudisstraße 19
- `final-erentrudisstr-dataset-hierarchy.md` - Vollständige Datensatz-Hierarchie
- `erentrudisstr-datasets-analyse.md` - Detaillierte Datensatzanalyse
- `Monitoringdaten_Erentrudisstr_Analyse.md` - Erste Monitoringdaten-Analyse
- `all-vs-relevant-comparison.md` - Vergleich All vs Relevant Dateien
- `relevant-files-comparison.md` - Vergleich der Relevant-Dateien
- `durchfluss-complete-comparison.md` - Durchflussdaten-Vergleich
- `complete-dataset-comparison.md` - Gesamtvergleich aller Datensätze

### 🏘️ [FIS_Inhauser](./FIS_Inhauser/)
Friedrich-Inhauser-Straße (8 Häuser)
- `fis-inhauser-datasets-analyse.md` - Aktuelle Datensatzanalyse
- `FIS_Inhauser_Datenanalyse.md` - Erste Datenanalyse

### ⚡ [KW_Neukirchen](./KW_Neukirchen/)
Kraftwerk Neukirchen Erzeugungsdaten
- `kw_neukirchen_datenanalyse.md` - Kraftwerksdaten-Analyse

### 📊 Übergreifende Dokumentation
- `datenlandschaft-uebersicht.md` - Gesamtübersicht aller Datenquellen
- `datenfiles-overview.md` - Übersicht aller Datendateien
- `aggregierte-datenuebersicht.md` - Aggregierte Datenübersicht
- `datenregionen-auflistung.md` - Auflistung der Datenregionen
- `fehlende-daten-analyse.md` - Analyse fehlender Daten

## 🎯 Haupterkenntnisse

### Datenumfang
| Standort | Dateien | Parameter (max) | Zeitraum | Besonderheit |
|----------|---------|-----------------|----------|--------------|
| **Twin2Sim** | 1 CSV | 145 | 2024 | Simulationsdaten |
| **Erentrudisstr** | 6 CSV, 3 Excel | 49 | 2023-2025 | Einzelgebäude |
| **FIS_Inhauser** | 3 CSV, 2 Excel | 112 | 2024-2025 | 8 Häuser, PV-Anlagen |
| **KW Neukirchen** | 1 CSV | 11 | 2024-2025 | Kraftwerksdaten |

### Hauptunterschiede
- **Twin2Sim:** Simulationsdaten mit höchster Parameteranzahl
- **Erentrudisstr:** Längste Zeitreihe (16 Monate), Fokus auf Heizung/Warmwasser
- **FIS_Inhauser:** Multi-Gebäude-Monitoring mit PV und Wärmepumpen
- **KW Neukirchen:** Spezialisiert auf Energieerzeugung

## 🔧 Technische Details

### Datenformate
- **CSV-Dateien:** Meist Komma-getrennt, UTF-8
- **Excel-Dateien:** Aggregierte/prozessierte Daten
- **Zeitformate:** DD.MM.YYYY HH:MM oder YYYY-MM-DD HH:MM
- **Intervalle:** 5-15 Minuten (standortabhängig)

### Bekannte Probleme
- Einige CSV-Dateien in Erentrudisstr benötigen Semikolon als Trennzeichen
- Unvollständige Zeitreihen in einigen Datensätzen
- Geringe Parameter-Überschneidung zwischen FIS_Inhauser-Dateien

## 📈 Dashboard & Visualisierung

Das entwickelte Dashboard integriert Daten aus allen Quellen:
- **Technologie:** Streamlit-basiert
- **Features:** Multi-Source-Integration, Zeitreihenanalyse, Vergleichsansichten
- **Status:** Funktionsfähig für alle Datenquellen

## 🚀 Nächste Schritte

1. **Datenqualität:** Bereinigung der CSV-Parsing-Probleme
2. **Integration:** Vereinheitlichung der Parameterbezeichnungen
3. **Analyse:** Erweiterte Korrelationsanalysen zwischen Standorten
4. **Dashboard:** Erweiterte Filterfunktionen und Exportmöglichkeiten

## 📝 Kontakt & Support

Für Fragen zur Dokumentation oder den Daten wenden Sie sich an das Projektteam.

---
*Letzte Aktualisierung: 22.08.2025*