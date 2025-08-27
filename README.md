# Building Energy Monitoring Dashboard

## Überblick

Ein Python-basiertes Plotly Dash Dashboard zur Visualisierung und Analyse von Energieverbrauchsdaten aus mehreren Gebäudestandorten in Österreich. Das Dashboard ermöglicht die Echtzeitüberwachung und -analyse von Energiedaten aus vier Hauptstandorten mit unterschiedlichen Datencharakteristika.

## Features

- 📊 **Interaktive Visualisierungen**: Zeitreihen-Diagramme, Heatmaps und Vergleichsansichten
- 📈 **Echtzeit-Datenanalyse**: Automatische Aggregation und statistische Auswertungen
- 🏢 **Multi-Standort-Unterstützung**: Integrierte Ansicht für 4 verschiedene Datenquellen
- ⚡ **Optimierte Performance**: Parquet-Format und In-Memory-Caching für schnelle Ladezeiten
- 📱 **Responsive Design**: Bootstrap-basiertes Layout für verschiedene Bildschirmgrößen

## Voraussetzungen

- **Python 3.8 oder höher**
- **Windows-Betriebssystem** (für die bereitgestellten Batch-Dateien)
- **Git** (zum Klonen des Repositories)
- Ca. 500 MB freier Speicherplatz

## Installation und Start

### Schritt 1: Repository klonen

```bash
git clone [repository-url]
cd building-energy-monitoring-dashboard
```

### Schritt 2: Virtuelle Umgebung erstellen und aktivieren

```bash
# Virtuelle Umgebung erstellen
python -m venv venv_windows

# Virtuelle Umgebung aktivieren (Windows)
venv_windows\Scripts\activate.bat
```

### Schritt 3: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### Schritt 4: Dashboard starten

**Option A: Mit der bereitgestellten Batch-Datei (empfohlen)**
```bash
START_DASHBOARD.bat
```

**Option B: Direkt mit Python**
```bash
python src/dashboard_optimized.py
```

### Schritt 5: Dashboard im Browser öffnen

Nach dem Start öffnet sich automatisch der Browser. Falls nicht, navigieren Sie manuell zu:
```
http://127.0.0.1:8050
```

## Schnellstart (Kurzanleitung)

Für erfahrene Nutzer - alle Befehle in Folge:

```bash
git clone [repository-url]
cd building-energy-monitoring-dashboard
python -m venv venv_windows
venv_windows\Scripts\activate.bat
pip install -r requirements.txt
START_DASHBOARD.bat
```

## Datenquellen

Das Dashboard überwacht vier Hauptstandorte:

| Standort | Beschreibung | Parameter | Datenintervall |
|----------|--------------|-----------|----------------|
| **Twin2Sim** | Simulationsdaten | 145 | 5-15 Minuten |
| **Erentrudisstr** | Einzelgebäude-Monitoring | 49 | 15 Minuten |
| **FIS_Inhauser** | 8 Häuser mit PV-Anlagen | 112 | 15 Minuten |
| **KW_Neukirchen** | Kraftwerk-Erzeugungsdaten | 11 | Variabel |
