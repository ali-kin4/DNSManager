# Distribution Guide - DNS Manager Pro

Professional distribution setup for Windows users.

## For End Users

### Installation

**Option 1: Windows Installer (Recommended)**
1. Download `DNSManagerPro-Setup-v2.0.0.exe` from [Releases](https://github.com/ali-kin4/DNSManager/releases)
2. Run the installer
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

**Features:**
- ✅ Automatic updates
- ✅ Desktop & Start Menu shortcuts
- ✅ Clean uninstallation
- ✅ Preserves your DNS configurations
- ✅ Requires admin rights (for DNS changes)

**Option 2: Portable Executable**
1. Download `DNSManagerPro.exe` from [Releases](https://github.com/ali-kin4/DNSManager/releases)
2. Run directly - no installation needed
3. Must run as Administrator

### System Requirements
- **OS:** Windows 10/11 (64-bit)
- **RAM:** 100 MB
- **Disk:** 150 MB
- **Network:** Required for updates and ping tests
- **Permissions:** Administrator rights required

### First Launch
1. Right-click `DNSManagerPro.exe` → **Run as Administrator**
2. Grant administrator permissions (required for DNS changes)
3. Select your network adapter
4. Start managing DNS!

## For Developers

### Building for Distribution

#### Prerequisites
```bash
pip install pyinstaller
# Optional: Download Inno Setup from https://jrsoftware.org/isdl.php
```

#### Build Commands

**Quick Build:**
```bash
build.bat
```

**Manual Build:**
```bash
# 1. Build executable
pyinstaller dns_manager.spec --clean

# 2. Build installer (if Inno Setup installed)
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

### Creating a Release

1. **Update Version**
   ```python
   # version.py
   __version__ = "2.1.0"
   ```

2. **Build Artifacts**
   ```bash
   build.bat
   ```

3. **Create GitHub Release**
   - Tag: `v2.1.0`
   - Title: `DNS Manager Pro v2.1.0`
   - Upload:
     - `DNSManagerPro-Setup-v2.1.0.exe` (Primary)
     - `DNSManagerPro.exe` (Portable)
     - Source code (automatic)

4. **Write Release Notes**
   ```markdown
   ## What's New
   - Feature 1
   - Feature 2
   - Bug fix 1

   ## Installation
   Download and run `DNSManagerPro-Setup-v2.1.0.exe`

   ## Portable Version
   Download `DNSManagerPro.exe` for portable use
   ```

### Auto-Update System

The app automatically checks for updates on startup using GitHub Releases API.

**Update Flow:**
1. App checks GitHub API on startup
2. Compares versions
3. Shows update notification if available
4. User can install with one click
5. App downloads and installs update
6. Restarts automatically

**Update Mechanisms:**
- **Installed version:** Downloads and runs new installer
- **Git repository:** Offers `git pull` option
- **Portable version:** Downloads and extracts new version

### Code Signing (Recommended)

For production releases, sign your executables:

```bash
# Using signtool (Windows SDK)
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com DNSManagerPro.exe
```

**Benefits:**
- Removes Windows SmartScreen warnings
- Increases user trust
- Professional appearance

**Get a Certificate:**
- [DigiCert](https://www.digicert.com/code-signing/)
- [Sectigo](https://sectigo.com/ssl-certificates-tls/code-signing)
- [SSL.com](https://www.ssl.com/certificates/code-signing/)

### Distribution Channels

**Primary:**
- GitHub Releases (automatic updates)

**Optional:**
- Microsoft Store
- Chocolatey package manager
- Winget repository
- Your own website

### Version Numbering

Follow Semantic Versioning:
- **Major.Minor.Patch** (e.g., 2.1.0)
- **Major:** Breaking changes
- **Minor:** New features
- **Patch:** Bug fixes

### Testing Checklist

Before release:
- [ ] Build completes without errors
- [ ] Executable runs on clean Windows system
- [ ] Installer works correctly
- [ ] Uninstaller preserves configs (optional)
- [ ] Auto-update detects and installs correctly
- [ ] All features work in compiled version
- [ ] Admin elevation prompt appears
- [ ] Icon displays correctly
- [ ] About dialog shows correct version

### File Sizes

Approximate sizes:
- **Executable:** 60-80 MB
- **Installer:** 65-85 MB
- **Source ZIP:** 1-2 MB

### Troubleshooting

**Antivirus False Positives:**
- Submit to antivirus vendors for whitelisting
- Code signing reduces false positives

**Windows SmartScreen:**
- Code signing eliminates warnings
- Without signing: Users must click "More info" → "Run anyway"

**Large File Size:**
- Python executables are large
- Consider using `--onefile` mode (slower startup)
- Exclude unnecessary modules in spec file

## Support

Questions? [Open an issue](https://github.com/ali-kin4/DNSManager/issues)
