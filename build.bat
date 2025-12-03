@echo off
REM Build script for DNS Manager Pro
REM This script builds the executable and creates the installer

echo ========================================
echo    DNS Manager Pro - Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [INFO] PyInstaller not found. Installing...
    pip install pyinstaller
)

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Building executable with PyInstaller...
pyinstaller dns_manager.spec --clean --noconfirm
if errorlevel 1 (
    echo [ERROR] PyInstaller build failed
    pause
    exit /b 1
)

echo.
echo [3/4] Checking if Inno Setup is installed...
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist "%INNO_PATH%" (
    echo [INFO] Building Windows installer...
    "%INNO_PATH%" installer.iss
    if errorlevel 1 (
        echo [WARNING] Installer build failed, but executable is ready
    ) else (
        echo [SUCCESS] Installer created successfully!
    )
) else (
    echo [WARNING] Inno Setup not found at: %INNO_PATH%
    echo [INFO] Download from: https://jrsoftware.org/isdl.php
    echo [INFO] You can still use the executable in dist\DNSManagerPro.exe
)

echo.
echo [4/4] Build complete!
echo.
echo Output files:
echo   - Executable: dist\DNSManagerPro.exe
if exist "dist\installer\DNSManagerPro-Setup-*.exe" (
    echo   - Installer: dist\installer\DNSManagerPro-Setup-*.exe
)
echo.
echo ========================================
pause
