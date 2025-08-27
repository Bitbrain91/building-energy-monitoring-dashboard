# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Building Energy Monitoring Dashboard - A Python-based Plotly Dash application for visualizing and analyzing energy consumption data from multiple building sites in Austria.

## Key Technologies

- **Framework**: Dash 3.2.0 with Dash Bootstrap Components
- **Data Processing**: Pandas 2.3.2, NumPy 2.3.2, PyArrow 21.0.0
- **Visualization**: Plotly 6.3.0
- **Environment**: Python with virtual environment (venv_windows)

## Development Commands

### Running the Dashboard

```bash
# Windows - Use the provided batch file
START_DASHBOARD.bat

# Or directly with Python
python src/dashboard_optimized.py
```

The dashboard runs on http://127.0.0.1:8050

### Virtual Environment Setup

```bash
# Create virtual environment
python -m venv venv_windows

# Activate (Windows)
venv_windows\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### Data Optimization

```bash
# Optimize data to Parquet format for better performance
python src/preprocess_data.py --source all
```

## Architecture Overview

### Data Sources

The application monitors four main locations with distinct data characteristics:

1. **Twin2Sim** (`Daten/Beispieldaten/`) - Simulation data with 145 parameters
2. **Erentrudisstr** (`Daten/Monitoringdaten/Erentrudisstr/`) - Single building monitoring, 49 parameters
3. **FIS_Inhauser** (`Daten/Monitoringdaten/FIS_Inhauser/`) - Multi-building (8 houses) with PV systems, 112 parameters  
4. **KW_Neukirchen** (`Daten/vertraulich_erzeugungsdaten-kw-neukirchen*/`) - Power plant generation data, 11 parameters

### Core Components

**Main Application**: `src/dashboard_optimized.py`
- Entry point for the dashboard
- Initializes Dash app with Bootstrap theme
- Loads data using OptimizedDataLoader
- Sets up layout and callbacks

**Data Loading**: `src/data_loader_optimized.py`
- OptimizedDataLoader class with caching and lazy loading
- Supports both Parquet (optimized) and CSV (fallback) formats
- In-memory cache with 5-minute TTL
- Handles multiple data sources with different formats

**UI Components**: `src/ui_components_improved.py`
- create_navbar() - Navigation bar
- create_metric_card() - KPI display cards
- create_data_table_with_full_columns() - Data tables
- create_statistics_panel() - Statistical summaries

**Callbacks**: `src/callbacks_improved.py`
- register_callbacks() - Main callback registration
- Handles data source selection, filtering, and visualization updates

**Visualization**: `src/visualization_improved.py`
- create_time_series_chart() - Time series plots
- create_heatmap() - Correlation matrices
- create_comparison_chart() - Multi-dataset comparisons

**Special Loaders**:
- `src/load_kw_aggregated.py` - Aggregates KW Neukirchen data from multiple years (2020-2024)
- `src/column_toggle_component.py` - Column visibility management for tables

### Data Flow

1. **OptimizedDataLoader** checks for Parquet files in `data_optimized/`
2. Falls back to CSV files in original locations if Parquet not found
3. Data cached in memory for 5 minutes to reduce I/O
4. Dashboard components request data through callbacks
5. Visualizations update based on user selections

### Key Patterns

- **Lazy Loading**: Data loaded on-demand, not all at startup
- **Caching Strategy**: Multi-level (memory + Parquet)
- **Error Handling**: Graceful fallbacks for missing data
- **Performance**: Optimized for datasets with 5-15 minute intervals

## Important Notes

- CSV files in Erentrudisstr may require semicolon as delimiter
- Time formats vary: `DD.MM.YYYY HH:MM` or `YYYY-MM-DD HH:MM`
- Some datasets have incomplete time series
- Virtual environment required for dependency isolation
- Dashboard supports multi-source integration and comparison views