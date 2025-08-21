@echo off
echo ============================================================
echo         MokiG Dashboard - Optimierte Version
echo ============================================================
echo.

REM Aktiviere venv wenn vorhanden
if exist "venv\Scripts\activate.bat" (
    echo Aktiviere virtuelle Umgebung...
    call venv\Scripts\activate.bat
)

REM Starte Dashboard
echo Starte Dashboard...
python start_dashboard.py

REM Pause am Ende
pause