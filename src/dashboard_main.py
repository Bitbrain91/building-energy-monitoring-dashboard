"""
MokiG Dashboard - Energiemonitoring
====================================
Optimierte Version mit vollständiger Fehlerbehandlung
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from pathlib import Path
import pandas as pd
import traceback

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
app.title = "MokiG Dashboard - Energiemonitoring"

# ============================================================================
# DATEN LADEN
# ============================================================================

BASE_PATH = Path(__file__).parent.parent
data_loader = DataLoader(BASE_PATH)

print("\n" + "="*60)
print("🚀 MokiG Dashboard wird gestartet...")
print("="*60)
print("📊 Lade Datenquellen...")
ALL_DATA = data_loader.load_all_data()

# ============================================================================
# LAYOUT
# ============================================================================

def create_overview_cards():
    """Erstellt die Übersichtskarten für alle Datenquellen"""
    try:
        return dbc.Row([
            dbc.Col([
                create_metric_card(
                    "Twin2Sim",
                    sum(len(df) for df in ALL_DATA.get('twin2sim', {}).values() if not df.empty),
                    f"{len([df for df in ALL_DATA.get('twin2sim', {}).values() if not df.empty])} Datasets",
                    "primary",
                    "chart-area"
                )
            ], width=6, md=3),
            dbc.Col([
                create_metric_card(
                    "Erentrudisstraße",
                    sum(len(df) for df in ALL_DATA.get('erentrudis', {}).values() if not df.empty),
                    f"{len([df for df in ALL_DATA.get('erentrudis', {}).values() if not df.empty])} Datasets",
                    "info",
                    "building"
                )
            ], width=6, md=3),
            dbc.Col([
                create_metric_card(
                    "FIS Inhauser",
                    sum(len(df) for df in ALL_DATA.get('fis', {}).values() if not df.empty),
                    f"{len([df for df in ALL_DATA.get('fis', {}).values() if not df.empty])} Datasets",
                    "warning",
                    "industry"
                )
            ], width=6, md=3),
            dbc.Col([
                create_metric_card(
                    "KW Neukirchen",
                    sum(len(df) for df in ALL_DATA.get('kw', {}).values() if not df.empty),
                    f"{len([df for df in ALL_DATA.get('kw', {}).values() if not df.empty])} Datasets",
                    "success",
                    "bolt"
                )
            ], width=6, md=3)
        ], className="mb-4")
    except Exception as e:
        print(f"❌ FEHLER in create_overview_cards: {e}")
        return html.Div(f"Fehler beim Erstellen der Übersichtskarten: {e}")

app.layout = html.Div([
    # Navigation
    create_navbar(),
    
    # Haupt-Container
    dbc.Container([
        # Übersichtskarten
        create_overview_cards(),
        
        # Tab-Navigation mit dcc.Tabs für bessere Stabilität
        dbc.Card([
            dbc.CardBody([
                dcc.Tabs(
                    id="main-tabs",
                    value="twin2sim",
                    children=[
                        dcc.Tab(label="Twin2Sim", value="twin2sim"),
                        dcc.Tab(label="Erentrudisstraße", value="erentrudis"),
                        dcc.Tab(label="FIS Inhauser", value="fis"),
                        dcc.Tab(label="KW Neukirchen", value="kw"),
                        dcc.Tab(label="Vergleichsansicht", value="comparison")
                    ]
                ),
                
                html.Hr(),
                
                # Tab-Inhalt wird hier dynamisch geladen
                html.Div(id="main-tab-content", className="mt-3")
            ])
        ], className="shadow-sm mb-4")
    ], fluid=True),
    
    # Hidden Stores für State Management
    dcc.Store(id="current-source-store", data="twin2sim"),
    dcc.Store(id="current-dataset-store"),
    dcc.Store(id="tab-datasets-store", data={})
], style={'backgroundColor': COLORS.get('background', '#f5f7fa')})

# ============================================================================
# HAUPTCALLBACK MIT VOLLSTÄNDIGER FEHLERBEHANDLUNG
# ============================================================================

@app.callback(
    [Output("main-tab-content", "children"),
     Output("current-source-store", "data")],
    [Input("main-tabs", "value")]
)
def update_main_tab(active_tab):
    """
    Callback mit vollständiger Fehlerbehandlung
    """
    
    try:
        # Spezialfall: Vergleichsansicht
        if active_tab == "comparison":
            content = dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-bar me-2"),
                    "Datenquellen-Vergleich"
                ]),
                dbc.CardBody([
                    dbc.Alert("Vergleichsansicht zeigt Übersicht über alle verfügbaren Datenquellen.", color="info"),
                    dbc.Row([
                        dbc.Col([
                            html.H5("Verfügbare Datenquellen:", className="mb-3"),
                            html.Ul([
                                html.Li(f"Twin2Sim: {len(ALL_DATA.get('twin2sim', {}))} Datasets"),
                                html.Li(f"Erentrudisstraße: {len(ALL_DATA.get('erentrudis', {}))} Datasets"),
                                html.Li(f"FIS Inhauser: {len(ALL_DATA.get('fis', {}))} Datasets"),
                                html.Li(f"KW Neukirchen: {len(ALL_DATA.get('kw', {}))} Datasets")
                            ])
                        ], md=6),
                        dbc.Col([
                            html.H5("Datenzeiträume:", className="mb-3"),
                            html.Ul([
                                html.Li("Twin2Sim: 2022-01-01 bis aktuell"),
                                html.Li("Erentrudisstraße: 01.12.2023 bis 31.03.2025"),
                                html.Li("FIS Inhauser: 31.12.2024 bis 31.05.2025"),
                                html.Li("KW Neukirchen: 01.01.2020 bis 31.12.2024")
                            ])
                        ], md=6)
                    ])
                ])
            ], className="shadow-sm")
            return content, "comparison"  # Return 'comparison' instead of None
        
        # Hole Daten für den aktiven Tab
        
        if active_tab not in ALL_DATA:
            return html.Div(
                dbc.Alert(f"Tab '{active_tab}' nicht gefunden in Daten.", color="danger")
            ), active_tab
        
        datasets = ALL_DATA[active_tab]
        
        # Filtere leere Datasets
        valid_datasets = {}
        for k, v in datasets.items():
            if hasattr(v, 'empty'):
                if not v.empty:
                    valid_datasets[k] = v
            else:
                pass  # Dataset ist kein DataFrame
        
        
        if not valid_datasets:
            content = html.Div(
                dbc.Alert(f"Keine Daten für {active_tab.upper()} verfügbar.", color="warning")
            )
            return content, active_tab
        
        # Erstelle Dataset-Optionen basierend auf Tab
        options = []
        
        if active_tab == "erentrudis":
            # Deutsche Labels für Erentrudisstr
            label_map = {
                'gesamtdaten_2024': '📊 Jahresübersicht 2024 (89.202 Zeilen)',
                'detail_juli_2024': '🌡️ Juli 2024 Detailanalyse (8.322 Zeilen)',
                'langzeit_2023_2025': '📈 Langzeitdaten 2023-2025 (484 Zeilen)'
            }
            for key in valid_datasets:
                label = label_map.get(key, f"{key} ({len(valid_datasets[key]):,} Zeilen)")
                options.append({'label': label, 'value': key})
                
        elif active_tab == "fis":
            # Deutsche Labels für FIS
            label_map = {
                'export_q1_2025': '🏢 Gebäudemonitoring Q1 2025 (22.806 Zeilen)',
                'data_2024_2025_at': '🌡️ Außentemperatur 2024-2025 (54.154 Zeilen)'
            }
            for key in valid_datasets:
                label = label_map.get(key, f"{key} ({len(valid_datasets[key]):,} Zeilen)")
                options.append({'label': label, 'value': key})
                
        elif active_tab == "kw":
            # Spezielle Gruppierung für KW Neukirchen mit deutschen Labels
            label_map = {
                'uebergabe_bezug_gesamt': '⚡ Übergabe Bezug - Gesamtdaten 2020-2024',
                'uebergabe_lieferung_gesamt': '📤 Übergabe Lieferung - Gesamtdaten 2020-2024',
                'kw_duernbach_gesamt': '🏭 Kraftwerk Dürnbach - Erzeugung 2020-2024',
                'kw_untersulzbach_gesamt': '🏭 Kraftwerk Untersulzbach - Erzeugung 2020-2024',
                'kw_wiesbach_gesamt': '🏭 Kraftwerk Wiesbach - Erzeugung 2020-2024'
            }
            
            # Erstelle gruppierte Optionen
            for key in ['uebergabe_bezug_gesamt', 'uebergabe_lieferung_gesamt', 
                       'kw_duernbach_gesamt', 'kw_untersulzbach_gesamt', 'kw_wiesbach_gesamt']:
                if key in valid_datasets:
                    df = valid_datasets[key]
                    rows_count = len(df) if not df.empty else 0
                    label = f"{label_map.get(key, key)} ({rows_count:,} Datenpunkte)"
                    options.append({'label': label, 'value': key})
                
        else:
            # Standard Labels für andere Tabs
            for key, df in valid_datasets.items():
                options.append({'label': f"{key} ({len(df):,} Zeilen)", 'value': key})
        
        
        # Erstelle den Tab-Content
        
        # Get first dataset description
        first_value = options[0]['value'] if options else None
        try:
            description = get_dataset_description(active_tab, first_value)
        except Exception as e:
            description = f"Dataset: {first_value}"
        
        content = dbc.Card([
            dbc.CardHeader([
                html.I(className="fas fa-database me-2"),
                html.Strong(f"{active_tab.upper()} - Dataset Auswahl")
            ], style={'backgroundColor': '#f8f9fa'}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Verfügbare Datasets:", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id='dataset-selector',
                            options=options,
                            value=first_value,
                            placeholder="Dataset wählen...",
                            clearable=False
                        ),
                        html.Div(
                            description,
                            id="dataset-description",
                            className="mt-2 text-muted small"
                        )
                    ], md=8),
                    dbc.Col([
                        html.Label("Aktion:", className="fw-bold mb-2"),
                        dbc.Button(
                            [html.I(className="fas fa-download me-2"), "Dataset laden"],
                            id="load-dataset-btn",
                            color="primary",
                            className="w-100"
                        )
                    ], md=4)
                ]),
                
                html.Hr(),
                
                # Container für Dataset-Content
                html.Div(id="dataset-content", className="mt-3")
            ])
        ], className="shadow-sm")
        
        return content, active_tab
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        # Gebe eine Fehler-Anzeige zurück
        error_content = dbc.Card([
            dbc.CardHeader("❌ Fehler", style={'backgroundColor': '#ffcccc'}),
            dbc.CardBody([
                html.H5("Ein Fehler ist aufgetreten:"),
                html.Pre(str(e), style={'backgroundColor': '#f8f9fa', 'padding': '10px'}),
                html.Hr(),
                html.P(f"Tab: {active_tab}"),
                html.P("Bitte prüfen Sie die Konsole für Details.")
            ])
        ], className="shadow-sm")
        
        return error_content, active_tab

# Registriere weitere Callbacks
try:
    register_callbacks(app, ALL_DATA)
    print("✅ Callbacks erfolgreich registriert")
except Exception as e:
    print(f"❌ FEHLER beim Registrieren der Callbacks: {e}")
    traceback.print_exc()

# ============================================================================
# SERVER
# ============================================================================

server = app.server

if __name__ == '__main__':
    print("\n" + "="*60)
    print("✅ Dashboard bereit auf http://127.0.0.1:8050")
    print("   Drücke Ctrl+C zum Beenden")
    print("="*60 + "\n")
    app.run(debug=True, host='127.0.0.1', port=8050)