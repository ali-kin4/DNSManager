# DNS Manager Pro

A beautiful, modern Windows application for managing DNS settings with ease. No more navigating through Windows Control Panel!

## Features

- **Quick DNS Switching**: Change DNS servers instantly with a single click
- **Save Configurations**: Save your favorite DNS settings with custom names
- **Popular DNS Presets**: Quick access to Cloudflare, Google, OpenDNS, Quad9, and more
- **Gaming Server Ping Tests**: Test latency to Fortnite, Epic Games, COD, EA, Battlefield, Steam, Valorant, and more
- **Network Adapter Selection**: Manage DNS for multiple network adapters
- **Modern UI**: Beautiful dark/light theme with an intuitive interface
- **Auto-save**: All your configurations are automatically saved
- **DHCP Reset**: Easily reset to automatic DNS settings

## Screenshots

The app features:
- Clean, modern interface with dark/light mode
- Real-time DNS configuration display
- One-click DNS preset loading
- Live ping testing with color-coded latency
- Easy configuration management

## Installation

### Prerequisites
- Windows OS (Windows 10/11 recommended)
- Python 3.8 or higher

### Setup Steps

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application with administrator privileges (required for DNS changes):
   - **Option 1**: Double-click `run_as_admin.bat`
   - **Option 2**: Run manually:
     ```bash
     python dns_manager.py
     ```
     (Right-click Command Prompt → "Run as Administrator")

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

## Gaming Servers Tested

- Fortnite (NA-East & EU)
- Epic Games
- Call of Duty / Activision
- EA / Battlefield
- Steam
- Riot Games / Valorant / League of Legends
- Battle.net (Blizzard)
- Ubisoft
- Apex Legends

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

## System Requirements

- Windows 10/11 (may work on Windows 7/8 but not tested)
- Python 3.8+
- Administrator privileges
- Active internet connection

## License

Free to use for personal and commercial purposes.

## Credits

Built with:
- Python
- CustomTkinter (Modern UI framework)
- Windows netsh commands

---

**Note**: Always be cautious when changing DNS settings. Keep a backup of your working DNS configuration. If you experience internet issues after changing DNS, simply click "Reset to DHCP" to restore automatic settings.
