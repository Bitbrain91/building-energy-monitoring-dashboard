"""
Enhanced Column Toggle Component with Grouping
===============================================
Provides user-friendly column toggling with logical grouping.
"""

import dash
from dash import dcc, html, Input, Output, State, ALL, MATCH
import dash_bootstrap_components as dbc
import pandas as pd
import re

def categorize_columns(columns):
    """
    Categorizes columns into logical groups based on their names.
    """
    categories = {
        'Datum & Zeit': [],
        'Temperaturen': [],
        'Energie & Leistung': [],
        'Durchfluss & Volumenstrom': [],
        'Ventile & Stellwerte': [],
        'Pumpen & Motoren': [],
        'Heizkreise': [],
        'Wetter & Umgebung': [],
        'Sensoren & Messwerte': [],
        'System & Status': [],
        'Sonstige': []
    }
    
    for col in columns:
        col_lower = col.lower()
        categorized = False
        
        # Datum & Zeit
        if any(keyword in col_lower for keyword in ['date', 'zeit', 'time', 'datum', 'timestamp', 'jahr', 'monat', 'tag']):
            categories['Datum & Zeit'].append(col)
            categorized = True
        
        # Temperaturen
        elif any(keyword in col_lower for keyword in ['temp', 'temperature', '°c', 'grad', 'celsius', 'vorlauf', 'rücklauf', 'ruecklauf']):
            categories['Temperaturen'].append(col)
            categorized = True
        
        # Energie & Leistung
        elif any(keyword in col_lower for keyword in ['energie', 'energy', 'leistung', 'power', 'kwh', 'kw', 'watt', 'strom', 'spannung', 'consumption', 'verbrauch']):
            categories['Energie & Leistung'].append(col)
            categorized = True
        
        # Durchfluss & Volumenstrom
        elif any(keyword in col_lower for keyword in ['durchfluss', 'flow', 'volumenstrom', 'volume', 'l/h', 'm³', 'm3', 'liter', 'menge']):
            categories['Durchfluss & Volumenstrom'].append(col)
            categorized = True
        
        # Ventile & Stellwerte
        elif any(keyword in col_lower for keyword in ['ventil', 'valve', 'stellwert', 'stellung', 'position', 'prozent', '%', 'öffnung', 'oeffnung']):
            categories['Ventile & Stellwerte'].append(col)
            categorized = True
        
        # Pumpen & Motoren
        elif any(keyword in col_lower for keyword in ['pumpe', 'pump', 'motor', 'drehzahl', 'rpm', 'frequenz', 'hz', 'laufzeit', 'betrieb']):
            categories['Pumpen & Motoren'].append(col)
            categorized = True
        
        # Heizkreise
        elif any(keyword in col_lower for keyword in ['heizkreis', 'hk', 'hkr', 'heating', 'kreis', 'wärme', 'waerme', 'fernwärme', 'fernwaerme']):
            categories['Heizkreise'].append(col)
            categorized = True
        
        # Wetter & Umgebung
        elif any(keyword in col_lower for keyword in ['wetter', 'weather', 'außen', 'aussen', 'wind', 'regen', 'sonne', 'strahlung', 'luftfeuchte', 'humidity', 'niederschlag']):
            categories['Wetter & Umgebung'].append(col)
            categorized = True
        
        # Sensoren & Messwerte
        elif any(keyword in col_lower for keyword in ['sensor', 'messwert', 'measurement', 'fühler', 'fuehler', 'signal', 'wert', 'value', 'meldung']):
            categories['Sensoren & Messwerte'].append(col)
            categorized = True
        
        # System & Status
        elif any(keyword in col_lower for keyword in ['status', 'zustand', 'state', 'alarm', 'fehler', 'error', 'warnung', 'warning', 'betriebsart', 'mode', 'quelle']):
            categories['System & Status'].append(col)
            categorized = True
        
        # Wenn nicht kategorisiert, dann zu Sonstige
        if not categorized:
            categories['Sonstige'].append(col)
    
    # Entferne leere Kategorien
    categories = {k: v for k, v in categories.items() if v}
    
    return categories


def create_column_toggle_panel(df, table_id, visible_columns=None):
    """
    Creates an advanced column toggle panel with grouped columns.
    
    Args:
        df: DataFrame with the data
        table_id: ID for the associated table
        visible_columns: List of initially visible columns (if None, all visible)
    
    Returns:
        Dash component with the column toggle panel
    """
    if df.empty:
        return html.Div()
    
    all_columns = list(df.columns)
    if visible_columns is None:
        visible_columns = all_columns.copy()
    
    # Categorize columns
    column_categories = categorize_columns(all_columns)
    
    # Create accordion items for each category
    accordion_items = []
    
    for category, columns in column_categories.items():
        if not columns:
            continue
        
        # Check if all columns in this category are visible
        all_checked = all(col in visible_columns for col in columns)
        
        # Create checkbox for the category header
        category_id = category.replace(' ', '_').replace('&', 'and')
        
        category_header = dbc.Row([
            dbc.Col([
                dbc.Checkbox(
                    id={'type': 'category-toggle', 'category': category_id},
                    label=f"{category} ({len(columns)} Spalten)",
                    value=all_checked,
                    className="fw-bold"
                )
            ])
        ])
        
        # Create checkboxes for individual columns
        column_checkboxes = []
        for col in columns:
            column_checkboxes.append(
                dbc.Checkbox(
                    id={'type': 'column-toggle', 'column': col, 'category': category_id},
                    label=col,
                    value=col in visible_columns,
                    className="ms-4 small"
                )
            )
        
        # Create accordion item
        accordion_items.append(
            dbc.AccordionItem(
                [
                    category_header,
                    html.Hr(className="my-2"),
                    html.Div(column_checkboxes)
                ],
                title=f"{category} ({len(columns)})",
                item_id=f"item-{category_id}"
            )
        )
    
    # Create the complete panel
    panel = dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-columns me-2"),
            "Spaltenauswahl - Gruppiert nach Kategorien"
        ]),
        dbc.CardBody([
            dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                f"Insgesamt {len(all_columns)} Spalten in {len(column_categories)} Kategorien. ",
                "Klicken Sie auf eine Kategorie, um alle Spalten dieser Gruppe ein-/auszuschalten."
            ], color="info", className="mb-3"),
            
            # Info about using category checkboxes
            dbc.Alert([
                html.I(className="fas fa-lightbulb me-2"),
                html.Strong("Tipp: "),
                "Klicken Sie auf eine Kategorie-Checkbox, um alle Spalten dieser Gruppe gleichzeitig ein- oder auszuschalten."
            ], color="success", className="mb-3"),
            
            # Accordion with categories
            dbc.Accordion(
                accordion_items,
                id=f"{table_id}-column-accordion",
                start_collapsed=True,
                always_open=True
            ),
            
            # Currently visible count
            html.Div([
                html.Hr(className="my-3"),
                dbc.Badge(
                    f"{len(visible_columns)} von {len(all_columns)} Spalten sichtbar",
                    id=f"{table_id}-visible-count",
                    color="primary",
                    className="p-2"
                )
            ])
        ])
    ], className="shadow-sm mb-3")
    
    return panel


def create_enhanced_data_table(df, table_id):
    """
    Creates an enhanced data table with integrated column toggle functionality.
    
    Returns a container with both the toggle panel and the table.
    """
    from ui_components_improved import create_data_table_with_full_columns
    
    if df.empty:
        return html.Div("Keine Daten verfügbar", className="text-muted text-center p-4")
    
    # Create container with toggle button and table
    container = html.Div([
        # Toggle button to show/hide the column panel
        dbc.Button(
            [html.I(className="fas fa-columns me-2"), "Spalten verwalten"],
            id={'type': 'toggle-panel-btn', 'id': table_id},
            color="primary",
            size="sm",
            className="mb-3"
        ),
        
        # Collapsible column toggle panel
        dbc.Collapse(
            create_column_toggle_panel(df, table_id),
            id={'type': 'column-panel-collapse', 'id': table_id},
            is_open=False
        ),
        
        # The actual data table container - initialize with full table
        html.Div(
            id={'type': 'table-container', 'id': table_id},
            children=[
                create_data_table_with_full_columns(df, table_id)
            ]
        ),
        
        # Store for the dataframe
        dcc.Store(
            id={'type': 'table-data-store', 'id': table_id},
            data=df.to_dict('records')
        )
    ])
    
    return container