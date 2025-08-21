"""
UI-Komponenten für MokiG Dashboard
===================================
Enthält alle wiederverwendbaren UI-Komponenten.
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
                "MokiG Dashboard v4.0 - Refactored"
            ], className="ms-2"),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Übersicht", href="#", id="nav-overview")),
                dbc.NavItem(dbc.NavLink("Dokumentation", href="#", id="nav-docs")),
                dbc.NavItem(
                    dbc.Button(
                        [html.I(className="fas fa-sync-alt me-2"), "Aktualisieren"],
                        id="refresh-btn",
                        color="primary",
                        size="sm",
                        className="ms-2"
                    )
                )
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


def create_improved_data_table(df, table_id, max_rows=10000):
    """
    Erstellt eine verbesserte interaktive Datentabelle mit:
    - Vollen Spaltennamen (nicht abgeschnitten)
    - Virtual Scrolling für große Datenmengen
    - Besserer Formatierung von Datumsspalten
    """
    if df.empty:
        return html.Div("Keine Daten verfügbar", className="text-muted text-center p-4")
    
    # Limitiere Spalten für Performance
    display_cols = list(df.columns)[:50]  # Erhöht von 30 auf 50
    display_df = df[display_cols].head(max_rows).copy()
    
    # Formatiere Datumsspalten besser
    if 'Date' in display_df.columns:
        try:
            # Stelle sicher, dass Date als datetime vorliegt
            if not pd.api.types.is_datetime64_any_dtype(display_df['Date']):
                display_df['Date'] = pd.to_datetime(display_df['Date'], errors='coerce')
            
            # Formatiere nur gültige Datumswerte
            mask = display_df['Date'].notna()
            display_df.loc[mask, 'Date'] = display_df.loc[mask, 'Date'].dt.strftime('%d.%m.%Y %H:%M:%S')
            display_df.loc[~mask, 'Date'] = ''  # Leere String statt NaT
        except Exception as e:
            print(f"Warnung bei Datumsformatierung: {e}")
    
    columns = []
    for col in display_cols:
        col_def = {
            "name": str(col),  # Voller Spaltenname ohne Kürzung
            "id": col,
            "deletable": False,
            "selectable": True,
            "hideable": True,
            "presentation": "markdown" if len(str(col)) > 30 else "input"  # Markdown für lange Namen
        }
        
        # Typ-spezifische Formatierung
        if pd.api.types.is_numeric_dtype(df[col]):
            col_def["type"] = "numeric"
            col_def["format"] = {"specifier": ",.2f"}
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            col_def["type"] = "text"  # Als Text für bessere Darstellung
        
        columns.append(col_def)
    
    return dash_table.DataTable(
        id=table_id,
        columns=columns,
        data=display_df.to_dict('records'),
        
        # Virtual Scrolling statt Paging für kontinuierliches Scrollen
        virtualization=True,
        
        # Erhöhte Seitengröße für virtuelles Scrolling
        page_action='none',  # Deaktiviert Paging
        
        # Sorting
        sort_action='native',
        sort_mode='multi',
        
        # Filtering
        filter_action='native',
        filter_options={'case': 'insensitive'},
        
        # Selection
        row_selectable='multi',
        selected_rows=[],
        
        # Scrolling mit fixer Header-Zeile
        fixed_rows={'headers': True},
        style_table={
            'height': '700px',  # Erhöht von 600px
            'overflowY': 'auto',
            'overflowX': 'auto'
        },
        
        # Zellen-Styling mit besserer Spaltenbreite
        style_cell={
            'textAlign': 'left',
            'padding': '12px',
            'whiteSpace': 'normal',
            'height': 'auto',
            'minWidth': '120px',  # Erhöht von 100px
            'maxWidth': '400px',  # Erhöht von 300px
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        
        # Header-Styling mit Wrap für lange Spaltennamen
        style_header={
            'backgroundColor': COLORS['primary'],
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'whiteSpace': 'normal',
            'height': 'auto',
            'minHeight': '40px',
            'maxHeight': '80px',
            'overflow': 'hidden'
        },
        
        style_data={
            'backgroundColor': 'white',
            'color': COLORS['text'],
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            },
            {
                'if': {'state': 'selected'},
                'backgroundColor': 'rgba(46, 134, 171, 0.1)',
                'border': '1px solid ' + COLORS['primary']
            }
        ],
        
        # Zellen-Tooltips für lange Inhalte
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
                if len(str(value)) > 50  # Tooltip nur für lange Werte
            } for row in display_df.to_dict('records')
        ] if len(display_df) < 100 else None,  # Tooltips nur für kleine Datasets
        
        tooltip_duration=None,
        
        # Export
        export_format='csv',
        export_headers='display',
        
        # Zusätzliche Optionen für bessere Performance
        style_as_list_view=True,
    )


def create_visualization_panel(df, panel_id):
    """Erstellt ein umfassendes Visualisierungspanel"""
    if df.empty:
        return html.Div("Keine Daten für Visualisierung verfügbar", 
                       className="text-muted text-center p-4")
    
    # Identifiziere Spaltentypen
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    has_date = 'Date' in df.columns or len(date_cols) > 0
    
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-chart-bar me-2"),
            "Visualisierungsoptionen"
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Visualisierungstyp:", className="fw-bold"),
                    dcc.Dropdown(
                        id={'type': 'viz-type', 'index': panel_id},
                        options=[
                            {'label': 'Liniendiagramm', 'value': 'line'},
                            {'label': 'Balkendiagramm', 'value': 'bar'},
                            {'label': 'Streudiagramm', 'value': 'scatter'},
                            {'label': 'Heatmap', 'value': 'heatmap'},
                            {'label': 'Box Plot', 'value': 'box'},
                            {'label': 'Histogramm', 'value': 'histogram'},
                            {'label': 'Violin Plot', 'value': 'violin'},
                            {'label': '3D Scatter', 'value': 'scatter3d'}
                        ],
                        value='line' if has_date else 'bar',
                        clearable=False
                    )
                ], md=3),
                
                dbc.Col([
                    html.Label("Parameter auswählen:", className="fw-bold"),
                    dcc.Dropdown(
                        id={'type': 'param-select', 'index': panel_id},
                        options=[{'label': col, 'value': col} for col in numeric_cols],  # Volle Namen
                        value=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols,
                        multi=True,
                        placeholder="Wähle Parameter...",
                        optionHeight=50  # Mehr Platz für lange Namen
                    )
                ], md=5),
                
                dbc.Col([
                    html.Label("Aggregation:", className="fw-bold"),
                    dcc.Dropdown(
                        id={'type': 'agg-select', 'index': panel_id},
                        options=[
                            {'label': 'Keine', 'value': 'none'},
                            {'label': 'Stündlich', 'value': 'H'},
                            {'label': 'Täglich', 'value': 'D'},
                            {'label': 'Wöchentlich', 'value': 'W'},
                            {'label': 'Monatlich', 'value': 'M'}
                        ],
                        value='none',
                        clearable=False
                    )
                ], md=2),
                
                dbc.Col([
                    html.Label("Aktion:", className="fw-bold"),
                    dbc.Button(
                        "Visualisieren",
                        id={'type': 'viz-btn', 'index': panel_id},
                        color="primary",
                        className="w-100"
                    )
                ], md=2)
            ], className="mb-3"),
            
            # Zeitbereich-Slider (wenn Datum vorhanden)
            html.Div(id={'type': 'time-controls', 'index': panel_id}),
            
            # Chart-Container
            dcc.Loading(
                id={'type': 'loading', 'index': panel_id},
                type="default",
                children=[
                    html.Div(id={'type': 'viz-output', 'index': panel_id})
                ]
            )
        ])
    ], className="shadow-sm")


def create_statistics_panel(df):
    """Erstellt ein Statistik-Panel"""
    if df.empty:
        return html.Div("Keine Daten für Statistiken verfügbar", 
                       className="text-muted text-center p-4")
    
    stats = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols[:15]:  # Erhöht von 10 auf 15
        col_stats = {
            'Parameter': col,  # Voller Name
            'Anzahl': df[col].count(),
            'Mittelwert': df[col].mean(),
            'Std.Abw.': df[col].std(),
            'Min': df[col].min(),
            '25%': df[col].quantile(0.25),
            'Median': df[col].median(),
            '75%': df[col].quantile(0.75),
            'Max': df[col].max(),
            'Fehlend': df[col].isna().sum()
        }
        stats.append(col_stats)
    
    stats_df = pd.DataFrame(stats)
    
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-calculator me-2"),
            "Statistische Übersicht"
        ]),
        dbc.CardBody([
            create_improved_data_table(stats_df, "stats-table", max_rows=100)
        ])
    ], className="shadow-sm")