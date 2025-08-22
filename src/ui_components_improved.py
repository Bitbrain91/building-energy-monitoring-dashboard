"""
Verbesserte UI-Komponenten für MokiG Dashboard
===============================================
Enthält alle UI-Komponenten mit Fixes für Tabellen und Visualisierungen.
"""

import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


# Farbschema
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff9800',
    'info': '#17a2b8',
    'twin2sim': '#2E86AB',
    'erentrudis': '#A23B72',
    'fis': '#F18F01',
    'kw': '#048A81',
    'background': '#f5f7fa',
    'card': '#ffffff',
    'text': '#2c3e50'
}


def create_navbar():
    """Erstellt die Navigation"""
    return dbc.Navbar([
        dbc.Container([
            dbc.NavbarBrand([
                html.I(className="fas fa-chart-line me-2"),
                "MokiG Dashboard - Energiemonitoring"
            ], className="ms-2"),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Übersicht", href="#", id="nav-overview")),
                dbc.NavItem(dbc.NavLink("Dokumentation", href="#", id="nav-docs")),
            ], className="ms-auto", navbar=True)
        ], fluid=True)
    ], color="dark", dark=True, className="mb-4")


def create_metric_card(title, value, subtitle="", color="primary", icon=None):
    """Erstellt eine Metrik-Karte"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"fas fa-{icon} me-2", style={'color': COLORS[color]}) if icon else None,
                html.H6(title, className="text-muted mb-2")
            ], className="d-flex align-items-center"),
            html.H3(f"{value:,}" if isinstance(value, (int, float)) else value, 
                   style={'color': COLORS[color]}),
            html.Small(subtitle, className="text-muted")
        ])
    ], className="h-100 shadow-sm")


def create_data_table_with_full_columns(df, table_id, max_rows=None):
    """
    Erstellt eine verbesserte Datentabelle mit:
    - Vollständigen Spaltennamen (nicht abgeschnitten)
    - Resizable Columns
    - Besserer Datumsformatierung
    - Horizontalem Scrolling mit festen Headers
    - Intelligenter Handhabung großer Datasets
    """
    if df.empty:
        return html.Div("Keine Daten verfügbar", className="text-muted text-center p-4")
    
    # Dynamische max_rows basierend auf Dataset-Größe
    if max_rows is None:
        # Für große Datasets (>50k Zeilen), zeige alle Daten mit virtualization
        # Für kleinere Datasets, zeige alle Daten
        if len(df) > 100000:
            max_rows = 100000  # Limit für sehr große Datasets
        else:
            max_rows = len(df)  # Zeige alle Daten für normale Datasets
    
    # Bei großen Datasets, zeige die neuesten Daten zuerst wenn Date-Spalte vorhanden
    if len(df) > 20000 and 'Date' in df.columns:
        try:
            # Sortiere nach Datum absteigend (neueste zuerst)
            df = df.sort_values('Date', ascending=False)
            display_df = df.head(max_rows).copy()
            # Sortiere wieder aufsteigend für Anzeige
            display_df = display_df.sort_values('Date', ascending=True)
        except:
            display_df = df.head(max_rows).copy()
    else:
        # Limitiere für Performance
        display_df = df.head(max_rows).copy()
    
    # Füge Info-Zeile hinzu wenn Daten limitiert wurden
    is_limited = len(df) > max_rows
    
    # Formatiere Datumsspalte wenn vorhanden
    if 'Date' in display_df.columns:
        try:
            # Stelle sicher dass es datetime ist
            if not pd.api.types.is_datetime64_any_dtype(display_df['Date']):
                display_df['Date'] = pd.to_datetime(display_df['Date'], errors='coerce')
            
            # Formatiere für Anzeige
            mask = display_df['Date'].notna()
            display_df.loc[mask, 'Date'] = display_df.loc[mask, 'Date'].dt.strftime('%d.%m.%Y %H:%M:%S')
            display_df.loc[~mask, 'Date'] = ''
        except:
            pass
    
    # Erstelle Spalten-Definitionen mit vollem Namen
    columns = []
    for col in display_df.columns:
        col_def = {
            "name": str(col),  # Voller Name ohne Kürzung
            "id": str(col),
            "deletable": False,
            "selectable": True,
            "hideable": True,
            "resizable": True,  # Spalten können in der Breite angepasst werden
        }
        
        # Typ-spezifische Formatierung
        if pd.api.types.is_numeric_dtype(df[col]):
            col_def["type"] = "numeric"
            col_def["format"] = {"specifier": ",.2f"}
        
        columns.append(col_def)
    
    # Erstelle Info-Alert wenn Daten limitiert wurden
    info_alert = None
    if is_limited:
        info_alert = dbc.Alert(
            [
                html.I(className="fas fa-info-circle me-2"),
                f"Anzeige limitiert auf {max_rows:,} von {len(df):,} Zeilen für bessere Performance. ",
                "Die Daten sind vollständig geladen und in Visualisierungen verfügbar."
            ],
            color="info",
            className="mb-2"
        )
    
    table_component = dash_table.DataTable(
        id=table_id,
        columns=columns,
        data=display_df.to_dict('records'),
        
        # Virtual Scrolling für große Datenmengen
        virtualization=True,
        page_action='none',
        
        # Sortierung und Filterung
        sort_action='native',
        sort_mode='multi',
        filter_action='native',
        filter_options={'case': 'insensitive'},
        
        # Selektion
        row_selectable='multi',
        selected_rows=[],
        
        # Tabellen-Styling mit horizontalem Scrolling
        fixed_rows={'headers': True},
        style_table={
            'height': '700px',
            'overflowY': 'auto',
            'overflowX': 'auto',  # Horizontales Scrolling
            'width': '100%'
        },
        
        # Zellen-Styling für bessere Lesbarkeit
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'whiteSpace': 'normal',  # Allow text wrapping in headers
            'height': 'auto',
            'minWidth': '180px',  # Increased minimum width
            'maxWidth': '500px',  # Maximum width
        },
        
        # Header-Styling mit vollem Text
        style_header={
            'backgroundColor': COLORS['primary'],
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'left',
            'whiteSpace': 'normal',  # Erlaubt Umbruch im Header
            'height': 'auto',
            'minHeight': '50px',
            'lineHeight': '15px',
            'padding': '10px'
        },
        
        # Daten-Styling
        style_data={
            'backgroundColor': 'white',
            'color': COLORS['text'],
            'border': '1px solid #e0e0e0'
        },
        
        # Bedingte Formatierung
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            },
            {
                'if': {'state': 'selected'},
                'backgroundColor': 'rgba(46, 134, 171, 0.1)',
                'border': '2px solid ' + COLORS['primary']
            }
        ],
        
        # Tooltip für abgeschnittene Werte
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'text'}
                for column, value in row.items()
            } for row in display_df.to_dict('records')
        ] if len(display_df) < 1000 else [],  # Nur für kleinere Datasets
        
        tooltip_duration=None,
        
        # Export-Buttons
        export_format='xlsx',
        export_headers='display'
    )
    
    # Wenn Info-Alert vorhanden, kombiniere mit Tabelle
    if info_alert:
        return html.Div([info_alert, table_component])
    else:
        return table_component


def create_visualization_panel_with_defaults(df, panel_id):
    """
    Erstellt ein Visualisierungs-Panel mit:
    - Datum/Zeit als Standard X-Achse
    - Sinnvollen Defaults für Y-Achse
    - Funktionierendem Graph
    """
    if df.empty:
        return html.Div("Keine Daten für Visualisierung", className="text-muted text-center p-4")
    
    # Finde numerische Spalten für Y-Achse
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Finde Datumsspalte
    date_col = None
    for col in ['Date', 'DateTime', 'Datum + Uhrzeit', 'Zeit', 'Timestamp']:
        if col in df.columns:
            date_col = col
            break
    
    # Falls keine Datumsspalte, verwende Index oder erste Spalte
    if not date_col:
        if 'Date' in df.columns:
            date_col = 'Date'
        else:
            date_col = df.columns[0] if len(df.columns) > 0 else None
    
    # Entferne Datumsspalte aus Y-Achsen-Optionen
    y_options = [col for col in numeric_cols if col != date_col]
    
    # Wähle sinnvolle Default Y-Achse
    default_y = None
    priority_keywords = ['power', 'leistung', 'energie', 'energy', 'temperatur', 'temp', 'value', 'wert']
    for keyword in priority_keywords:
        for col in y_options:
            if keyword in col.lower():
                default_y = col
                break
        if default_y:
            break
    
    if not default_y and y_options:
        default_y = y_options[0]
    
    # Erstelle initiales Diagramm
    initial_fig = go.Figure()
    if date_col and default_y and date_col in df.columns and default_y in df.columns:
        initial_fig = go.Figure(
            data=[go.Scatter(
                x=df[date_col],
                y=df[default_y],
                mode='lines',
                name=default_y
            )]
        )
        initial_fig.update_layout(
            xaxis_title=date_col,
            yaxis_title=default_y,
            height=500,
            hovermode='x unified'
        )
    
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-chart-line me-2"),
            "Datenvisualisierung"
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("X-Achse (Zeitachse):", className="fw-bold"),
                    dcc.Dropdown(
                        id=f"{panel_id}-x-axis",
                        options=[{'label': date_col, 'value': date_col}] if date_col else [],
                        value=date_col,
                        disabled=True,  # X-Achse ist fest auf Datum
                        placeholder="Datum/Zeit"
                    )
                ], md=6),
                dbc.Col([
                    html.Label("Y-Achse (Messwerte):", className="fw-bold"),
                    dcc.Dropdown(
                        id=f"{panel_id}-y-axis",
                        options=[{'label': col, 'value': col} for col in y_options],
                        value=default_y,
                        placeholder="Wählen Sie einen Parameter..."
                    )
                ], md=6)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Label("Diagrammtyp:", className="fw-bold mt-3"),
                    dcc.RadioItems(
                        id=f"{panel_id}-chart-type",
                        options=[
                            {'label': ' Liniendiagramm', 'value': 'line'},
                            {'label': ' Balkendiagramm', 'value': 'bar'},
                            {'label': ' Streudiagramm', 'value': 'scatter'},
                            {'label': ' Flächendiagramm', 'value': 'area'}
                        ],
                        value='line',
                        inline=True
                    )
                ], md=12)
            ]),
            
            html.Hr(),
            
            # Diagramm-Container mit initialem Graph
            html.Div(id=f"{panel_id}-chart-container", children=[
                dcc.Graph(
                    id=f"{panel_id}-chart",
                    figure=initial_fig,
                    style={'height': '500px'}
                )
            ]),
            
            # Hidden Store für Daten
            dcc.Store(id=f"{panel_id}-data-store", data=df.to_dict('records')),
            
            # Zusätzliche Optionen
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        [html.I(className="fas fa-download me-2"), "Als Bild exportieren"],
                        id=f"{panel_id}-export-btn",
                        color="secondary",
                        size="sm",
                        className="mt-2"
                    )
                ])
            ])
        ])
    ], className="shadow-sm")


def create_statistics_panel(df):
    """Erstellt ein Statistik-Panel mit wichtigen Kennzahlen"""
    if df.empty:
        return html.Div("Keine Daten für Statistik", className="text-muted text-center p-4")
    
    # Berechne Statistiken
    stats = df.describe()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Erstelle Zeitraum-Information wenn Datumsspalte vorhanden
    date_range_info = None
    if 'Date' in df.columns and df['Date'].notna().any():
        try:
            date_min = df['Date'].min()
            date_max = df['Date'].max()
            date_range_info = dbc.Alert(
                [
                    html.I(className="fas fa-calendar-alt me-2"),
                    f"Zeitraum: {date_min.strftime('%d.%m.%Y %H:%M')} bis {date_max.strftime('%d.%m.%Y %H:%M')}",
                    html.Br(),
                    f"Anzahl Tage: {(date_max - date_min).days} Tage",
                    html.Br(),
                    f"Anzahl Datenpunkte: {df['Date'].notna().sum():,}"
                ],
                color="success",
                className="mb-3"
            )
        except:
            pass
    
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-calculator me-2"),
            "Statistische Auswertung"
        ]),
        dbc.CardBody([
            dbc.Alert(
                f"Dataset enthält {len(df):,} Datenpunkte über {len(df.columns)} Parameter.",
                color="info",
                className="mb-3"
            ),
            
            # Zeitraum-Information wenn vorhanden
            date_range_info if date_range_info else html.Div(),
            
            # Statistik-Tabelle für numerische Spalten
            html.H5("Statistische Kennzahlen:", className="mt-3 mb-2"),
            html.Div([
                create_data_table_with_full_columns(
                    stats.round(2).reset_index().rename(columns={'index': 'Statistik'}),
                    "stats-table",
                    max_rows=100
                )
            ]) if not stats.empty else html.Div("Keine numerischen Daten verfügbar"),
            
            # Fehlende Werte Analyse
            html.H5("Datenqualität:", className="mt-4 mb-2"),
            html.Div([
                dbc.Progress(
                    value=(1 - df.isna().sum().sum() / (len(df) * len(df.columns))) * 100,
                    label=f"{(1 - df.isna().sum().sum() / (len(df) * len(df.columns))) * 100:.1f}% vollständig",
                    color="success" if df.isna().sum().sum() == 0 else "warning"
                )
            ])
        ])
    ], className="shadow-sm")


def get_dataset_description(source, dataset_name):
    """
    Gibt eine kurze Beschreibung für das ausgewählte Dataset zurück.
    Basiert auf den Analysen in docs/.
    """
    descriptions = {
        'twin2sim': {
            'default': 'Twin2Sim: Hochauflösende Simulationsdaten (1-5 Sek. Frequenz) für PV-Anlagen, Lüftung und Wetterparameter. Zeitraum: 2022 bis aktuell.',
            'intpv': 'Integrale PV-Daten mit Leistungs- und Energiemessungen.',
            'manipv': 'Manipulierte PV-Testdaten für Simulationsszenarien.',
            'lüftung': 'Lüftungsanlagen-Daten mit Temperatur und Volumenstrom.',
            'rau006': 'Raumklimadaten für Raum 006.',
            'wetterdaten': 'Wetterdaten inkl. Temperatur, Strahlung und Niederschlag.'
        },
        'erentrudis': {
            'default': 'Erentrudisstraße: Gebäudemonitoring-Daten mit Energieverbrauch, Temperaturen und Durchflussmessungen.',
            'gesamtdaten_2024': '\ud83d\udcc1 Datei: Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv\n\u2192 Gesamtjahr 2024 mit 23 ausgewählten Parametern: Heizkreistemperaturen, Ventilstellungen, Fernwärme- und Zirkulationsdaten.',
            'detail_juli_2024': '\ud83d\udcc1 Datei: All_24-07_export_2011_2024-07-01-00-00_2024-07-31-23-59.csv\n\u2192 Detailanalyse Juli 2024 mit 44 Parametern: Alle Messgrößen inkl. Ventilstellungen, Pumpendrehzahlen, Temperaturen und Energieverbrauch für den Sommermonat.',
            'langzeit_2023_2025': '\ud83d\udcc1 Datei: export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv\n\u2192 Langzeitdaten Dezember 2023 bis März 2025 in täglicher Auflösung mit 48 Parametern: Kompletter Systemüberblick inkl. Pumpensteuerung, Puffertemperaturen, Heizkreise und Fernwärmedaten.',
            'durchfluss': 'Durchflussmessungen für Heizkreise und Warmwasser.',
            '2024': 'Monitoring-Daten aus 2024 mit Energieverbrauch und Temperaturen.',
            'relevant': 'Ausgewählte relevante Parameter für Energieanalyse.'
        },
        'fis': {
            'default': 'FIS Inhauser: Gebäudemonitoring-System mit Temperatur-, Energie- und Durchflussmessungen.',
            'export_q1_2025': '🏢 GEBÄUDEMONITORING KOMPLETT\n📅 Zeitraum: 31.12.2024 - 31.03.2025 (Q1 2025)\n⏱️ Messintervall: 5 Minuten (288 Messungen/Tag)\n📊 111 Parameter umfassend:\n   • 44 Temperaturmessungen (Heizkreise, Rücklauf, Vorlauf)\n   • 38 Strom-/Energiemessungen (Wärmepumpen, Lüftung)\n   • 14 Durchflussmessungen (Heizung, Kühlung)\n   • 14 Leistungsmessungen (kW)\n📁 Originaldatei: export_1551_2024-12-31-00-00_2025-03-31-23-55.csv',
            'data_2024_2025_at': '🌡️ AUßENTEMPERATUR-ZEITREIHE\n📅 Zeitraum: Januar 2024 - Mai 2025 (>16 Monate)\n⏱️ Messintervall: 5 Minuten (hochauflösend)\n📊 54.154 Datenpunkte - Kontinuierliche Außenfühler-Messungen für:\n   • Klimaanalysen und Heizlastberechnungen\n   • Vergleich mit Innentemperaturen\n   • Wetterabhängige Energiebedarfsanalyse\n   • Jahreszeiten-übergreifende Temperaturverläufe\n📁 Originaldatei: 2024-2025-05_AT.csv',
            'hauptdaten': 'Hauptdatensatz Q1 2025 mit allen Messpunkten.',
            'test': 'Testdaten für Validierung und Kalibrierung.',
            '250101': 'Daten Januar-März 2025.'
        },
        'kw': {
            'default': 'KW Neukirchen: Kraftwerksdaten (15 Min. Frequenz) für 3 Kraftwerke plus Netzübergabe. Zeitraum: 01.01.2020 - 31.12.2024.',
            'uebergabe_bezug_gesamt': '⚡ ÜBERGABE BEZUG - AGGREGIERTE GESAMTDATEN\n📅 Zeitraum: Januar 2020 - Dezember 2024 (5 Jahre)\n⏱️ Messintervall: 15 Minuten\n📊 Umfasst alle monatlichen Bezugsdaten vom Netz:\n   • Leistungsmessungen (kW)\n   • Energiemessungen (kWh)\n   • Netzqualitätsparameter\n📁 Aggregiert aus 60 Monatsdateien (12 Monate × 5 Jahre)',
            'uebergabe_lieferung_gesamt': '📤 ÜBERGABE LIEFERUNG - AGGREGIERTE GESAMTDATEN\n📅 Zeitraum: Januar 2020 - Dezember 2024 (5 Jahre)\n⏱️ Messintervall: 15 Minuten\n📊 Umfasst alle monatlichen Lieferdaten ins Netz:\n   • Eingespeiste Leistung (kW)\n   • Eingespeiste Energie (kWh)\n   • Einspeisequalität\n📁 Aggregiert aus 60 Monatsdateien (12 Monate × 5 Jahre)',
            'kw_duernbach_gesamt': '🏭 KRAFTWERK DÜRNBACH - ERZEUGUNGSDATEN\n📅 Zeitraum: 2020 - 2024 (5 Jahre komplett)\n⏱️ Messintervall: 15 Minuten\n💧 Wasserkraftwerk mit folgenden Parametern:\n   • Turbinenleistung (kW)\n   • Erzeugte Energie (kWh)\n   • Betriebsstunden\n   • Verfügbarkeit\n📁 Aggregiert aus 5 Jahresdateien',
            'kw_untersulzbach_gesamt': '🏭 KRAFTWERK UNTERSULZBACH - ERZEUGUNGSDATEN\n📅 Zeitraum: 2020 - 2024 (5 Jahre komplett)\n⏱️ Messintervall: 15 Minuten\n💧 Wasserkraftwerk mit folgenden Parametern:\n   • Turbinenleistung (kW)\n   • Erzeugte Energie (kWh)\n   • Betriebsstunden\n   • Verfügbarkeit\n📁 Aggregiert aus 5 Jahresdateien',
            'kw_wiesbach_gesamt': '🏭 KRAFTWERK WIESBACH - ERZEUGUNGSDATEN\n📅 Zeitraum: 2020 - 2024 (5 Jahre komplett)\n⏱️ Messintervall: 15 Minuten\n💧 Wasserkraftwerk mit folgenden Parametern:\n   • Turbinenleistung (kW)\n   • Erzeugte Energie (kWh)\n   • Betriebsstunden\n   • Verfügbarkeit\n📁 Aggregiert aus 5 Jahresdateien',
            'dürnbach': 'KW Dürnbach - Erzeugungsdaten.',
            'untersulzbach': 'KW Untersulzbach - Erzeugungsdaten.',
            'wiesbach': 'KW Wiesbach - Erzeugungsdaten.',
            'übergabe': 'Netzübergabe-Daten (Bezug/Lieferung).'
        }
    }
    
    source_desc = descriptions.get(source, {})
    
    # Suche nach passendem Dataset
    if dataset_name:
        for key in source_desc:
            if key != 'default' and key in dataset_name.lower():
                return source_desc[key]
    
    return source_desc.get('default', f'Dataset aus {source.upper()}')


def create_comparison_chart(dataframes, labels, chart_type='line'):
    """
    Erstellt ein Vergleichsdiagramm für mehrere Datasets.
    """
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set2
    
    for i, (df, label) in enumerate(zip(dataframes, labels)):
        if 'Date' in df.columns and len(df) > 0:
            # Finde erste numerische Spalte
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                y_col = numeric_cols[0]
                
                if chart_type == 'line':
                    fig.add_trace(go.Scatter(
                        x=df['Date'],
                        y=df[y_col],
                        mode='lines',
                        name=f"{label} - {y_col}",
                        line=dict(color=colors[i % len(colors)])
                    ))
                elif chart_type == 'bar':
                    fig.add_trace(go.Bar(
                        x=df['Date'],
                        y=df[y_col],
                        name=f"{label} - {y_col}",
                        marker_color=colors[i % len(colors)]
                    ))
    
    fig.update_layout(
        title="Datenvergleich",
        xaxis_title="Zeit",
        yaxis_title="Werte",
        hovermode='x unified',
        showlegend=True,
        height=500
    )
    
    return fig