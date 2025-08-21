#!/usr/bin/env python
"""
MokiG Dashboard - Hauptstartskript
==================================
Startet das optimierte Dashboard mit allen Verbesserungen.
"""

import os
import sys
from pathlib import Path
import subprocess
import webbrowser
import threading
import time

# Füge src zum Python-Pfad hinzu
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def check_dependencies():
    """Überprüft ob alle notwendigen Pakete installiert sind"""
    required_packages = [
        'dash',
        'dash-bootstrap-components',
        'plotly',
        'pandas',
        'numpy',
        'openpyxl'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("\n⚠️  Fehlende Pakete gefunden:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nInstalliere fehlende Pakete...")
        
        # Aktiviere venv wenn vorhanden
        venv_path = Path(__file__).parent / "venv"
        if venv_path.exists():
            if sys.platform == "win32":
                pip_cmd = str(venv_path / "Scripts" / "pip")
            else:
                pip_cmd = str(venv_path / "bin" / "pip")
        else:
            pip_cmd = "pip"
        
        for pkg in missing:
            print(f"Installiere {pkg}...")
            subprocess.run([pip_cmd, "install", pkg], check=False)
        
        print("\n✅ Alle Pakete installiert!")
        return True
    return False


def open_browser():
    """Öffnet den Browser nach kurzer Verzögerung"""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:8050')


def main():
    """Hauptfunktion zum Starten des Dashboards"""
    print("\n" + "="*60)
    print("🚀 MokiG Dashboard - Optimierte Version")
    print("="*60)
    
    # Prüfe Abhängigkeiten
    print("\n📦 Überprüfe Abhängigkeiten...")
    check_dependencies()
    
    # Importiere Dashboard
    try:
        from dashboard_main import app
    except ImportError as e:
        print(f"\n❌ Fehler beim Import des Dashboards: {e}")
        print("Stelle sicher, dass dashboard_main.py im src/ Ordner vorhanden ist.")
        sys.exit(1)
    
    # Starte Browser in separatem Thread
    print("\n🌐 Öffne Browser...")
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Starte Dashboard
    print("\n" + "="*60)
    print("✅ Dashboard läuft auf http://127.0.0.1:8050")
    print("   Drücke Ctrl+C zum Beenden")
    print("="*60 + "\n")
    
    try:
        app.run(
            debug=False,  # Produktionsmodus
            host='127.0.0.1',
            port=8050,
            use_reloader=False  # Verhindert doppelten Start
        )
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard beendet.")
    except Exception as e:
        print(f"\n❌ Fehler beim Starten: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()