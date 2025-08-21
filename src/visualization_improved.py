"""
Improved Visualization Component with User-Defined Parameter Selection
=======================================================================
Replaces the simple visualization with a fully customizable parameter selection.
"""

from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots


def create_advanced_visualization_panel(df, panel_id):
    """
    Creates an advanced visualization panel with user-defined parameter selection
    """
    if df.empty:
        return html.Div("Keine Daten verfügbar", className="text-muted text-center p-4")
    
    # Find date column
    date_col = None
    for col in ['Date', 'DateTime', 'Datum + Uhrzeit', 'Zeit', 'Timestamp']:
        if col in df.columns:
            date_col = col
            break
    
    if not date_col and 'Date' in df.columns:
        date_col = 'Date'
    
    # Find numeric columns for visualization
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove date column from numeric columns
    y_options = [col for col in numeric_cols if col != date_col]
    
    if not y_options:
        return dbc.Alert("Keine visualisierbaren numerischen Daten gefunden", color="warning")
    
    # Find interesting default parameters (up to 3)
    default_params = []
    priority_keywords = ['power', 'leistung', 'energie', 'energy', 'temperatur', 'temp', 'value', 'wert']
    
    # First try to find columns with priority keywords
    for keyword in priority_keywords:
        for col in y_options:
            if keyword in col.lower() and col not in default_params:
                default_params.append(col)
                if len(default_params) >= 3:
                    break
        if len(default_params) >= 3:
            break
    
    # Fill up with first columns if needed
    if len(default_params) < 3:
        for col in y_options:
            if col not in default_params:
                default_params.append(col)
                if len(default_params) >= 3:
                    break
    
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-chart-line me-2"),
            "Datenvisualisierung - Benutzerdefinierte Auswahl"
        ]),
        dbc.CardBody([
            # Information alert
            dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                f"Dataset enthält {len(y_options)} visualisierbare Parameter. ",
                "Wählen Sie beliebige Parameter zur Visualisierung aus."
            ], color="info", className="mb-3"),
            
            # Parameter selection controls
            dbc.Row([
                dbc.Col([
                    html.Label("Parameter auswählen:", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        id={'type': 'param-selector', 'index': panel_id},
                        options=[{'label': col, 'value': col} for col in y_options],
                        value=default_params,
                        multi=True,
                        placeholder="Wählen Sie Parameter zur Visualisierung...",
                        clearable=True,
                        searchable=True,
                        style={'minHeight': '40px'}
                    ),
                    html.Small(
                        "Tipp: Sie können mehrere Parameter auswählen oder abwählen", 
                        className="text-muted"
                    )
                ], md=8),
                dbc.Col([
                    html.Label("Darstellungsart:", className="fw-bold mb-2"),
                    dbc.RadioItems(
                        id={'type': 'chart-type', 'index': panel_id},
                        options=[
                            {"label": "Getrennte Charts", "value": "separate"},
                            {"label": "Überlagert", "value": "overlay"},
                            {"label": "Subplots", "value": "subplots"}
                        ],
                        value="separate",
                        inline=False
                    )
                ], md=4)
            ], className="mb-3"),
            
            # Additional options
            dbc.Row([
                dbc.Col([
                    dbc.Checklist(
                        id={'type': 'chart-options', 'index': panel_id},
                        options=[
                            {"label": "Glättung anwenden", "value": "smooth"},
                            {"label": "Datenpunkte zeigen", "value": "markers"},
                            {"label": "Bereichsauswahl aktivieren", "value": "rangeslider"}
                        ],
                        value=[],
                        inline=True,
                        switch=True
                    )
                ])
            ], className="mb-3"),
            
            # Loading spinner
            dcc.Loading(
                id={'type': 'loading-viz', 'index': panel_id},
                children=[
                    html.Div(id={'type': 'viz-container', 'index': panel_id})
                ],
                type="default",
                color="#2E86AB"
            ),
            
            # Store for data
            dcc.Store(
                id={'type': 'viz-data-store', 'index': panel_id},
                data={
                    'df': df.to_dict('records'),
                    'date_col': date_col,
                    'numeric_cols': y_options
                }
            )
        ])
    ], className="shadow-sm")


def create_visualization_figure(df_dict, selected_params, chart_type, chart_options, date_col):
    """
    Creates the actual visualization figure based on user selections
    """
    df = pd.DataFrame(df_dict)
    
    if not selected_params:
        return html.Div(
            dbc.Alert("Bitte wählen Sie mindestens einen Parameter aus", color="warning"),
            className="mt-3"
        )
    
    # Apply smoothing if requested
    apply_smoothing = 'smooth' in chart_options
    show_markers = 'markers' in chart_options
    show_rangeslider = 'rangeslider' in chart_options
    
    if apply_smoothing and date_col:
        # Apply rolling mean for smoothing
        for param in selected_params:
            if param in df.columns:
                df[f"{param}_smooth"] = df[param].rolling(window=10, min_periods=1).mean()
    
    if chart_type == "separate":
        # Create separate charts for each parameter
        figures = []
        for param in selected_params:
            if param in df.columns:
                fig = go.Figure()
                
                # Add original line
                fig.add_trace(go.Scatter(
                    x=df[date_col] if date_col else df.index,
                    y=df[param],
                    mode='lines+markers' if show_markers else 'lines',
                    name=param,
                    line=dict(width=2),
                    opacity=0.3 if apply_smoothing else 1
                ))
                
                # Add smoothed line if requested
                if apply_smoothing and f"{param}_smooth" in df.columns:
                    fig.add_trace(go.Scatter(
                        x=df[date_col] if date_col else df.index,
                        y=df[f"{param}_smooth"],
                        mode='lines',
                        name=f"{param} (geglättet)",
                        line=dict(width=2)
                    ))
                
                fig.update_layout(
                    title=f"{param}",
                    xaxis_title="Zeit" if date_col else "Index",
                    yaxis_title=param,
                    height=350,
                    hovermode='x unified',
                    template='plotly_white',
                    showlegend=apply_smoothing
                )
                
                if show_rangeslider and date_col:
                    fig.update_xaxes(rangeslider_visible=True)
                
                figures.append(dcc.Graph(figure=fig, style={'marginBottom': '20px'}))
        
        return html.Div(figures)
    
    elif chart_type == "overlay":
        # Create single chart with all parameters overlaid
        fig = go.Figure()
        
        for param in selected_params:
            if param in df.columns:
                fig.add_trace(go.Scatter(
                    x=df[date_col] if date_col else df.index,
                    y=df[param],
                    mode='lines+markers' if show_markers else 'lines',
                    name=param,
                    line=dict(width=2)
                ))
                
                if apply_smoothing and f"{param}_smooth" in df.columns:
                    fig.add_trace(go.Scatter(
                        x=df[date_col] if date_col else df.index,
                        y=df[f"{param}_smooth"],
                        mode='lines',
                        name=f"{param} (geglättet)",
                        line=dict(width=2, dash='dash')
                    ))
        
        fig.update_layout(
            title="Multi-Parameter Visualisierung",
            xaxis_title="Zeit" if date_col else "Index",
            yaxis_title="Werte",
            height=500,
            hovermode='x unified',
            template='plotly_white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        if show_rangeslider and date_col:
            fig.update_xaxes(rangeslider_visible=True)
        
        return dcc.Graph(figure=fig)
    
    else:  # subplots
        # Create subplots for each parameter
        n_params = len(selected_params)
        fig = make_subplots(
            rows=n_params,
            cols=1,
            subplot_titles=selected_params,
            shared_xaxes=True,
            vertical_spacing=0.05
        )
        
        for i, param in enumerate(selected_params, 1):
            if param in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df[date_col] if date_col else df.index,
                        y=df[param],
                        mode='lines+markers' if show_markers else 'lines',
                        name=param,
                        line=dict(width=2)
                    ),
                    row=i, col=1
                )
                
                if apply_smoothing and f"{param}_smooth" in df.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=df[date_col] if date_col else df.index,
                            y=df[f"{param}_smooth"],
                            mode='lines',
                            name=f"{param} (geglättet)",
                            line=dict(width=2, dash='dash')
                        ),
                        row=i, col=1
                    )
        
        fig.update_layout(
            height=250 * n_params,
            hovermode='x unified',
            template='plotly_white',
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Zeit" if date_col else "Index", row=n_params, col=1)
        
        if show_rangeslider and date_col:
            fig.update_xaxes(rangeslider_visible=True, row=n_params, col=1)
        
        return dcc.Graph(figure=fig)