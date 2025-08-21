#!/usr/bin/env python3
"""
Script to generate a comprehensive file overview of the project structure.
Creates a compact markdown documentation with hierarchical structure and links.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Directories to skip
SKIP_DIRS = {
    'venv', '__pycache__', '.git', 'node_modules', '.pytest_cache',
    '.mypy_cache', '.ruff_cache', '.claude', '.claude-flow', 
    '.hive-mind', '.roo', '.swarm', 'coordination', 'memory'
}

# File extensions to categorize
FILE_CATEGORIES = {
    'Data': ['.csv', '.json', '.xlsx', '.xls', '.parquet'],
    'Documentation': ['.md', '.txt', '.pdf'],
    'Code': ['.py', '.js', '.html', '.css'],
    'Config': ['.yaml', '.yml', '.toml', '.ini', '.conf'],
    'Test': ['test_*.py', '*_test.py'],
}

def get_file_category(file_path: str) -> str:
    """Determine the category of a file based on its extension."""
    file_name = os.path.basename(file_path)
    
    # Check for test files
    if 'test' in file_name.lower():
        return 'Test'
    
    ext = Path(file_path).suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return 'Other'

def scan_directory(root_path: str, max_depth: int = 4) -> Dict:
    """Scan directory structure and return organized information."""
    structure = {}
    root = Path(root_path)
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip unwanted directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        
        # Calculate depth
        rel_path = Path(dirpath).relative_to(root)
        depth = len(rel_path.parts)
        
        if depth > max_depth:
            continue
            
        # Get relative path for structure
        if str(rel_path) == '.':
            current = structure
        else:
            current = structure
            for part in rel_path.parts:
                if part not in current:
                    current[part] = {'_files': [], '_dirs': {}}
                current = current[part].get('_dirs', {})
                if '_files' not in current:
                    current['_files'] = []
                if '_dirs' not in current:
                    current['_dirs'] = {}
        
        # Add files with categories
        for filename in filenames[:20]:  # Limit files per directory
            category = get_file_category(filename)
            current.setdefault('_files', []).append({
                'name': filename,
                'category': category
            })
    
    return structure

def generate_markdown(structure: Dict, base_path: str = "") -> List[str]:
    """Generate markdown lines from directory structure."""
    lines = []
    
    def process_dir(data: Dict, path: str = "", indent: int = 0):
        """Recursively process directory structure."""
        prefix = "  " * indent
        
        # Sort directories
        dirs = {k: v for k, v in data.items() if k not in ['_files', '_dirs'] or (k == '_dirs' and v)}
        
        for name, content in sorted(dirs.items()):
            if name in ['_files', '_dirs']:
                continue
                
            # Directory header with link
            rel_path = f"{path}/{name}" if path else name
            lines.append(f"{prefix}- **[{name}/]({rel_path}/)**")
            
            # Process subdirectories
            if isinstance(content, dict):
                if '_dirs' in content and content['_dirs']:
                    process_dir(content['_dirs'], rel_path, indent + 1)
                
                # Group files by category
                if '_files' in content and content['_files']:
                    files_by_cat = {}
                    for file_info in content['_files']:
                        cat = file_info['category']
                        files_by_cat.setdefault(cat, []).append(file_info['name'])
                    
                    # Add categorized files
                    for category, files in sorted(files_by_cat.items()):
                        if files:
                            file_list = ', '.join(files[:5])  # Limit display
                            if len(files) > 5:
                                file_list += f" (+{len(files)-5} more)"
                            lines.append(f"{prefix}  - *{category}*: {file_list}")
    
    # Process root files
    if '_files' in structure:
        files_by_cat = {}
        for file_info in structure['_files']:
            cat = file_info['category']
            files_by_cat.setdefault(cat, []).append(file_info['name'])
        
        for category, files in sorted(files_by_cat.items()):
            if files:
                file_list = ', '.join(files[:5])
                if len(files) > 5:
                    file_list += f" (+{len(files)-5} more)"
                lines.append(f"- *{category}*: {file_list}")
    
    # Process directories
    if '_dirs' in structure:
        process_dir(structure['_dirs'])
    else:
        # Handle case where structure itself contains directories
        process_dir({k: v for k, v in structure.items() if k not in ['_files', '_dirs']})
    
    return lines

def count_files_in_dir(path: str) -> Tuple[int, Dict[str, int]]:
    """Count files in directory and return total and by type."""
    total = 0
    by_type = {}
    
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for file in files:
            total += 1
            ext = Path(file).suffix.lower()
            by_type[ext] = by_type.get(ext, 0) + 1
    
    return total, by_type

def main():
    """Main function to generate file overview."""
    root_path = "/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025"
    
    print("Scanning project structure...")
    
    # Generate overview content
    overview_lines = [
        "# 📁 Project File Overview",
        "",
        "Kompakte Übersicht der Projektstruktur für das Forschungsprojekt zur Energiedatenanalyse.",
        "",
        "## 📊 Projekt-Statistiken",
        ""
    ]
    
    # Count files in main directories
    main_dirs = ['Daten', 'docs', 'src', 'scripts', 'tests', 'archive_old_dashboards']
    stats = []
    
    for dir_name in main_dirs:
        dir_path = os.path.join(root_path, dir_name)
        if os.path.exists(dir_path):
            total, by_type = count_files_in_dir(dir_path)
            stats.append(f"- **{dir_name}/**: {total} Dateien")
    
    overview_lines.extend(stats)
    overview_lines.extend(["", "## 🗂️ Hauptverzeichnisse", ""])
    
    # Add main directory descriptions
    dir_descriptions = {
        "Daten": "Alle Projektdaten (Twin2Sim, Monitoring, Erzeugung)",
        "docs": "Dokumentation, Analysen und Dashboard-Anleitungen",
        "src": "Dashboard-Quellcode und Hauptanwendung",
        "scripts": "Hilfsskripte und Analysetools",
        "tests": "Testdateien und Validierung",
        "archive_old_dashboards": "Archivierte Dashboard-Versionen",
        "General": "Allgemeine Projektdokumente",
        "Literatur (Reini, Max, Simon)": "Forschungsliteratur und Referenzen"
    }
    
    for dir_name, desc in dir_descriptions.items():
        dir_path = os.path.join(root_path, dir_name)
        if os.path.exists(dir_path):
            overview_lines.append(f"- **[{dir_name}/]({dir_name}/)**: {desc}")
    
    overview_lines.extend(["", "## 📂 Detaillierte Struktur", ""])
    
    # Scan and add detailed structure
    structure = scan_directory(root_path, max_depth=3)
    detailed_lines = generate_markdown(structure)
    overview_lines.extend(detailed_lines)
    
    # Add specific sections for important areas
    overview_lines.extend([
        "",
        "## 🔍 Wichtige Dateien",
        "",
        "### Dashboard-Hauptdateien",
        "- [src/dashboard_v3_complete.py](src/dashboard_v3_complete.py) - Aktuelle Dashboard-Version",
        "- [docs/Dashboard_v3_Complete_Documentation.md](docs/Dashboard_v3_Complete_Documentation.md) - Vollständige Dokumentation",
        "",
        "### Datenanalysen",
        "- [docs/datenlandschaft-uebersicht.md](docs/datenlandschaft-uebersicht.md) - Gesamtübersicht aller Daten",
        "- [docs/fehlende-daten-analyse.md](docs/fehlende-daten-analyse.md) - Analyse fehlender Daten",
        "- [docs/Monitoringdaten_Erentrudisstr_Analyse.md](docs/Monitoringdaten_Erentrudisstr_Analyse.md) - Erentrudisstr. Analyse",
        "- [docs/FIS_Inhauser_Datenanalyse.md](docs/FIS_Inhauser_Datenanalyse.md) - FIS Inhauser Analyse",
        "- [docs/kw_neukirchen_datenanalyse.md](docs/kw_neukirchen_datenanalyse.md) - KW Neukirchen Analyse",
        "",
        "### Datenquellen",
        "- [Daten/Beispieldaten/](Daten/Beispieldaten/) - Twin2Sim Beispieldaten",
        "- [Daten/Monitoringdaten/Erentrudisstr/](Daten/Monitoringdaten/Erentrudisstr/) - Monitoring Erentrudisstr.",
        "- [Daten/Monitoringdaten/FIS_Inhauser/](Daten/Monitoringdaten/FIS_Inhauser/) - Monitoring FIS Inhauser",
        "- [Daten/vertraulich_erzeugungsdaten-kw-neukirchen_2025-07-21_0937/](Daten/vertraulich_erzeugungsdaten-kw-neukirchen_2025-07-21_0937/) - KW Neukirchen Erzeugungsdaten",
        "",
        "## 🛠️ Entwicklungsumgebung",
        "",
        "- **Python-Umgebung**: venv (aktiviert)",
        "- **Hauptframework**: Streamlit für Dashboard",
        "- **Datenverarbeitung**: pandas, numpy",
        "- **Visualisierung**: plotly, matplotlib",
        "",
        "## 📝 Notizen",
        "",
        "- Dashboard unterstützt alle verfügbaren Datenquellen",
        "- Automatische Erkennung von Zeitstempelspalten",
        "- Interaktive Filterung nach Datum und Variablen",
        "- Export-Funktionen für gefilterte Daten",
        "",
        "---",
        f"*Generiert am: {os.popen('date').read().strip()}*"
    ])
    
    # Write to file
    output_path = os.path.join(root_path, "docs", "fileoverview.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(overview_lines))
    
    print(f"✅ File overview generated: {output_path}")
    print(f"📊 Total lines: {len(overview_lines)}")

if __name__ == "__main__":
    main()