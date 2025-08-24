"""
Column Toggle Callbacks - Fixed Circular Dependency
====================================================
Handles the interaction logic for the grouped column toggle functionality.
Fixed version without circular dependencies.
"""

from dash import Input, Output, State, ALL, MATCH, callback_context
from dash.exceptions import PreventUpdate
import pandas as pd
from ui_components_improved import create_data_table_with_full_columns


def register_column_toggle_callbacks(app):
    """
    Registers callbacks for column toggle functionality without circular dependencies.
    Only allows one-way updates to avoid cycles.
    """
    
    # Callback 1: Category checkbox toggles its columns (one-way only)
    @app.callback(
        Output({'type': 'column-toggle', 'column': ALL, 'category': MATCH}, 'value'),
        Input({'type': 'category-toggle', 'category': MATCH}, 'value'),
        State({'type': 'column-toggle', 'column': ALL, 'category': MATCH}, 'value'),
        prevent_initial_call=True
    )
    def toggle_category_columns(category_checked, column_values):
        """Toggle all columns in a category when category checkbox is clicked."""
        if callback_context.triggered:
            # Only update if the trigger came from a user click, not from another callback
            trigger_id = callback_context.triggered[0]['prop_id']
            if 'category-toggle' in trigger_id:
                # Set all columns in the category to the same state as the category checkbox
                return [category_checked] * len(column_values)
        return column_values
    
    
    # Removed the reverse callback to avoid circular dependency
    # Category checkboxes will not auto-update based on column selections
    # This prevents the circular dependency error