"""
Verbesserte Callback-Funktionen für MokiG Dashboard
====================================================
Callbacks mit Fixes für Visualisierungen und Datenauswahl.
"""

from dash import Input, Output, State, callback_context, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from ui_components_improved import (
    COLORS, 
    create_data_table_with_full_columns,
    create_visualization_panel_with_defaults,
    create_statistics_panel,
    get_dataset_description
)
from visualization_improved import create_advanced_visualization_panel, create_visualization_figure


def register_callbacks(app, ALL_DATA):
    """Registriert alle Callbacks für die App"""
    
    # Callback to save dataset selection per tab
    @app.callback(
        Output("tab-datasets-store", "data"),
        [Input("dataset-selector", "value")],
        [State("current-source-store", "data"),
         State("tab-datasets-store", "data")]
    )
    def save_tab_dataset_selection(selected_dataset, current_source, tab_datasets):
        """Speichert die Dataset-Auswahl pro Tab"""
        if not current_source or not selected_dataset:
            return tab_datasets or {}
        
        # Update the store with the current selection
        if tab_datasets is None:
            tab_datasets = {}
        tab_datasets[current_source] = selected_dataset
        return tab_datasets
    
    # Callback for custom visualization parameter selection
    @app.callback(
        Output({'type': 'viz-container', 'index': MATCH}, 'children'),
        [Input({'type': 'param-selector', 'index': MATCH}, 'value'),
         Input({'type': 'chart-type', 'index': MATCH}, 'value'),
         Input({'type': 'chart-options', 'index': MATCH}, 'value')],
        [State({'type': 'viz-data-store', 'index': MATCH}, 'data')]
    )
    def update_visualization(selected_params, chart_type, chart_options, stored_data):
        """Updates the visualization based on user parameter selection"""
        if not stored_data or not selected_params:
            return html.Div(
                dbc.Alert("Bitte wählen Sie mindestens einen Parameter aus", color="info"),
                className="mt-3"
            )
        
        df_dict = stored_data['df']
        date_col = stored_data['date_col']
        
        return create_visualization_figure(df_dict, selected_params, chart_type, chart_options or [], date_col)
    
    @app.callback(
        Output("dataset-description", "children"),
        [Input("dataset-selector", "value")],
        [State("current-source-store", "data")]
    )
    def update_dataset_description(selected_dataset, current_source):
        """Aktualisiert die Dataset-Beschreibung"""
        if not selected_dataset or not current_source:
            return ""
        
        return get_dataset_description(current_source, selected_dataset)
    
    
    @app.callback(
        Output("dataset-content", "children"),
        [Input("load-dataset-btn", "n_clicks")],
        [State("dataset-selector", "value"),
         State("current-source-store", "data")]
    )
    def load_dataset_content(n_clicks, selected_dataset, current_source):
        """Lädt den Inhalt für das ausgewählte Dataset"""
        if not n_clicks or not selected_dataset or not current_source:
            return html.Div(
                "Bitte wählen Sie ein Dataset und klicken Sie auf 'Dataset laden'", 
                className="text-muted text-center p-4"
            )
        
        # Lade das Dataset
        df = ALL_DATA.get(current_source, {}).get(selected_dataset, pd.DataFrame())
        if df.empty:
            return dbc.Alert(
                f"Dataset '{selected_dataset}' konnte nicht geladen werden.", 
                color="danger"
            )
        
        # Erstelle Sub-Tabs für verschiedene Ansichten
        return html.Div([
            dbc.Tabs([
                dbc.Tab(label="📊 Datentabelle", tab_id="table"),
                dbc.Tab(label="📈 Visualisierungen", tab_id="viz"),
                dbc.Tab(label="📉 Statistiken", tab_id="stats")
            ], id="sub-tabs", active_tab="table", className="nav-fill"),
            
            html.Div(id="sub-tab-content", className="mt-3"),
            
            # Hidden Store für aktuelles Dataset
            dcc.Store(id="current-dataset-data", data=df.to_dict('records'))
        ])
    
    @app.callback(
        Output("sub-tab-content", "children"),
        [Input("sub-tabs", "active_tab")],
        [State("dataset-selector", "value"),
         State("current-source-store", "data")]
    )
    def update_sub_tab(active_sub_tab, selected_dataset, current_source):
        """Aktualisiert den Inhalt der Sub-Tabs"""
        if not selected_dataset or not current_source:
            return html.Div("Kein Dataset geladen", className="text-muted text-center p-4")
        
        # Lade das Dataset
        df = ALL_DATA.get(current_source, {}).get(selected_dataset, pd.DataFrame())
        if df.empty:
            return html.Div("Dataset ist leer", className="text-muted text-center p-4")
        
        if active_sub_tab == "table":
            return dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-table me-2"),
                    f"Datentabelle: {selected_dataset}"
                ]),
                dbc.CardBody([
                    dbc.Alert(
                        [
                            f"📊 Dataset: {len(df):,} Zeilen × {len(df.columns)} Spalten",
                            html.Br(),
                            "💡 Tipp: Spalten sind resizable - ziehen Sie am Spaltenrand!"
                        ],
                        color="info",
                        className="mb-3"
                    ),
                    # Spezielle Behandlung für FIS Daten - zeige alle Zeilen
                    create_data_table_with_full_columns(
                        df, 
                        f"table-{selected_dataset}",
                        max_rows=None if current_source == 'fis' else None
                    )
                ])
            ], className="shadow-sm")
        
        elif active_sub_tab == "viz":
            # Use the improved visualization with user-defined parameter selection
            return create_advanced_visualization_panel(df, f"viz-{selected_dataset}")
        
        elif active_sub_tab == "stats":
            return create_statistics_panel(df)
        
        return html.Div("Tab nicht implementiert")
    



# Export für Import
__all__ = ['register_callbacks']