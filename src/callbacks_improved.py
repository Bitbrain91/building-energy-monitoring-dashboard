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
from column_toggle_component import create_enhanced_data_table
from column_toggle_callbacks import register_column_toggle_callbacks


def register_callbacks(app, ALL_DATA):
    """Registriert alle Callbacks für die App"""
    
    # Registriere Column Toggle Callbacks
    register_column_toggle_callbacks(app)
    
    # Callback for collapsing/expanding column toggle panel
    @app.callback(
        Output({'type': 'column-panel-collapse', 'id': MATCH}, 'is_open'),
        Input({'type': 'toggle-panel-btn', 'id': MATCH}, 'n_clicks'),
        State({'type': 'column-panel-collapse', 'id': MATCH}, 'is_open'),
        prevent_initial_call=True
    )
    def toggle_column_panel(n_clicks, is_open):
        """Toggle the column selection panel."""
        if n_clicks:
            return not is_open
        return is_open
    
    # Callback to update table based on column selection
    @app.callback(
        Output({'type': 'table-container', 'id': MATCH}, 'children'),
        [Input({'type': 'column-toggle', 'column': ALL, 'category': ALL}, 'value')],
        [State({'type': 'table-data-store', 'id': MATCH}, 'data')],
        prevent_initial_call=False
    )
    def update_table_columns(column_values, stored_data):
        """Update the table to show only selected columns."""
        if not stored_data:
            return html.Div("Keine Daten verfügbar")
        
        # Get context to find which table this is for
        ctx = callback_context
        
        # Extract visible columns from the callback values
        visible_columns = []
        for i, value in enumerate(column_values):
            if value:
                # Extract column name from the input id
                input_id = ctx.inputs_list[0][i]['id']
                if 'column' in input_id:
                    visible_columns.append(input_id['column'])
        
        # If no columns selected, show a message
        if not visible_columns:
            return dbc.Alert("Bitte wählen Sie mindestens eine Spalte aus", color="warning")
        
        # Create DataFrame from stored data
        df = pd.DataFrame(stored_data)
        
        # Create table with only visible columns
        return create_data_table_with_full_columns(
            df, 
            "dynamic-table",
            visible_columns=visible_columns
        )
    
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
        [Output("dataset-content", "children"),
         Output("load-dataset-btn", "children"),
         Output("load-dataset-btn", "disabled")],
        [Input("load-dataset-btn", "n_clicks")],
        [State("dataset-selector", "value"),
         State("current-source-store", "data")]
    )
    def load_dataset_content(n_clicks, selected_dataset, current_source):
        """Lädt den Inhalt für das ausgewählte Dataset mit Ladeindikator"""
        if not n_clicks or not selected_dataset or not current_source:
            return html.Div(
                "Bitte wählen Sie ein Dataset und klicken Sie auf 'Dataset laden'", 
                className="text-muted text-center p-4"
            ), [html.I(className="fas fa-download me-2"), "Dataset laden"], False
        
        # Lade das Dataset
        df = ALL_DATA.get(current_source, {}).get(selected_dataset, pd.DataFrame())
        if df.empty:
            return dbc.Alert(
                f"Dataset '{selected_dataset}' konnte nicht geladen werden.", 
                color="danger"
            ), [html.I(className="fas fa-download me-2"), "Dataset laden"], False
        
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
        ]), [html.I(className="fas fa-download me-2"), "Dataset laden"], False
    
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
                            "💡 Tipp: Nutzen Sie 'Spalten verwalten' um Spalten gruppiert ein-/auszublenden!"
                        ],
                        color="info",
                        className="mb-3"
                    ),
                    # Verwende die erweiterte Tabelle mit Column Toggle
                    create_enhanced_data_table(df, f"table-{selected_dataset}")
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