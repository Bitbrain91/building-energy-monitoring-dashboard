#!/usr/bin/env python3
"""
Scan the Daten/ directory structure and create a comprehensive overview
of all data files with their locations and basic metadata.
"""

import os
import json
from pathlib import Path
from datetime import datetime
import mimetypes

def get_file_info(filepath):
    """Get basic information about a file."""
    try:
        stat = os.stat(filepath)
        size = stat.st_size
        modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
        
        # Determine file type
        _, ext = os.path.splitext(filepath)
        mime_type, _ = mimetypes.guess_type(filepath)
        
        return {
            'size_bytes': size,
            'size_readable': format_size(size),
            'modified': modified,
            'extension': ext.lower(),
            'mime_type': mime_type or 'unknown'
        }
    except Exception as e:
        return {
            'error': str(e)
        }

def format_size(bytes):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} TB"

def scan_directory(root_path):
    """Recursively scan directory and collect file information."""
    data_structure = {}
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Skip hidden directories and __pycache__
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
        
        rel_path = os.path.relpath(dirpath, root_path)
        if rel_path == '.':
            rel_path = ''
        
        if filenames:
            data_structure[rel_path] = []
            for filename in filenames:
                # Skip hidden files and temporary files
                if filename.startswith('.') or filename.startswith('~'):
                    continue
                    
                filepath = os.path.join(dirpath, filename)
                file_info = {
                    'name': filename,
                    'path': os.path.relpath(filepath, root_path),
                    **get_file_info(filepath)
                }
                data_structure[rel_path].append(file_info)
    
    return data_structure

def analyze_data_types(data_structure):
    """Analyze the types of data files found."""
    file_types = {}
    total_files = 0
    total_size = 0
    
    for directory, files in data_structure.items():
        for file in files:
            if 'extension' in file:
                ext = file['extension']
                if ext not in file_types:
                    file_types[ext] = {'count': 0, 'total_size': 0, 'examples': []}
                file_types[ext]['count'] += 1
                if 'size_bytes' in file:
                    file_types[ext]['total_size'] += file['size_bytes']
                    total_size += file['size_bytes']
                if len(file_types[ext]['examples']) < 3:
                    file_types[ext]['examples'].append(file['name'])
                total_files += 1
    
    return {
        'total_files': total_files,
        'total_size': format_size(total_size),
        'file_types': file_types
    }

def identify_data_content(filename, filepath=None):
    """Try to identify the content of a data file based on its name and path."""
    filename_lower = filename.lower()
    
    # Check for specific data types
    if 'twin2sim' in filename_lower:
        return "Twin2Sim simulation data"
    elif 'monitoring' in filename_lower or 'monitor' in filename_lower:
        return "Monitoring/sensor data"
    elif 'erzeugung' in filename_lower:
        return "Energy generation data"
    elif 'verbrauch' in filename_lower:
        return "Energy consumption data"
    elif 'wetter' in filename_lower or 'weather' in filename_lower:
        return "Weather data"
    elif 'temperatur' in filename_lower or 'temp' in filename_lower:
        return "Temperature measurements"
    elif filename.endswith('.csv'):
        return "Structured data (CSV)"
    elif filename.endswith('.json'):
        return "JSON data"
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        return "Excel spreadsheet data"
    elif filename.endswith('.parquet'):
        return "Parquet columnar data"
    elif filename.endswith('.h5') or filename.endswith('.hdf5'):
        return "HDF5 scientific data"
    elif filename.endswith('.txt'):
        return "Text data"
    elif filename.endswith('.pkl') or filename.endswith('.pickle'):
        return "Python pickled data"
    else:
        return "Data file"

def main():
    """Main execution function."""
    daten_path = Path('/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025/Daten')
    
    if not daten_path.exists():
        print(f"Error: Daten directory not found at {daten_path}")
        return
    
    print(f"Scanning directory: {daten_path}")
    print("=" * 60)
    
    # Scan the directory
    data_structure = scan_directory(daten_path)
    
    # Analyze file types
    analysis = analyze_data_types(data_structure)
    
    print(f"\n📊 Summary Statistics:")
    print(f"Total files: {analysis['total_files']}")
    print(f"Total size: {analysis['total_size']}")
    print()
    
    print("📁 Directory Structure:")
    print("-" * 40)
    
    # Sort directories for better readability
    sorted_dirs = sorted(data_structure.keys())
    
    for directory in sorted_dirs:
        files = data_structure[directory]
        if files:
            if directory:
                print(f"\n📂 {directory}/")
            else:
                print(f"\n📂 [Root]")
            
            # Sort files by name
            files.sort(key=lambda x: x['name'])
            
            for file in files[:10]:  # Show first 10 files per directory
                content_desc = identify_data_content(file['name'])
                size_str = file.get('size_readable', 'N/A')
                print(f"  📄 {file['name']} ({size_str}) - {content_desc}")
            
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more files")
    
    print("\n" + "=" * 60)
    print("📈 File Type Distribution:")
    for ext, info in sorted(analysis['file_types'].items(), key=lambda x: x[1]['count'], reverse=True):
        total_size = format_size(info['total_size'])
        print(f"  {ext or 'no extension'}: {info['count']} files ({total_size})")
        if info['examples']:
            print(f"    Examples: {', '.join(info['examples'][:3])}")
    
    # Save detailed structure to JSON for documentation generation
    output_file = Path('/mnt/c/Users/admin/OneDrive - Fachhochschule Salzburg GmbH/MokiG/OneDrive_1_18.8.2025/data_structure.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'scan_date': datetime.now().isoformat(),
            'root_path': str(daten_path),
            'structure': data_structure,
            'analysis': analysis
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Detailed structure saved to: {output_file}")

if __name__ == "__main__":
    main()