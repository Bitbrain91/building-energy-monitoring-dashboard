# 📊 Datenqualitäts-Analyse Report

**Stand:** 27.08.2025 15:42 Uhr

---

## 🎯 Schnellübersicht

| Datensatz | Dateien | Kritische Fehler | Hauptprobleme |
|-----------|---------|------------------|---------------|
| **Erentrudisstr** | 3 | ⚠️ Hoch | 60% fehlende Zeitstempel, 17 Parameter ohne Daten |
| **FIS_Inhauser** | 2 | ✅ Keine | Zeitlücken, negative Kälteleistung |
| **Twin2Sim** | 5 | ✅ Gering | Vereinzelt fehlende Zeitstempel |
| **KW_Neukirchen** | 135 | ⚠️ Mittel | Duplizierte Zeitstempel in allen Dateien |

---

## 🔴 Kritische Fehler (Sofortmaßnahmen erforderlich)

### Erentrudisstr
**Zeitraum:** 2024
- **Fehlende Zeitstempel:** Alle 3 CSV-Dateien betroffen (>60% Datenverlust)
- **Komplett fehlende Parameter:**
  - Drehzahl Pumpe Zirkulation sekundär
  - Ventil HK1 Ost / HK2 West / Fernwärme
  - Pumpe Pufferladung
  - Status KWZ

### KW_Neukirchen
**Zeitraum:** 2020-2024
- **Duplizierte Zeitstempel:** Alle 15 Hauptdateien
- **Betroffene Kraftwerke:** Dürnbach, Untersulzbach, Wiesbach

---

## 📁 Detailanalyse nach Datensatz

### 1️⃣ Erentrudisstr

| Problem | Betroffene Parameter | Zeitraum |
|---------|---------------------|----------|
| **Zeitstempel fehlen** | Alle Parameter | Jul 2024, Dez 2023 - März 2025, Jan-Dez 2024 |
| **Zeitlücken** | Alle Parameter | Unregelmäßige Intervalle |
| **Ausreißer** | Vorlauf HK2 West (°C)<br>Leistung Fernwärme (W)<br>Zirkulation Wohnungen (°C) | Gesamter Zeitraum |
| **Negative Leistung** | Leistung Zähler Fernwärme | Jan-Dez 2024 |
| **100% Datenverlust** | 5 Pumpen/Ventil-Parameter | Gesamter Zeitraum |

### 2️⃣ FIS_Inhauser

| Problem | Betroffene Parameter | Zeitraum |
|---------|---------------------|----------|
| **Zeitlücken** | Alle Parameter | 2024-2025 |
| **Negative Leistung** | Kältezähler Haus 5, 9, 11 | Dez 2024 - März 2025 |
| **Ausreißer** | Außenfühler<br>Stromzähler Haus 7<br>Kältezähler Haus 13 | Vereinzelt |

### 3️⃣ Twin2Sim

| Problem | Betroffene Parameter | Zeitraum |
|---------|---------------------|----------|
| **Zeitstempel fehlen** | Alle 5 Dateien (minimal) | 23.-28. Juni 2025 |
| **Kurzer Zeitraum** | Alle Parameter | Nur 5 Tage Daten |

### 4️⃣ KW_Neukirchen

| Problem | Betroffene Parameter | Zeitraum |
|---------|---------------------|----------|
| **Duplizierte Zeit** | Alle Erzeugungsdaten | 2020-2024 (Jahreswechsel) |
| **Struktur** | 135 Einzeldateien statt Gesamtdatei | Monatliche Aufteilung |

---

## ✅ Handlungsempfehlungen

### Sofortmaßnahmen
1. **Erentrudisstr:** Zeitstempel-Import prüfen (Delimiter, Format)
2. **KW_Neukirchen:** Duplikate bei Jahreswechsel bereinigen
3. **Alle Datensätze:** Einheitliches Zeitstempel-Format etablieren

### Mittelfristig
- Automatische Datenvalidierung beim Import
- Plausibilitätsprüfungen für Leistungswerte
- Konsolidierung der KW_Neukirchen Dateien

### Parameter-Prioritäten
🔴 **Kritisch:** Fehlende Zeitstempel (Erentrudisstr)
🟠 **Wichtig:** Negative Leistungswerte, Duplikate
🟡 **Normal:** Ausreißer, Zeitlücken

---


*Report automatisch generiert - Fokus auf Parameter und Zeiträume*