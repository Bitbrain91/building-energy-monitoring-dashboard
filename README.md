# MokiG Dashboard - Hauptversion

## 🎯 Projektübersicht

Umfassendes Dashboard zur Visualisierung und Analyse von Energiemonitoringdaten aus verschiedenen Quellen im Rahmen des MokiG-Forschungsprojekts (Monitoring für klimaneutrale Gebäude).

## ✨ Hauptfeatures

- **🎯 Benutzerdefinierte Visualisierungen**: Freie Auswahl der Parameter zur Darstellung
- **📊 Multi-Source Support**: Twin2Sim, Erentrudisstr., FIS Inhauser, KW Neukirchen
- **📈 Erweiterte Tabellen**: Vollständige Spaltennamen mit Resizing-Funktion
- **🔄 Integrierte Zeitreihenanalyse**: Aggregationen und Multi-Parameter-Vergleiche
- **📉 Statistische Analysen**: Automatische deskriptive Statistiken
- **💾 Cross-Platform**: Läuft auf Windows, Linux und macOS

## 🚀 Quick Start

```bash
# Dashboard starten
python start_dashboard.py
```

Das Dashboard öffnet sich automatisch im Browser unter: **http://127.0.0.1:8050**

## 📁 Projektstruktur

```
MokiG/
├── start_dashboard.py              # Haupteinstiegspunkt
├── src/
│   ├── dashboard_main.py           # Hauptdashboard-Logik
│   ├── data_loader_improved.py     # Datenlade-Modul
│   ├── ui_components_improved.py   # UI-Komponenten
│   ├── callbacks_improved.py       # Callback-Funktionen
│   └── visualization_improved.py   # Erweiterte Visualisierungen
├── Daten/
│   ├── Beispieldaten/              # Twin2Sim Daten
│   ├── Monitoringdaten/            # Gebäudemonitoring
│   └── vertraulich_*/              # Kraftwerksdaten
├── docs/
│   └── Dashboard_Hauptversion_Dokumentation.md
└── venv/                           # Virtuelle Umgebung
```

## 📊 Dashboard-Module

### Hauptnavigation
- **Twin2Sim**: Simulationsdaten (PV, Lüftung, Raumklima, Wetter)
- **Erentrudisstraße**: Gebäudemonitoring und Energieverbrauch
- **FIS Inhauser**: Friedrich-Inhauser-Straße Gebäudedaten
- **KW Neukirchen**: Kraftwerksdaten (Dürnbach, Untersulzbach, Wiesbach)
- **Vergleichsansicht**: Überblick über alle Datenquellen

### Funktionen pro Dataset
1. **Datentabelle**: Vollständige Datenansicht mit Sortierung und Filterung
2. **Visualisierungen**: Benutzerdefinierte Parameter-Auswahl mit:
   - Getrennte Charts
   - Überlagerte Ansicht
   - Subplots
   - Datenglättung
   - Bereichsauswahl
3. **Statistiken**: Deskriptive Statistik aller numerischen Spalten

## 🛠️ Technische Details

- **Framework**: Dash/Plotly (Python)
- **Datenverarbeitung**: Pandas, NumPy
- **UI**: Dash Bootstrap Components
- **Update-Intervall**: 60 Sekunden

## 📈 Datenquellen

### Twin2Sim (1-5 Sek. Frequenz)
- T2S_IntPV.csv: Growatt PV-Wechselrichter (9 Parameter)
- T2S_ManiPV.csv: Manipulation PV-System (13 Parameter)
- T2S_Lüftung.csv: Lüftungsanlage (42 Parameter)
- T2S_RAU006.csv: Büro-Raummonitoring (25 Parameter)
- T2S_Wetterdaten.csv: Wetterstation MSR02 (14 Parameter)

### Erentrudisstraße (5 Min. Frequenz)
- Energieverbrauch und Gebäudetechnik
- Zeitraum: 01.12.2023 bis 31.03.2025

### FIS Inhauser (5 Min. Frequenz)
- Friedrich-Inhauser-Straße Gebäudedaten
- Zeitraum: 01.10.2024 bis 31.03.2025

### KW Neukirchen (15 Min. Frequenz)
- Kraftwerke: Dürnbach, Untersulzbach, Wiesbach
- Erzeugung und Übergabe-Daten
- Zeitraum: 01.01.2020 bis 31.12.2024

## 🔧 Installation (bei Problemen)

```bash
# Python Virtual Environment erstellen
python -m venv venv

# Aktivieren (Windows)
venv\Scripts\activate.bat

# Aktivieren (Linux/Mac)
source venv/bin/activate

# Abhängigkeiten installieren
pip install dash plotly pandas numpy dash-bootstrap-components openpyxl
```

## 📝 Erweiterte Nutzung

### Datenanalyse exportieren
```python
from data_processor import DataProcessor

processor = DataProcessor("Daten/Beispieldaten")
processor.load_all_data()
processor.export_summary("analyse.xlsx")
```

## 🏢 Projektinformationen

- **Projekt**: MokiG - Monitoring für klimaneutrale Gebäude
- **FFG Projektnummer**: 923166
- **Projektleitung**: Fachhochschule Salzburg
- **Laufzeit**: 2025-2026

## 👥 Projektpartner

- Fachhochschule Salzburg (Projektleitung)
- Meshmakers GmbH
- Unbuzz Consulting
- ECB energy consult business gmbh
- Heimat Österreich (assoziiert)
- Lichtgenossenschaft Neukirchen (assoziiert)

## 📄 Lizenz

© 2025 Fachhochschule Salzburg - Alle Rechte vorbehalten

---

*Dashboard entwickelt für das MokiG-Projekt zur Förderung klimaneutraler Gebäude*