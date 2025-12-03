# DNS Manager Pro

A beautiful, professional Windows application for managing DNS settings with ease. Built like famous apps with auto-updates, installers, and a modern UI!

## ✨ Features

### Core Features
- 🚀 **Quick DNS Switching**: Change DNS servers instantly with a single click
- 💾 **Save Configurations**: Save your favorite DNS settings with custom names
- 📋 **Popular DNS Presets**: Quick access to Cloudflare, Google, OpenDNS, Quad9, and more
- 🎮 **Gaming Server Ping Tests**: Test latency to Fortnite, Epic Games, COD, EA, Battlefield, Steam, Valorant, and more
- 🔌 **Network Adapter Selection**: Manage DNS for multiple network adapters
- 🎨 **Modern UI**: Beautiful dark/light/system theme with an intuitive interface
- 💿 **Auto-save**: All your configurations are automatically saved
- ↩️ **DHCP Reset**: Easily reset to automatic DNS settings

### Professional Features
- 🔄 **Auto-Update System**: Automatically checks for updates and installs them with one click
- ⚡ **DNS Benchmarking**: Test all your saved DNS configs against multiple services to find the fastest
- 🎯 **Active Config Highlighting**: See which DNS config is currently active (moves to top with green highlight)
- 📊 **Performance Optimized**: Cached DNS queries for faster performance
- 🎨 **System Theme Support**: Auto-detects Windows theme preference
- 📂 **Import/Export Configs**: Share DNS configurations with others
- 🔧 **Network Diagnostics**: Built-in network diagnostics tool
- 📱 **Professional Installer**: Windows installer with automatic shortcuts and clean uninstallation

## Screenshots

The app features:
- Clean, modern interface with dark/light mode
- Real-time DNS configuration display
- One-click DNS preset loading
- Live ping testing with color-coded latency
- Easy configuration management

## 📥 Installation

### For Regular Users (Recommended)

**Windows Installer:**
1. Download `DNSManagerPro-Setup-v2.0.0.exe` from [Releases](https://github.com/ali-kin4/DNSManager/releases)
2. Run the installer
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

**Portable Version:**
1. Download `DNSManagerPro.exe` from [Releases](https://github.com/ali-kin4/DNSManager/releases)
2. Run directly (no installation needed)
3. Must run as Administrator

### For Developers

**Prerequisites:**
- Windows 10/11
- Python 3.8 or higher

**Setup Steps:**

1. Clone this repository:
```bash
git clone https://github.com/ali-kin4/DNSManager.git
cd DNSManager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python dns_manager.py
```
*(Must run as Administrator)*

**Building from Source:**
```bash
# Build executable and installer
build.bat

# Or create a release
release.bat
```

See [BUILD.md](BUILD.md) for detailed build instructions.

## Usage

### Setting DNS

1. **Select Network Adapter**: Choose your active network adapter from the dropdown
2. **Enter DNS Servers**:
   - Type primary DNS (required)
   - Type secondary DNS (optional)
3. **Apply**: Click "Apply DNS" button

### Using Presets

Click any preset button (Cloudflare, Google, etc.) to auto-fill the DNS fields, then click "Apply DNS"

### Quick Apply from Saved Configs

1. Enter DNS servers in the input fields
2. Give it a custom name (e.g., "Gaming DNS", "Work DNS")
3. Click "Save"
4. Later, click "Apply" next to any saved config for instant switching!

### Testing Gaming Servers

- Click any game/platform name to test ping
- Click "Test All" to test all servers at once
- Results show latency in milliseconds:
  - 🟢 Green: < 50ms (Excellent)
  - 🟠 Orange: 50-100ms (Good)
  - 🔴 Red: > 100ms (High latency)

### Reset to Automatic

Click "Reset to DHCP" to revert to automatic DNS settings from your router

### DNS Benchmarking

**Find the fastest DNS for your location:**

1. Go to **Tools → Benchmark All DNS**
2. Select services you want to test against:
   - Use quick filters: Gaming, AI Platforms, Select All
   - Or manually select individual services
3. Click **Start Benchmark**
4. View ranked results with average latency
5. Apply the fastest config!

**Results show:**
- 🥇 #1 (Green) - Fastest
- 🥈 #2 (Orange) - Second
- 🥉 #3 (Red) - Third
- Average latency across all services
- Success rate per config

### Auto-Updates

**Stay up to date automatically:**

- App checks for updates on startup
- Notification appears when new version is available
- One-click update installation
- Automatic restart after update

**Manual update check:**
- Go to **Help → Check for Updates**

**Update methods:**
- **Installed version:** Downloads and runs new installer
- **Git repository:** Offers `git pull` option
- **Portable:** Downloads and extracts new version

### Theme Selection

Choose your preferred theme:
- **System:** Auto-detects Windows theme (default)
- **Dark:** Always dark mode
- **Light:** Always light mode

**Change theme:**
- Use the segmented button in top-right
- Or go to **View → [Theme Name]**

## Popular DNS Providers

The app includes these preset DNS providers:

- **Cloudflare**: 1.1.1.1 (Fast & Private)
- **Cloudflare Family**: 1.1.1.3 (Blocks malware & adult content)
- **Google**: 8.8.8.8 (Reliable & Fast)
- **OpenDNS**: 208.67.222.222 (Security & filtering)
- **Quad9**: 9.9.9.9 (Security focused)
- **AdGuard**: 94.140.14.14 (Ad blocking)
- **Comodo Secure**: 8.26.56.26 (Security)
- **CleanBrowsing**: 185.228.168.9 (Family filter)
- **Alternate DNS**: 76.76.19.19 (Ad blocking)

## Services Available for Testing

### Gaming Servers
- Fortnite (NA-East & EU)
- Epic Games
- Call of Duty / Activision
- EA / Battlefield
- Steam
- Riot Games / Valorant / League of Legends
- Battle.net (Blizzard)
- Ubisoft
- Apex Legends

### AI Platforms
- ChatGPT (OpenAI)
- Gemini (Google)
- Claude (Anthropic)
- Perplexity AI

### Other Services
- YouTube
- Cloudflare DNS
- Google DNS

## Configuration File

Your saved DNS configurations are stored in `dns_configs.json` in the application directory. This file is automatically created and updated when you save configurations.

## Troubleshooting

### "Administrator rights required" warning
- You must run the application as Administrator to change DNS settings
- Use the provided `run_as_admin.bat` file
- Or right-click Python/Command Prompt and select "Run as Administrator"

### DNS changes not applying
- Ensure you selected the correct network adapter
- Check if you have admin privileges
- Try flushing DNS cache manually: `ipconfig /flushdns`

### Ping tests showing "Timeout"
- Server might be blocking ICMP packets
- Check your internet connection
- Some gaming servers don't respond to ping

### No network adapters showing
- Click the refresh button (🔄)
- Check your network connections in Windows settings

## Tips

- **For Gaming**: Try Cloudflare (1.1.1.1) or Google (8.8.8.8) for low latency
- **For Privacy**: Use Cloudflare (1.1.1.1) or Quad9 (9.9.9.9)
- **For Ad Blocking**: Use AdGuard or Alternate DNS
- **For Families**: Use Cloudflare Family or CleanBrowsing
- **Test Before Switching**: Use ping tests to check if a DNS server is fast for you

## 💻 System Requirements

**For Users (Installer/Portable):**
- Windows 10/11 (64-bit)
- 100 MB RAM
- 150 MB Disk Space
- Administrator privileges
- Internet connection (for updates and testing)

**For Developers:**
- Windows 10/11
- Python 3.8+
- Administrator privileges

## 🏗️ Building

See [BUILD.md](BUILD.md) for comprehensive build instructions.

**Quick build:**
```bash
build.bat
```

**Create release:**
```bash
release.bat
```

## 👨‍💻 About the Creator

**DNS Manager Pro** is created and maintained by **Ali Jabbary**

- 🌐 **Website:** [alijabbary.com](https://alijabbary.com)
- 💻 **GitHub:** [@ali-kin4](https://github.com/ali-kin4)
- 📧 **Support:** [GitHub Issues](https://github.com/ali-kin4/DNSManager/issues)

Connect with me for more projects and updates!

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

Free to use for personal and commercial purposes.

Copyright (c) 2025 Ali Jabbary

## 🙏 Credits

**Created by:** [Ali Jabbary](https://alijabbary.com) • [GitHub](https://github.com/ali-kin4)

Built with:
- **Python** - Programming language
- **CustomTkinter** - Modern UI framework
- **Pillow** - Image processing
- **darkdetect** - System theme detection
- **PyInstaller** - Executable builder
- **Inno Setup** - Windows installer

Special thanks to all DNS providers for their free services!

## 📚 Documentation

- [BUILD.md](BUILD.md) - Building from source
- [DISTRIBUTION.md](DISTRIBUTION.md) - Distribution guide
- [GitHub Issues](https://github.com/ali-kin4/DNSManager/issues) - Bug reports & features

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## ⚠️ Important Notes

- **Administrator Required:** DNS changes require admin privileges
- **Backup Configs:** Your configs are saved, but keep backups
- **Safe Reset:** Use "Reset to DHCP" if you have connection issues
- **Test First:** Use ping tests before switching DNS permanently
- **Auto-Updates:** Keep the app updated for latest features and fixes

---

**Made with ❤️ for the community**

[⭐ Star this repo](https://github.com/ali-kin4/DNSManager) | [📥 Download Latest Release](https://github.com/ali-kin4/DNSManager/releases) | [🐛 Report Issues](https://github.com/ali-kin4/DNSManager/issues)
