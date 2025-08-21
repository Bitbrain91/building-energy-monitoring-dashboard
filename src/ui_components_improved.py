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
                "MokiG Dashboard - Optimierte Version"
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


def create_data_table_with_full_columns(df, table_id, max_rows=10000):
    """
    Erstellt eine verbesserte Datentabelle mit:
    - Vollständigen Spaltennamen (nicht abgeschnitten)
    - Resizable Columns
    - Besserer Datumsformatierung
    - Horizontalem Scrolling mit festen Headers
    """
    if df.empty:
        return html.Div("Keine Daten verfügbar", className="text-muted text-center p-4")
    
    # Limitiere für Performance
    display_df = df.head(max_rows).copy()
    
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
    
    return dash_table.DataTable(
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
            
            # Zeitraum-Information wenn Datumsspalte vorhanden
            html.Div(id="date-range-info", className="mb-3"),
            
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
            'default': 'Erentrudisstr.: Gebäudemonitoring-Daten (5 Min. Frequenz) mit ca. 49 Parametern. Zeitraum: 01.12.2023 - 31.03.2025.',
            'durchfluss': 'Durchflussmessungen für Heizkreise und Warmwasser.',
            '2024': 'Monitoring-Daten aus 2024 mit Energieverbrauch und Temperaturen.',
            'relevant': 'Ausgewählte relevante Parameter für Energieanalyse.'
        },
        'fis': {
            'default': 'FIS Inhauser: Gebäudedaten (5 Min. Frequenz) mit 111 Parametern. Zeitraum: 01.10.2024 - 31.03.2025.',
            'hauptdaten': 'Hauptdatensatz Q1 2025 mit allen Messpunkten.',
            'test': 'Testdaten für Validierung und Kalibrierung.',
            '250101': 'Daten Januar-März 2025.'
        },
        'kw': {
            'default': 'KW Neukirchen: Kraftwerksdaten (15 Min. Frequenz) für 3 Kraftwerke plus Netzübergabe. Zeitraum: 01.01.2020 - 31.12.2024.',
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