# Datenanalyse: Erzeugungsdaten KW-Neukirchen

**Analysedatum:** 20. August 2025  
**Datenquelle:** vertraulich_erzeugungsdaten-kw-neukirchen_2025-07-21_0937

## 1. Übersicht der verfügbaren Daten

### 1.1 Datenzeitraum und Umfang
- **Zeitraum:** Januar 2020 bis Dezember 2024 (5 Jahre)
- **Gesamtanzahl Dateien:** 135 Excel-Dateien
- **Gesamtanzahl Datensätze:** 876.966 Zeilen
- **Kraftwerke:** 3 Anlagen (Dürnbach, Untersulzbach, Wiesbach)

### 1.2 Datenstruktur

Die Daten sind in drei Hauptkategorien organisiert:

| Kategorie | Anzahl Dateien | Beschreibung | Datengranularität |
|-----------|----------------|--------------|-------------------|
| **ÜBERGABE_BEZUG** | 60 | Bezugsdaten (Energieverbrauch/-beschaffung) | Monatlich, 15-Minuten-Intervalle |
| **ÜBERGABE_LIEFERUNG** | 60 | Lieferungsdaten (Energiebereitstellung) | Monatlich, 15-Minuten-Intervalle |
| **KW_ERZEUGUNG** | 15 | Erzeugungsdaten der Kraftwerke | Jährlich, 15-Minuten-Intervalle |

## 2. Detaillierte Datenanalyse

### 2.1 ÜBERGABE-Daten (Bezug und Lieferung)

#### Datenstruktur
- **Zeitliche Auflösung:** 15-Minuten-Intervalle
- **Datenpunkte pro Monat:** ~2.880-2.980 (abhängig von Monatslänge)
- **Spalten:**
  - `ZEIT_VON_UTC`: Startzeitpunkt (UTC)
  - `ZEIT_BIS_UTC`: Endzeitpunkt (UTC)
  - `WERT`: Messwert
  - `EINHEIT`: Maßeinheit

#### Datenverfügbarkeit
| Jahr | Bezug-Dateien | Lieferung-Dateien | Vollständigkeit |
|------|---------------|-------------------|-----------------|
| 2020 | 12/12 | 12/12 | 100% |
| 2021 | 12/12 | 12/12 | 100% |
| 2022 | 12/12 | 12/12 | 100% |
| 2023 | 12/12 | 12/12 | 100% |
| 2024 | 12/12 | 12/12 | 100% |

### 2.2 Kraftwerk-Erzeugungsdaten

#### Kraftwerke im Detail

**KW Dürnbach:**
- Datenzeitraum: 2020-2024
- Datenpunkte pro Jahr: ~35.040-35.137
- Durchschnittliche Energieerzeugung: 60,77 kWh
- Maximale Leistung: 292,61 kW

**KW Untersulzbach:**
- Datenzeitraum: 2020-2024
- Datenpunkte pro Jahr: ~35.040-35.137
- Identische Struktur wie Dürnbach

**KW Wiesbach:**
- Datenzeitraum: 2020-2024
- Datenpunkte pro Jahr: ~35.040-35.137
- Identische Struktur wie andere Kraftwerke

#### Datenfelder in Erzeugungsdaten
- `ZEIT_VON_UTC` / `ZEIT_BIS_UTC`: Zeitintervalle
- `WERT_ENERGIE`: Erzeugte Energie (kWh)
- `WERT_LEISTUNG`: Leistung (kW)
- `EINHEIT`: Maßeinheiten

## 3. Datenqualität und -verfügbarkeit

### 3.1 Vollständigkeitsanalyse

| Metrik | Wert |
|--------|------|
| **Zeitliche Abdeckung** | 100% (alle Monate 2020-2024) |
| **Kraftwerksabdeckung** | 100% (alle 3 Kraftwerke) |
| **Fehlende Werte** | < 0,1% |
| **Datenintegrität** | Hoch (konsistente Zeitreihen) |

### 3.2 Identifizierte Datenlücken
- **Keine systematischen Lücken** in den Zeitreihen identifiziert
- Vereinzelte fehlende Werte (< 0,1%) vermutlich durch Wartungszeiten
- Schaltjahre (2020, 2024) korrekt abgebildet mit 2.784 Einträgen im Februar

### 3.3 Datenqualitätsindikatoren
- **Konsistente Zeitintervalle:** 15-Minuten-Takt durchgehend eingehalten
- **Plausible Wertebereiche:** Keine offensichtlichen Ausreißer
- **Einheitliche Struktur:** Alle Dateien folgen demselben Schema

## 4. File-zu-Daten-Mapping

### 4.1 ÜBERGABE-Dateien (Beispiel 2024)

| Datei | Inhalt | Zeilen | Zeitraum |
|-------|--------|--------|----------|
| ÜBERGABE_BEZUG_2024.01.XLSX | Bezugsdaten Januar | 2.976 | 01.01-31.01.2024 |
| ÜBERGABE_BEZUG_2024.02.XLSX | Bezugsdaten Februar | 2.784 | 01.02-29.02.2024 |
| ... | ... | ... | ... |
| ÜBERGABE_BEZUG_2024.12.XLSX | Bezugsdaten Dezember | 2.976 | 01.12-31.12.2024 |
| ÜBERGABE_LIEFERUNG_2024.01.XLSX | Lieferungsdaten Januar | 2.976 | 01.01-31.01.2024 |
| ... | ... | ... | ... |

### 4.2 Kraftwerk-Erzeugungsdateien

| Datei | Kraftwerk | Jahr | Datenpunkte | Beschreibung |
|-------|-----------|------|-------------|--------------|
| KW DÜRNBACH_ERZEUGUNG_2020.XLSX | Dürnbach | 2020 | 35.137 | Jahreserzeugung 15-Min-Intervalle |
| KW DÜRNBACH_ERZEUGUNG_2021.XLSX | Dürnbach | 2021 | 35.041 | Jahreserzeugung 15-Min-Intervalle |
| ... | ... | ... | ... | ... |
| KW UNTERSULZBACH_ERZEUGUNG_2024.XLSX | Untersulzbach | 2024 | 35.136 | Jahreserzeugung 15-Min-Intervalle |
| KW WIESBACH_ERZEUGUNG_2024.XLSX | Wiesbach | 2024 | 35.136 | Jahreserzeugung 15-Min-Intervalle |

## 5. Statistische Kennzahlen

### 5.1 Aggregierte Statistiken

| Kennzahl | Wert |
|----------|------|
| **Gesamte Datenpunkte** | 876.966 |
| **Durchschnittliche Dateigröße** | ~300-500 KB |
| **Speicherbedarf gesamt** | ~50 MB |
| **Zeitliche Auflösung** | 15 Minuten (96 Werte/Tag) |

### 5.2 Energie-Erzeugungskennzahlen (Beispiel Dürnbach 2024)

| Metrik | Wert |
|--------|------|
| **Mittlere Energie** | 60,77 kWh pro Intervall |
| **Mittlere Leistung** | 243,06 kW |
| **Maximale Leistung** | 292,61 kW |
| **Minimale Leistung** | 0 kW |
| **Jahreserzeugung** | ~2,14 GWh (geschätzt) |

## 6. Empfehlungen für weitere Analysen

### 6.1 Zeitreihenanalyse
- **Saisonalität:** Analyse von jahreszeitlichen Mustern in der Erzeugung
- **Tagesprofile:** Identifikation typischer Tagesverläufe
- **Lastganganalyse:** Korrelation zwischen Bezug und Lieferung

### 6.2 Kraftwerksvergleich
- **Effizienzanalyse:** Vergleich der drei Kraftwerke
- **Ausfallzeiten:** Identifikation von Stillstandszeiten
- **Leistungskurven:** Analyse der Leistungscharakteristika

### 6.3 Prognosemodelle
- **Erzeugungsprognose:** Basierend auf historischen Daten
- **Bedarfsprognose:** Analyse der Bezugsdaten
- **Optimierung:** Abstimmung von Erzeugung und Bedarf

## 7. Technische Hinweise

### 7.1 Datenformat
- **Dateiformat:** Excel (.XLSX)
- **Encoding:** UTF-8
- **Zeitzone:** UTC
- **Dezimaltrennzeichen:** Punkt (.)

### 7.2 Datenverarbeitung
- Alle Dateien können mit Standard-Python-Bibliotheken (pandas, openpyxl) gelesen werden
- Konsistente Spaltenstruktur ermöglicht automatisierte Verarbeitung
- Zeitstempel sind bereits in standardisiertem Format

### 7.3 Speicheranforderungen
- Für vollständige Analyse im Arbeitsspeicher: ~2 GB RAM empfohlen
- Für zeitreihenbasierte Analysen: Chunked Processing möglich

## 8. Zusammenfassung

Die Erzeugungsdaten des KW-Neukirchen zeigen eine **ausgezeichnete Datenqualität** mit:
- **100% Datenverfügbarkeit** über 5 Jahre
- **Konsistente 15-Minuten-Auflösung**
- **Minimale fehlende Werte** (< 0,1%)
- **Drei vollständig dokumentierte Kraftwerke**

Die Datenstruktur eignet sich hervorragend für:
- Detaillierte Energieflussanalysen
- Kraftwerksoptimierung
- Prognosemodelle
- Netzstabilitätsuntersuchungen

Die einheitliche Struktur und hohe Qualität der Daten ermöglichen eine direkte Integration in bestehende Analysesysteme und die Entwicklung aussagekräftiger Dashboards zur Visualisierung der Energieerzeugung und -verteilung.