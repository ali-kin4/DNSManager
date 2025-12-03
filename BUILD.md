# Building DNS Manager Pro

This guide explains how to build DNS Manager Pro from source and create distribution packages.

## Prerequisites

### Required Software
1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **PyInstaller** - Installed automatically by build script
3. **Inno Setup** (Optional, for installer) - [Download](https://jrsoftware.org/isdl.php)

### Python Dependencies
```bash
pip install -r requirements.txt
```

## Quick Build (Windows)

Simply run the build script:
```bash
build.bat
```

This will:
1. Install all dependencies
2. Build the standalone executable
3. Create a Windows installer (if Inno Setup is installed)

## Manual Build Process

### Step 1: Build Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build with PyInstaller
pyinstaller dns_manager.spec --clean
```

Output: `dist\DNSManagerPro.exe`

### Step 2: Create Installer (Optional)

If you have Inno Setup installed:

```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

Output: `dist\installer\DNSManagerPro-Setup-v2.0.0.exe`

## Build Output

After a successful build:

```
dist/
├── DNSManagerPro.exe          # Standalone executable
└── installer/
    └── DNSManagerPro-Setup-v2.0.0.exe  # Windows installer
```

## Distribution

### For End Users (Recommended)
Distribute the installer: `DNSManagerPro-Setup-v2.0.0.exe`
- Professional installation experience
- Automatic shortcuts
- Clean uninstallation
- Updates preserved configs

### For Portable Use
Distribute just: `DNSManagerPro.exe`
- No installation needed
- Run from any location
- Requires admin rights when changing DNS

## Creating a GitHub Release

1. Build the project using `build.bat`
2. Create a new release on GitHub
3. Upload these files:
   - `dist\installer\DNSManagerPro-Setup-v2.0.0.exe` (Primary)
   - `dist\DNSManagerPro.exe` (Portable version)
4. Tag format: `v2.0.0`

The app will automatically detect new releases and offer to update!

## Development Build

For testing during development:

```bash
# Run directly with Python
python dns_manager.py
```

## Troubleshooting

### PyInstaller Build Issues

**Problem:** Module not found errors
```bash
# Solution: Add to hiddenimports in dns_manager.spec
hiddenimports=['missing_module_name']
```

**Problem:** File not found at runtime
```bash
# Solution: Add to datas in dns_manager.spec
datas=[('your_file.txt', '.')],
```

### Inno Setup Issues

**Problem:** Installer build fails
- Ensure Inno Setup 6 is installed
- Check path in build.bat matches your installation
- Verify all source files exist

### Runtime Issues

**Problem:** App won't start
- Check Windows Event Viewer for errors
- Run from command line to see error messages
- Ensure all dependencies are bundled

## Advanced Configuration

### Custom Icon
Replace `logo.ico` with your own icon (must be .ico format, 256x256 recommended)

### Version Update
Edit `version.py`:
```python
__version__ = "2.1.0"
```

Then rebuild.

### Excluding Modules
To reduce size, add to `excludes` in `dns_manager.spec`:
```python
excludes=['unused_module'],
```

## Build Size Optimization

Current build size: ~60-80 MB

To reduce:
1. Use UPX compression (already enabled)
2. Exclude unnecessary modules
3. Consider using `--onefile` mode (slower startup)

## Continuous Integration

For automated builds, see `.github/workflows/build.yml` (if available)

## Support

Issues with building? [Open an issue](https://github.com/ali-kin4/DNSManager/issues)
