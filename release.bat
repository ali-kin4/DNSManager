@echo off
REM Release script for DNS Manager Pro
REM This script automates the release process

echo ========================================
echo   DNS Manager Pro - Release Script
echo ========================================
echo.

REM Get version from version.py
for /f "tokens=3 delims== " %%a in ('findstr "__version__" version.py') do set VERSION=%%a
set VERSION=%VERSION:"=%
echo Current version: %VERSION%
echo.

echo This script will:
echo   1. Run tests (if available)
echo   2. Build the application
echo   3. Create distribution packages
echo   4. Prepare release artifacts
echo.
pause

echo.
echo [1/5] Running tests...
if exist tests (
    python -m pytest tests/
    if errorlevel 1 (
        echo [ERROR] Tests failed! Fix issues before releasing.
        pause
        exit /b 1
    )
) else (
    echo [INFO] No tests found, skipping...
)

echo.
echo [2/5] Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec~ del *.spec~
echo [SUCCESS] Cleaned build directories

echo.
echo [3/5] Building application...
call build.bat
if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo [4/5] Creating release directory...
set RELEASE_DIR=release\v%VERSION%
if exist release\v%VERSION% rmdir /s /q release\v%VERSION%
mkdir "%RELEASE_DIR%"

echo Copying artifacts...
if exist "dist\DNSManagerPro.exe" (
    copy "dist\DNSManagerPro.exe" "%RELEASE_DIR%\DNSManagerPro-v%VERSION%-Portable.exe"
    echo   - Portable executable: OK
) else (
    echo   - Portable executable: MISSING!
)

if exist "dist\installer\DNSManagerPro-Setup-v%VERSION%.exe" (
    copy "dist\installer\DNSManagerPro-Setup-v%VERSION%.exe" "%RELEASE_DIR%\"
    echo   - Installer: OK
) else (
    echo   - Installer: NOT FOUND (Inno Setup may not be installed)
)

REM Copy documentation
copy README.md "%RELEASE_DIR%\"
copy LICENSE "%RELEASE_DIR%\"
copy BUILD.md "%RELEASE_DIR%\"
copy DISTRIBUTION.md "%RELEASE_DIR%\"

echo.
echo [5/5] Creating checksums...
cd "%RELEASE_DIR%"
certutil -hashfile "DNSManagerPro-v%VERSION%-Portable.exe" SHA256 > checksums.txt
if exist "DNSManagerPro-Setup-v%VERSION%.exe" (
    certutil -hashfile "DNSManagerPro-Setup-v%VERSION%.exe" SHA256 >> checksums.txt
)
cd ..\..

echo.
echo ========================================
echo         RELEASE READY!
echo ========================================
echo.
echo Version: %VERSION%
echo Location: %RELEASE_DIR%
echo.
echo Files ready for release:
dir "%RELEASE_DIR%" /b
echo.
echo Next steps:
echo   1. Test the executables on a clean Windows system
echo   2. Create a new release on GitHub: https://github.com/ali-kin4/DNSManager/releases/new
echo   3. Tag: v%VERSION%
echo   4. Upload files from: %RELEASE_DIR%
echo   5. Write release notes describing changes
echo.
echo Release notes template:
echo ----------------------------------------
echo ## What's New in v%VERSION%
echo.
echo ### Features
echo - New feature 1
echo - New feature 2
echo.
echo ### Improvements
echo - Improvement 1
echo - Improvement 2
echo.
echo ### Bug Fixes
echo - Fix 1
echo - Fix 2
echo.
echo ### Installation
echo Download and run `DNSManagerPro-Setup-v%VERSION%.exe`
echo.
echo ### Portable Version
echo Download `DNSManagerPro-v%VERSION%-Portable.exe` for portable use
echo ----------------------------------------
echo.
pause

REM Open release folder
start "" "%RELEASE_DIR%"
