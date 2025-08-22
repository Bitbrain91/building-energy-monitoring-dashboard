"""
MokiG Dashboard - Hauptversion (Refactored & Optimized)
=========================================================
Vollständig überarbeitetes Dashboard mit folgenden Verbesserungen:
- Benutzerdefinierte Parameter-Auswahl in Visualisierungen
- Verbesserte Tabellen mit vollständigen Spaltennamen und Resizing
- Konsolidierter Code ohne alte Versionen
- Integrierte Zeitreihenanalyse in Visualisierungen
- Optimierte Performance und Wartbarkeit
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from pathlib import Path
import pandas as pd

# Importiere eigene Module
from data_loader_improved import DataLoader
from ui_components_improved import (
    create_navbar, 
    create_metric_card,
    create_data_table_with_full_columns,
    create_statistics_panel,
    get_dataset_description,
    COLORS
)
from callbacks_improved import register_callbacks

# ============================================================================
# APP INITIALISIERUNG
# ============================================================================

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True
)
app.title = "MokiG Dashboard - Erentrudisstraße"

# ============================================================================
# DATEN LADEN
# ============================================================================

# Initialisiere DataLoader
BASE_PATH = Path(__file__).parent.parent
data_loader = DataLoader(BASE_PATH)

# Lade alle Daten
print("\n" + "="*60)
print("🚀 MokiG Dashboard - Erentrudisstraße Monitoring wird gestartet...")
print("="*60)
print("📊 Lade Datenquellen...")
ALL_DATA = data_loader.load_all_data()

# ============================================================================
# LAYOUT KOMPONENTEN
# ============================================================================

def create_overview_cards():
    """Erstellt die Übersichtskarten für alle Datenquellen"""
    return dbc.Row([
        dbc.Col([
            create_metric_card(
                "Twin2Sim",
                sum(len(df) for df in ALL_DATA['twin2sim'].values() if not df.empty),
                f"{len([df for df in ALL_DATA['twin2sim'].values() if not df.empty])} Datasets",
                "primary",
                "chart-area"
            )
        ], width=6, md=3),
        dbc.Col([
            create_metric_card(
                "Erentrudisstr.",
                sum(len(df) for df in ALL_DATA['erentrudis'].values() if not df.empty),
                f"{len([df for df in ALL_DATA['erentrudis'].values() if not df.empty])} Datasets",
                "info",
                "building"
            )
        ], width=6, md=3),
        dbc.Col([
            create_metric_card(
                "FIS Inhauser",
                sum(len(df) for df in ALL_DATA['fis'].values() if not df.empty),
                f"{len([df for df in ALL_DATA['fis'].values() if not df.empty])} Datasets",
                "warning",
                "industry"
            )
        ], width=6, md=3),
        dbc.Col([
            create_metric_card(
                "KW Neukirchen",
                sum(len(df) for df in ALL_DATA['kw'].values() if not df.empty),
                f"{len([df for df in ALL_DATA['kw'].values() if not df.empty])} Datasets",
                "success",
                "bolt"
            )
        ], width=6, md=3)
    ], className="mb-4")

# ============================================================================
# HAUPT-LAYOUT DEFINITION
# ============================================================================

app.layout = html.Div([
    # Navigation
    create_navbar(),
    
    # Haupt-Container
    dbc.Container([
        # Übersichtskarten
        create_overview_cards(),
        
        # Tab-Navigation
        dbc.Card([
            dbc.CardBody([
                dbc.Tabs([
                    dbc.Tab(label="Twin2Sim", tab_id="twin2sim"),
                    dbc.Tab(label="Erentrudisstr.", tab_id="erentrudis"),
                    dbc.Tab(label="FIS Inhauser", tab_id="fis"),
                    dbc.Tab(label="KW Neukirchen", tab_id="kw"),
                    dbc.Tab(label="Vergleichsansicht", tab_id="comparison")
                ], id="main-tabs", active_tab="twin2sim", className="nav-fill"),
                
                html.Hr(),
                
                # Tab-Inhalt
                html.Div(id="main-tab-content", className="mt-3")
            ])
        ], className="shadow-sm mb-4")
    ], fluid=True),
    
    # Hidden Stores für State Management
    dcc.Store(id="current-source-store"),
    dcc.Store(id="current-dataset-store")
], style={'backgroundColor': COLORS['background']})

# ============================================================================
# HAUPT-CALLBACKS
# ============================================================================

@app.callback(
    [Output("main-tab-content", "children"),
     Output("current-source-store", "data")],
    [Input("main-tabs", "active_tab")]
)
def update_main_tab(active_tab):
    """Aktualisiert den Haupttab-Inhalt"""
    if active_tab == "comparison":
        return create_comparison_view(), None
    
    # Dataset-Auswahl für die gewählte Quelle
    datasets = ALL_DATA.get(active_tab, {})
    valid_datasets = {k: v for k, v in datasets.items() if not v.empty}
    
    if not valid_datasets:
        return html.Div(
            dbc.Alert(
                f"Keine Daten für {active_tab.upper()} verfügbar.",
                color="warning"
            )
        ), active_tab
    
    # Erstelle Dropdown für Dataset-Auswahl mit deutschen Labels für Erentrudisstr
    if active_tab == "erentrudis":
        # Spezielle Labels für Erentrudisstr Datasets mit vollständigen Dateinamen
        label_mapping = {
            'gesamtdaten_2024': {
                'label': 'Gesamtdaten 2024 (23 Parameter)',
                'filename': 'Relevant-1_2024_export_2011_2024-01-01-00-00_2024-12-31-23-59 (3).csv'
            },
            'detail_juli_2024': {
                'label': 'Juli 2024 Detaildaten (44 Parameter)', 
                'filename': 'All_24-07_export_2011_2024-07-01-00-00_2024-07-31-23-59.csv'
            },
            'langzeit_2023_2025': {
                'label': 'Langzeit 2023-2025 (täglich)',
                'filename': 'export_ERS_2023-12-01-00-00_2025-03-31-23-59.csv'
            }
        }
        options = []
        for k, v in valid_datasets.items():
            if k in label_mapping and not v.empty:
                info = label_mapping[k]
                # Zeige vollständigen Dateinamen im Label
                label = f"{info['label']} - {len(v):,} Zeilen\n📁 {info['filename']}"
                options.append({'label': label, 'value': k})
    else:
        options = [{'label': f"{k} ({len(v):,} Zeilen)", 'value': k} 
                   for k, v in valid_datasets.items()]
    
    # Hole Dataset-Beschreibung
    description = get_dataset_description(active_tab, options[0]['value'] if options else None)
    
    content = dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-database me-2"),
            f"{active_tab.upper()} - Dataset Auswahl"
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Verfügbare Datasets:", className="fw-bold"),
                    dcc.Dropdown(
                        id='dataset-selector',
                        options=options,
                        value=options[0]['value'] if options else None,
                        placeholder="Dataset wählen...",
                        clearable=False,
                        style={'height': 'auto', 'minHeight': '60px'}  # Mehr Platz für mehrzeilige Labels
                    ),
                    # Dataset-Beschreibung
                    html.Div(
                        description,
                        id="dataset-description",
                        className="mt-2 text-muted small"
                    )
                ], md=8),
                dbc.Col([
                    html.Label("Aktion:", className="fw-bold"),
                    dbc.Button(
                        [html.I(className="fas fa-download me-2"), "Datensatz laden"],
                        id="load-dataset-btn",
                        color="primary",
                        className="w-100"
                    )
                ], md=4)
            ]),
            
            html.Hr(),
            
            # Sub-Tabs für verschiedene Ansichten
            html.Div(id="dataset-content", className="mt-3")
        ])
    ], className="shadow-sm")
    
    return content, active_tab

def create_comparison_view():
    """Erstellt die Vergleichsansicht für alle Datenquellen"""
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-chart-bar me-2"),
            "Datenquellen-Vergleich"
        ]),
        dbc.CardBody([
            dbc.Alert(
                "Vergleichsansicht zeigt Übersicht über alle verfügbaren Datenquellen.",
                color="info"
            ),
            dbc.Row([
                dbc.Col([
                    html.H5("Verfügbare Datenquellen:", className="mb-3"),
                    html.Ul([
                        html.Li(f"Twin2Sim: {len(ALL_DATA['twin2sim'])} Datasets"),
                        html.Li(f"Erentrudisstr.: {len(ALL_DATA['erentrudis'])} Datasets"),
                        html.Li(f"FIS Inhauser: {len(ALL_DATA['fis'])} Datasets"),
                        html.Li(f"KW Neukirchen: {len(ALL_DATA['kw'])} Datasets")
                    ])
                ], md=6),
                dbc.Col([
                    html.H5("Datenzeiträume:", className="mb-3"),
                    html.Ul([
                        html.Li("Twin2Sim: 2022-01-01 bis aktuell (1-5 Sek. Frequenz)"),
                        html.Li("Erentrudisstr.: 01.12.2023 bis 31.03.2025 (5 Min. Frequenz)"),
                        html.Li("FIS Inhauser: 01.10.2024 bis 31.03.2025 (5 Min. Frequenz)"),
                        html.Li("KW Neukirchen: 01.01.2020 bis 31.12.2024 (15 Min. Frequenz)")
                    ])
                ], md=6)
            ])
        ])
    ], className="shadow-sm")

# Registriere weitere Callbacks
register_callbacks(app, ALL_DATA)

# ============================================================================
# SERVER KONFIGURATION
# ============================================================================

# Server object for deployment
server = app.server

if __name__ == '__main__':
    print("\n" + "="*60)
    print("✅ Dashboard bereit auf http://127.0.0.1:8050")
    print("   Drücke Ctrl+C zum Beenden")
    print("="*60 + "\n")
    app.run(debug=False, host='127.0.0.1', port=8050)