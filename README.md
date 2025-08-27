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

## Dashboard-Funktionen

### Hauptnavigation
- **Übersicht**: KPI-Karten mit aktuellen Metriken
- **Datenquelle**: Dropdown zur Auswahl des Standorts
- **Zeitbereich**: Flexible Zeitfilterung der Daten

### Visualisierungen
- **Zeitreihen**: Verlauf ausgewählter Parameter
- **Heatmap**: Korrelationsanalyse zwischen Parametern
- **Vergleichsansicht**: Multi-Standort-Vergleiche
- **Datentabelle**: Detaillierte Rohdatenansicht

### Datenexport
- Export als CSV über die Datentabellenansicht
- Diagramme als PNG speicherbar

## Performance-Optimierung (Optional)

Für bessere Performance können die Daten ins Parquet-Format konvertiert werden:

```bash
python src/preprocess_data.py --source all
```

Dies erstellt optimierte Dateien im `data_optimized/` Verzeichnis.

## Fehlerbehebung

### Dashboard startet nicht
1. Prüfen Sie, ob die virtuelle Umgebung aktiviert ist
2. Stellen Sie sicher, dass alle Abhängigkeiten installiert sind: `pip install -r requirements.txt`
3. Überprüfen Sie, ob Port 8050 frei ist

### Keine Daten sichtbar
1. Prüfen Sie, ob die Datenordner vorhanden sind
2. Kontrollieren Sie die Dateipfade in `src/data_loader_optimized.py`

### Langsame Performance
1. Führen Sie die Datenoptimierung aus (siehe oben)
2. Reduzieren Sie den ausgewählten Zeitbereich
3. Schließen Sie andere speicherintensive Anwendungen

## Projektstruktur

```
building-energy-monitoring-dashboard/
├── src/                            # Quellcode
│   ├── dashboard_optimized.py     # Hauptanwendung
│   ├── data_loader_optimized.py   # Datenlade-Logik
│   ├── ui_components_improved.py  # UI-Komponenten
│   ├── callbacks_improved.py      # Interaktions-Callbacks
│   ├── visualization_improved.py  # Visualisierungen
│   ├── load_kw_aggregated.py      # KW Neukirchen Datenaggregation
│   ├── column_toggle_component.py # Spalten-Toggle Komponente
│   ├── column_toggle_callbacks.py # Spalten-Toggle Callbacks
│   ├── data_optimizer.py          # Datenoptimierung zu Parquet
│   └── data/                       # Kopierte/optimierte Daten
│       ├── twin2sim/               # Twin2Sim CSV-Daten
│       ├── erentrudisstr/          # Erentrudisstr CSV-Daten
│       ├── fis_inhauser/           # FIS Inhauser CSV-Daten
│       └── kw_neukirchen/          # KW Neukirchen XLSX-Daten
├── Daten/                          # Original-Rohdaten
│   ├── Beispieldaten/              # Twin2Sim Simulationsdaten
│   ├── Monitoringdaten/            # Monitoring-Daten
│   │   ├── Erentrudisstr/          # Gebäude Erentrudisstraße
│   │   └── FIS_Inhauser/           # Friedrich-Inhauser-Straße
│   └── vertraulich_erzeugungsdaten-kw-neukirchen*/ # Kraftwerksdaten
├── docs/                           # Dokumentation
│   ├── datenlandschaft-uebersicht.md # Datenübersicht
│   └── Fehlerhafte_Daten/         # Datenqualitätsanalysen
├── venv_windows/                   # Virtuelle Umgebung
├── requirements.txt                # Python-Abhängigkeiten
├── START_DASHBOARD.bat             # Start-Skript für Windows
├── CLAUDE.md                       # Entwickler-Dokumentation
└── README.md                       # Diese Datei
```

## Systemanforderungen

- **RAM**: Mindestens 4 GB (8 GB empfohlen)
- **CPU**: Dual-Core oder besser
- **Browser**: Chrome, Firefox, Edge (aktuelle Versionen)
- **Netzwerk**: Keine Internetverbindung erforderlich (läuft lokal)

## Support

Bei Fragen oder Problemen:
1. Überprüfen Sie die Dokumentation im `docs/` Ordner
2. Konsultieren Sie die CLAUDE.md für technische Details
3. Erstellen Sie ein Issue im Repository

## Lizenz

[Lizenzinformation hier einfügen]

---

**Hinweis**: Dieses Dashboard wurde für die Analyse von Gebäudeenergiedaten in Österreich entwickelt und ist für den lokalen Betrieb optimiert.