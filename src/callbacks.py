"""
Callback-Funktionen für MokiG Dashboard
========================================
Enthält alle Dash-Callbacks für Interaktivität.
"""

from dash import Input, Output, State, callback_context, ALL, MATCH
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json

from ui_components import COLORS, create_improved_data_table, create_visualization_panel, create_statistics_panel


def register_callbacks(app, ALL_DATA):
    """Registriert alle Callbacks für die App"""
    
    @app.callback(
        [Output("main-tab-content", "children"),
         Output("current-source-store", "data")],
        [Input("main-tabs", "active_tab")]
    )
    def update_main_tab(active_tab):
        """Aktualisiert den Haupttab-Inhalt"""
        if active_tab == "comparison":
            return create_comparison_view(ALL_DATA), None
        
        # Dataset-Auswahl für die gewählte Quelle
        datasets = ALL_DATA.get(active_tab, {})
        valid_datasets = {k: v for k, v in datasets.items() if not v.empty}
        
        if not valid_datasets:
            return html.Div(
                dbc.Alert(
                    f"Keine Daten für {active_tab.upper()} verfügbar. "
                    "Bitte überprüfen Sie die Datenpfade.",
                    color="warning"
                )
            ), active_tab
        
        # Erstelle Dropdown für Dataset-Auswahl
        options = [{'label': f"{k} ({len(v):,} Zeilen)", 'value': k} 
                   for k, v in valid_datasets.items()]
        
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
                            clearable=False
                        )
                    ], md=8),
                    dbc.Col([
                        html.Label("Aktion:", className="fw-bold"),
                        dbc.Button(
                            "Dataset laden",
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
    
    @app.callback(
        Output("dataset-content", "children"),
        [Input("load-dataset-btn", "n_clicks")],
        [State("dataset-selector", "value"),
         State("current-source-store", "data")]
    )
    def load_dataset_content(n_clicks, selected_dataset, current_source):
        """Lädt den Inhalt für das ausgewählte Dataset"""
        if not n_clicks or not selected_dataset or not current_source:
            return html.Div("Bitte wählen Sie ein Dataset und klicken Sie auf 'Dataset laden'", 
                           className="text-muted text-center p-4")
        
        # Lade das Dataset
        df = ALL_DATA.get(current_source, {}).get(selected_dataset, pd.DataFrame())
        if df.empty:
            return dbc.Alert(f"Dataset '{selected_dataset}' konnte nicht geladen werden.", color="danger")
        
        # Erstelle Sub-Tabs für verschiedene Ansichten
        return dbc.Tabs([
            dbc.Tab(label="Datentabelle", tab_id="table"),
            dbc.Tab(label="Visualisierungen", tab_id="viz"),
            dbc.Tab(label="Statistiken", tab_id="stats"),
            dbc.Tab(label="Zeitreihenanalyse", tab_id="timeseries")
        ], id="sub-tabs", active_tab="table"), html.Div(id="sub-tab-content", className="mt-3")
    
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
                        f"Dataset enthält {len(df):,} Zeilen und {len(df.columns)} Spalten. "
                        "Die Tabelle unterstützt jetzt virtuelles Scrolling - Sie können kontinuierlich scrollen!",
                        color="info",
                        className="mb-3"
                    ),
                    create_improved_data_table(df, f"table-{selected_dataset}")
                ])
            ], className="shadow-sm")
        
        elif active_sub_tab == "viz":
            return create_visualization_panel(df, f"viz-{selected_dataset}")
        
        elif active_sub_tab == "stats":
            return create_statistics_panel(df)
        
        elif active_sub_tab == "timeseries":
            return create_timeseries_analysis(df, selected_dataset)
        
        return html.Div("Tab nicht implementiert")
    
    @app.callback(
        Output('comparison-output', 'children'),
        [Input('create-comparison-btn', 'n_clicks')],
        [State('comparison-selector', 'value')]
    )
    def update_comparison_output(n_clicks, selected_series):
        """Erstellt den Vergleichs-Output"""
        if not n_clicks or not selected_series:
            return html.Div("Wählen Sie Datensätze und klicken Sie auf 'Vergleich erstellen'", 
                           className="text-muted text-center p-4")
        
        fig = go.Figure()
        colors = px.colors.qualitative.Plotly
        
        for i, series_json in enumerate(selected_series[:5]):  # Max 5 Serien
            series = json.loads(series_json)
            df = ALL_DATA[series['source']][series['dataset']]
            
            if not df.empty and series['column'] in df.columns:
                # Verwende Datum wenn vorhanden, sonst Index
                x_data = df['Date'] if 'Date' in df.columns else df.index
                
                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=df[series['column']],
                    mode='lines',
                    name=f"{series['source']}/{series['dataset']}/{series['column']}",  # Volle Namen
                    line=dict(color=colors[i % len(colors)])
                ))
        
        fig.update_layout(
            title="Datenvergleich",
            xaxis_title="Zeit/Index",
            yaxis_title="Werte",
            height=600,
            hovermode='x unified',
            template="plotly_white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return dcc.Graph(figure=fig)
    
    # Callback für dynamische Visualisierungen
    @app.callback(
        Output({'type': 'viz-output', 'index': MATCH}, 'children'),
        [Input({'type': 'viz-btn', 'index': MATCH}, 'n_clicks')],
        [State({'type': 'viz-type', 'index': MATCH}, 'value'),
         State({'type': 'param-select', 'index': MATCH}, 'value'),
         State({'type': 'agg-select', 'index': MATCH}, 'value'),
         State("dataset-selector", "value"),
         State("current-source-store", "data")]
    )
    def create_dynamic_visualization(n_clicks, viz_type, selected_params, agg_type, dataset, source):
        """Erstellt dynamische Visualisierungen basierend auf Benutzerauswahl"""
        if not n_clicks or not dataset or not source:
            return html.Div("Konfigurieren Sie die Visualisierung und klicken Sie auf 'Visualisieren'", 
                           className="text-muted text-center p-4")
        
        df = ALL_DATA.get(source, {}).get(dataset, pd.DataFrame())
        if df.empty:
            return html.Div("Keine Daten verfügbar", className="text-muted")
        
        if not selected_params:
            return dbc.Alert("Bitte wählen Sie mindestens einen Parameter", color="warning")
        
        # Aggregation anwenden wenn gewünscht
        if agg_type != 'none' and 'Date' in df.columns:
            try:
                df_agg = df.set_index('Date')[selected_params].resample(agg_type).mean().reset_index()
                df = df_agg
            except:
                pass  # Falls Aggregation fehlschlägt, verwende Original-Daten
        
        # Erstelle Visualisierung basierend auf Typ
        fig = create_chart_by_type(df, viz_type, selected_params)
        
        if fig:
            fig.update_layout(height=500, template="plotly_white", hovermode='closest')
            return dcc.Graph(figure=fig)
        
        return dbc.Alert(f"Visualisierungstyp '{viz_type}' konnte nicht erstellt werden", color="danger")


def create_chart_by_type(df, viz_type, selected_params):
    """Erstellt verschiedene Chart-Typen"""
    
    if viz_type == 'line':
        fig = go.Figure()
        for param in selected_params:
            if param in df.columns:
                x_data = df['Date'] if 'Date' in df.columns else df.index
                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=df[param],
                    mode='lines+markers',
                    name=param
                ))
        fig.update_layout(title="Liniendiagramm", xaxis_title="Zeit", yaxis_title="Werte")
        return fig
    
    elif viz_type == 'bar':
        df_sample = df.sample(min(50, len(df))) if len(df) > 50 else df
        fig = go.Figure()
        for param in selected_params:
            if param in df_sample.columns:
                fig.add_trace(go.Bar(
                    x=df_sample.index,
                    y=df_sample[param],
                    name=param
                ))
        fig.update_layout(title="Balkendiagramm", xaxis_title="Index", yaxis_title="Werte")
        return fig
    
    elif viz_type == 'scatter':
        if len(selected_params) >= 2:
            return px.scatter(df, x=selected_params[0], y=selected_params[1],
                           title=f"Streudiagramm: {selected_params[0]} vs {selected_params[1]}")
        return None
    
    elif viz_type == 'heatmap':
        corr_matrix = df[selected_params].corr()
        return px.imshow(corr_matrix, 
                       labels=dict(color="Korrelation"),
                       x=selected_params,
                       y=selected_params,
                       color_continuous_scale='RdBu',
                       title="Korrelations-Heatmap")
    
    elif viz_type == 'box':
        fig = go.Figure()
        for param in selected_params:
            if param in df.columns:
                fig.add_trace(go.Box(y=df[param], name=param))
        fig.update_layout(title="Box Plot", yaxis_title="Werte")
        return fig
    
    elif viz_type == 'histogram':
        fig = go.Figure()
        for param in selected_params:
            if param in df.columns:
                fig.add_trace(go.Histogram(x=df[param], name=param, opacity=0.7))
        fig.update_layout(title="Histogramm", xaxis_title="Werte", yaxis_title="Häufigkeit",
                         barmode='overlay')
        return fig
    
    elif viz_type == 'violin':
        fig = go.Figure()
        for param in selected_params:
            if param in df.columns:
                fig.add_trace(go.Violin(y=df[param], name=param, box_visible=True))
        fig.update_layout(title="Violin Plot", yaxis_title="Werte")
        return fig
    
    elif viz_type == 'scatter3d':
        if len(selected_params) >= 3:
            return px.scatter_3d(df, x=selected_params[0], y=selected_params[1], z=selected_params[2],
                              title="3D Streudiagramm")
        return None
    
    return None


def create_timeseries_analysis(df, dataset_name):
    """Erstellt eine Zeitreihenanalyse"""
    if 'Date' not in df.columns:
        return dbc.Alert("Keine Zeitreihen-Daten verfügbar (keine Datumsspalte gefunden)", color="warning")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        return dbc.Alert("Keine numerischen Spalten für Zeitreihenanalyse verfügbar", color="warning")
    
    # Erstelle mehrere Zeitreihen-Charts
    charts = []
    
    # 1. Übersichts-Chart mit allen numerischen Spalten
    fig_overview = go.Figure()
    for col in numeric_cols[:5]:  # Max 5 Linien
        fig_overview.add_trace(go.Scatter(
            x=df['Date'],
            y=df[col],
            mode='lines',
            name=col,  # Voller Name
            hovertemplate='%{x}<br>%{y:.2f}<extra>%{fullData.name}</extra>'
        ))
    
    fig_overview.update_layout(
        title=f"Zeitreihenübersicht: {dataset_name}",
        xaxis_title="Zeit",
        yaxis_title="Werte",
        height=400,
        hovermode='x unified',
        template="plotly_white"
    )
    
    charts.append(dcc.Graph(figure=fig_overview))
    
    # 2. Tagesverlauf-Analyse (wenn genug Daten)
    if len(df) > 100 and len(numeric_cols) > 0:
        try:
            df_daily = df.set_index('Date')[numeric_cols[0]].resample('D').agg(['mean', 'min', 'max'])
            
            fig_daily = go.Figure()
            fig_daily.add_trace(go.Scatter(
                x=df_daily.index,
                y=df_daily['mean'],
                mode='lines',
                name='Mittelwert',
                line=dict(color='blue')
            ))
            fig_daily.add_trace(go.Scatter(
                x=df_daily.index,
                y=df_daily['max'],
                mode='lines',
                name='Maximum',
                line=dict(color='red', dash='dash')
            ))
            fig_daily.add_trace(go.Scatter(
                x=df_daily.index,
                y=df_daily['min'],
                mode='lines',
                name='Minimum',
                line=dict(color='green', dash='dash')
            ))
            
            fig_daily.update_layout(
                title=f"Tagesaggregation: {numeric_cols[0]}",
                xaxis_title="Datum",
                yaxis_title="Werte",
                height=400,
                template="plotly_white"
            )
            
            charts.append(dcc.Graph(figure=fig_daily))
        except:
            pass  # Falls Aggregation fehlschlägt
    
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-chart-line me-2"),
            f"Zeitreihenanalyse: {dataset_name}"
        ]),
        dbc.CardBody(charts)
    ], className="shadow-sm")


def create_comparison_view(ALL_DATA):
    """Erstellt die Vergleichsansicht für mehrere Datenquellen"""
    all_options = []
    
    # Sammle alle verfügbaren Datensätze
    for source, datasets in ALL_DATA.items():
        for key, df in datasets.items():
            if not df.empty:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols[:5]:  # Max 5 Spalten pro Dataset
                    all_options.append({
                        'label': f"{source}/{key}/{col}",  # Volle Namen
                        'value': json.dumps({
                            'source': source,
                            'dataset': key,
                            'column': col
                        })
                    })
    
    if not all_options:
        return dbc.Alert("Keine Daten für Vergleich verfügbar", color="warning")
    
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-chart-line me-2"),
            "Multi-Datenquellen Vergleich"
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Wählen Sie Datensätze zum Vergleich (max. 5):", className="fw-bold"),
                    dcc.Dropdown(
                        id='comparison-selector',
                        options=all_options[:200],  # Erhöht von 100 auf 200
                        multi=True,
                        placeholder="Datensätze wählen...",
                        maxHeight=400
                    )
                ], md=8),
                dbc.Col([
                    html.Label("Visualisierung:", className="fw-bold"),
                    dbc.Button(
                        "Vergleich erstellen",
                        id="create-comparison-btn",
                        color="primary",
                        className="w-100"
                    )
                ], md=4)
            ]),
            
            html.Hr(),
            
            dcc.Loading(
                id="loading-comparison",
                type="default",
                children=[
                    html.Div(id='comparison-output')
                ]
            )
        ])
    ], className="shadow-sm")