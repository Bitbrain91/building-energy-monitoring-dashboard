# Friedrich-Inhauser-Straße - Dokumentation

## 🏘️ Übersicht

Multi-Gebäude-Monitoring für 8 Häuser (1, 3, 5, 7, 9, 11, 13, 15) in der Friedrich-Inhauser-Straße, Salzburg. Umfasst Heizung, Kühlung, Lüftung, Wärmepumpen und PV-Anlagen.

## 📁 Verfügbare Dokumente

1. **fis-inhauser-datasets-analyse.md** ⭐  
   - Aktuelle umfassende Datensatzanalyse
   - Parameter-Vergleiche
   - Zeitliche Abdeckung
   - Empfehlungen

2. **FIS_Inhauser_Datenanalyse.md**  
   - Erste Datenexploration
   - Initiale Erkenntnisse

## 🔑 Datensatz-Übersicht

```
V1_Export (112 Parameter, Testwoche)
    ≈
export_2024-12 (111 Parameter, Q1 2025)
    ⊃
export_2025-01 (26 Parameter, Q1 2025)
```

## 📊 Hauptdatensätze

| Datei | Parameter | Zeitraum | Besonderheit |
|-------|-----------|----------|--------------|
| V1_Export | 112 | 23.-29.01.2025 | Test + PV-Daten |
| export_2024-12 | 111 | 31.12.24 - 31.03.25 | Vollständiges Monitoring |
| export_2025-01 | 26 | 01.01.25 - 31.03.25 | Wärmepumpen-Fokus |
| Main Excel | 2 | 01.01.24 - 16.05.25 | Aggregierte Daten |

## 🏠 Gebäudeüberwachung

### Pro Haus verfügbar:
- Lüftungsgerät mit Kältezähler
- Stromzähler (individuell)
- Heizkreis-Monitoring
- Raumtemperaturen

### Spezielle Systeme:
- **PV-Anlagen:** Haus 1 & 15 (nur in V1_Export)
- **Wärmepumpen:** Abluft-WP, Abwasser-WP
- **Pelletkessel:** Zentralheizung
- **Durchlauferhitzer:** Warmwasserbereitung

## 💡 Besonderheiten

- **Multi-Gebäude:** 8 separate Häuser überwacht
- **PV-Integration:** Solarstrom-Monitoring
- **Wärmepumpen:** Innovative Abwasser-Wärmenutzung
- **Nur 2 gemeinsame Parameter** zwischen allen Dateien (ungewöhnlich!)

## 📈 Datenqualität

- Konsistente 5-Minuten-Intervalle
- Vollständige Zeitreihen ohne Lücken
- Identische Werte für gemeinsame Parameter

## ⚠️ Hinweise

- Sehr unterschiedliche Parametersätze zwischen Dateien
- V1_Export enthält exklusive PV-Daten
- export_2025-01 nur für Wärmepumpen-Analyse geeignet

---
*Ordner erstellt: 22.08.2025*