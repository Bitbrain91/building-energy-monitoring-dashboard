@echo off
REM ============================================================================
REM MokiG Dashboard - Windows Starter
REM ============================================================================
REM Dieses Script startet das optimierte Dashboard auf Windows
REM ============================================================================

echo.
echo ============================================================
echo MokiG Dashboard - Performance Optimiert
echo ============================================================
echo.

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FEHLER] Python ist nicht installiert oder nicht im PATH!
    echo Bitte installieren Sie Python 3.8 oder höher von python.org
    pause
    exit /b 1
)

REM Prüfe ob Virtual Environment existiert
if not exist "venv_windows" (
    echo [INFO] Erstelle Virtual Environment...
    python -m venv venv_windows
    
    echo [INFO] Aktiviere Virtual Environment...
    call venv_windows\Scripts\activate.bat
    
    echo [INFO] Installiere Abhängigkeiten...
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo [INFO] Aktiviere Virtual Environment...
    call venv_windows\Scripts\activate.bat
    
    REM Prüfe ob alle Module installiert sind
    python -c "import pyarrow, pandas, dash, plotly" >nul 2>&1
    if %errorlevel% neq 0 (
        echo [INFO] Installiere fehlende Module...
        pip install --upgrade pip
        pip install pyarrow pandas numpy dash plotly dash-bootstrap-components openpyxl xlrd lz4 psutil
    )
)

REM Prüfe ob Parquet-Dateien existieren
if not exist "data_optimized\*.parquet" (
    echo.
    echo ============================================================
    echo ACHTUNG: Keine optimierten Daten gefunden!
    echo ============================================================
    echo.
    echo Möchten Sie die Daten jetzt optimieren? (J/N)
    set /p optimize=
    
    if /i "%optimize%"=="J" (
        echo [INFO] Starte Datenoptimierung...
        python src\preprocess_data.py --source all
        echo.
        echo [OK] Datenoptimierung abgeschlossen!
        echo.
    )
)

REM Starte Dashboard
echo.
echo ============================================================
echo Starte Dashboard...
echo ============================================================
echo.
echo Dashboard läuft unter: http://127.0.0.1:8050
echo Drücken Sie Ctrl+C zum Beenden
echo.

python src\dashboard_optimized.py

REM Nach Beendigung
echo.
echo Dashboard wurde beendet.
pause