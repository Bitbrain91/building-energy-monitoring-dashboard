# MokiG Dashboard - Hauptversion Dokumentation

## Übersicht

Das MokiG Dashboard ist eine umfassende Datenvisualisierungs- und Analyseplattform für das Monitoring verschiedener Energiedatenquellen. Diese überarbeitete Hauptversion bietet verbesserte Funktionalität und Benutzerfreundlichkeit.

## Hauptverbesserungen

### 1. Benutzerdefinierte Parameter-Auswahl in Visualisierungen
- **Multi-Select Dropdown**: Wählen Sie beliebig viele Parameter zur Visualisierung
- **Dynamische Darstellung**: Getrennte Charts, überlagerte Ansicht oder Subplots
- **Erweiterte Optionen**: Datenglättung, Datenpunkte, Bereichsauswahl

### 2. Verbesserte Tabellendarstellung
- **Vollständige Spaltennamen**: Keine abgeschnittenen Headers mehr
- **Resizable Columns**: Spaltenbreite kann angepasst werden
- **Tooltips**: Vollständige Werte bei Hover
- **Auto-Fit**: Spalten passen sich dem Inhalt an

### 3. Konsolidierter Code
- **Eine zentrale Dashboard-Version**: Alle alten Versionen wurden entfernt
- **Modularisierte Architektur**: Klare Trennung von Datenladung, UI und Callbacks
- **Optimierte Imports**: Nur notwendige Komponenten werden geladen

### 4. Integrierte Zeitreihenanalyse
- **In Visualisierungen integriert**: Keine separate Zeitreihenanalyse-Tab mehr
- **Aggregationsoptionen**: Stündlich, täglich, wöchentlich, monatlich
- **Multi-Parameter Vergleich**: Beliebige Parameter gleichzeitig visualisieren

## Verfügbare Datenquellen

### 1. Twin2Sim
- **Dateien**: T2S_IntPV.csv, T2S_Lüftung.csv, T2S_ManiPV.csv, T2S_RAU006.csv, T2S_Wetterdaten.csv
- **Frequenz**: 1-5 Sekunden
- **Zeitraum**: 2022-01-01 bis aktuell

### 2. Erentrudisstraße
- **Monitoring-Daten**: Energieverbrauch und Gebäudetechnik
- **Frequenz**: 5 Minuten
- **Zeitraum**: 01.12.2023 bis 31.03.2025

### 3. FIS Inhauser
- **Gebäudedaten**: Friedrich-Inhauser-Straße
- **Frequenz**: 5 Minuten
- **Zeitraum**: 01.10.2024 bis 31.03.2025

### 4. KW Neukirchen
- **Kraftwerksdaten**: Erzeugung und Übergabe
- **Kraftwerke**: Dürnbach, Untersulzbach, Wiesbach
- **Frequenz**: 15 Minuten
- **Zeitraum**: 01.01.2020 bis 31.12.2024

## Bedienung

### Dashboard starten

```bash
# Im Hauptverzeichnis
python start_dashboard.py
```

Das Dashboard öffnet sich automatisch im Browser unter http://127.0.0.1:8050

### Navigation

1. **Haupttabs**: Wählen Sie zwischen den Datenquellen (Twin2Sim, Erentrudisstr., FIS Inhauser, KW Neukirchen)
2. **Dataset-Auswahl**: Wählen Sie ein spezifisches Dataset aus dem Dropdown
3. **Dataset laden**: Klicken Sie auf "Dataset laden" um die Daten zu aktivieren

### Visualisierungen

1. **Parameter auswählen**: 
   - Nutzen Sie das Multi-Select Dropdown
   - Suchen Sie nach spezifischen Parametern
   - Wählen/Abwählen durch Klick

2. **Darstellungsart**:
   - **Getrennte Charts**: Jeder Parameter in eigenem Chart
   - **Überlagert**: Alle Parameter in einem Chart
   - **Subplots**: Gestapelte Charts mit gemeinsamer X-Achse

3. **Zusatzoptionen**:
   - **Glättung**: Rolling Mean für glattere Kurven
   - **Datenpunkte**: Zeigt einzelne Messpunkte
   - **Bereichsauswahl**: Interaktiver Slider für Zeitbereich

### Datentabelle

- **Sortierung**: Klick auf Spaltenheader
- **Filterung**: Eingabefelder unter Headers
- **Selektion**: Mehrfachauswahl möglich
- **Export**: Excel-Export verfügbar

### Statistiken

- **Deskriptive Statistik**: Automatisch für alle numerischen Spalten
- **Zeitraumanalyse**: Min/Max Zeitstempel
- **Fehlende Werte**: Prozentuale Anzeige pro Spalte

## Technische Details

### Architektur

```
start_dashboard.py          # Haupteinstiegspunkt
src/
├── dashboard_main.py       # Hauptdashboard-Logik
├── data_loader_improved.py # Datenlade-Modul
├── ui_components_improved.py # UI-Komponenten
├── callbacks_improved.py   # Callback-Funktionen
└── visualization_improved.py # Erweiterte Visualisierungen
```

### Verwendete Bibliotheken

- **Dash**: Web-Framework für das Dashboard
- **Plotly**: Interaktive Visualisierungen
- **Pandas**: Datenverarbeitung
- **NumPy**: Numerische Berechnungen
- **Dash Bootstrap Components**: UI-Komponenten

### Performance-Optimierungen

- **Virtuelles Scrolling**: Für große Datentabellen
- **Lazy Loading**: Daten werden nur bei Bedarf geladen
- **Caching**: Wiederverwendung geladener Daten
- **Batch-Operationen**: Effiziente Datenverarbeitung

## Wartung und Erweiterung

### Neue Datenquelle hinzufügen

1. Daten im entsprechenden Ordner ablegen
2. `data_loader_improved.py` erweitern
3. Neue Metrik-Karte in `dashboard_main.py` hinzufügen

### Neue Visualisierung erstellen

1. Funktion in `visualization_improved.py` hinzufügen
2. Callback in `callbacks_improved.py` registrieren
3. UI-Komponente in `ui_components_improved.py` erstellen

## Fehlerbehebung

### Dashboard startet nicht
- Prüfen Sie die Python-Version (≥3.8 empfohlen)
- Installieren Sie fehlende Pakete: `pip install -r requirements.txt`
- Aktivieren Sie die virtuelle Umgebung: `venv\Scripts\activate` (Windows)

### Daten werden nicht angezeigt
- Überprüfen Sie die Dateipfade in `data_loader_improved.py`
- Stellen Sie sicher, dass die CSV/Excel-Dateien vorhanden sind
- Prüfen Sie die Konsole auf Fehlermeldungen

### Visualisierungen funktionieren nicht
- Wählen Sie mindestens einen Parameter aus
- Stellen Sie sicher, dass numerische Daten vorhanden sind
- Prüfen Sie, ob eine Datumsspalte erkannt wurde

## Support

Bei Fragen oder Problemen wenden Sie sich bitte an das Entwicklungsteam oder erstellen Sie ein Issue im Projektrepository.