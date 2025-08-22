# Durchfluss-Datei - Vollständiger Vergleich

## Übersicht
Die Durchfluss-Datei ist der minimalste Datensatz mit nur 4 Parametern.

## Dateivergleich

| Datei | Zeitraum | Datenpunkte | Parameter | Besonderheit |
|-------|----------|-------------|-----------|--------------|
| **Durchfluss** | Jahr 2024 | 89.202 | 4 | Nur Durchflüsse |
| Vp.csv | Unvollständig | 7.618 | 4 | Identische Struktur |
| Relevant_2024 | Jahr 2024 | 89.202 | 15 | Enthält Durchfluss + 11 mehr |
| Relevant-1_2024 | Jahr 2024 | 89.202 | 23 | Enthält Durchfluss + 19 mehr |
| All_24-07 | Juli 2024 | 8.322 | 45 | Enthält Durchfluss + 41 mehr |

## Parameter in Durchfluss-Datei
1. Datum + Uhrzeit
2. Durchfluss Zähler Fernwärme (m³/h)
3. Durchfluss Wasserzähler TWE (m³/h)
4. Durchfluss m³ Zähler Zirkulation (m³/h)

## Wichtige Erkenntnisse
- **Minimalster Datensatz**: Nur Volumenstrom-Messungen
- **Identisch mit Vp.csv**: Gleiche Parameter, aber mehr Datenpunkte
- **Subset aller anderen**: Jede andere Datei enthält diese Parameter
- **Datenkonsistenz**: Werte sind identisch in allen Dateien

## Verwendungszweck
Ideal für reine Durchflussanalysen und hydraulische Berechnungen ohne zusätzliche Temperatur- oder Energiedaten.
