# Quick Start Guide

## Installation (30 seconds)

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Done!** You're ready to use DNS Manager Pro.

## Running the App

### Method 1: Double-Click (Easiest)
Simply double-click `run_as_admin.bat`

### Method 2: Command Line
```bash
python dns_manager.py
```
(Run Command Prompt as Administrator)

## First-Time Setup (1 minute)

1. **Select Your Network Adapter**
   - Open the app
   - The dropdown at the top shows your network adapters
   - Select your active adapter (usually "Wi-Fi" or "Ethernet")

2. **View Current DNS**
   - Your current DNS settings are displayed below the adapter selector

## Common Tasks

### Change DNS to Cloudflare (10 seconds)
1. Click "Cloudflare (1.1.1.1)" in the Popular DNS Providers section
2. Click "Apply DNS"
3. Done!

### Save Your Favorite DNS (15 seconds)
1. Enter primary DNS: `1.1.1.1`
2. Enter secondary DNS: `1.0.0.1`
3. Type a name in "Configuration name": `My Gaming DNS`
4. Click "💾 Save"
5. Done! It's saved forever.

### Use Saved DNS Later (5 seconds)
1. Find your saved config in "Saved Configurations"
2. Click "Apply" next to it
3. Done!

### Test Gaming Server Ping (5 seconds)
1. Click on any game/platform name (e.g., "Fortnite (NA-East)")
2. Wait 2-3 seconds
3. See the latency in milliseconds
   - Green = Great
   - Orange = Good
   - Red = High latency

### Test All Servers (10 seconds)
1. Click "Test All" button
2. Wait a few seconds
3. See all latencies at once

### Reset to Automatic DNS (5 seconds)
1. Click "Reset to DHCP"
2. Done! Back to automatic.

## Tips for Best Results

### For Gaming
- Try Cloudflare (1.1.1.1) or Google (8.8.8.8)
- Use ping tests to find the fastest for your location
- Lower ping = better gaming experience

### For Privacy
- Use Cloudflare (1.1.1.1) - doesn't log your browsing
- Or use Quad9 (9.9.9.9) - blocks malicious sites

### For Families
- Use Cloudflare Family (1.1.1.3) - blocks adult content
- Or CleanBrowsing (185.228.168.9) - family filter

### For Ad Blocking
- Use AdGuard (94.140.14.14)
- Or Alternate DNS (76.76.19.19)

## Troubleshooting (1 minute fixes)

### "Administrator rights required" warning
**Fix**: Right-click `run_as_admin.bat` → "Run as administrator"

### DNS not changing
**Fix**: Make sure you're running as Administrator (see above)

### No internet after changing DNS
**Fix**: Click "Reset to DHCP" - this restores automatic settings

### No network adapters showing
**Fix**: Click the 🔄 refresh button next to the adapter dropdown

### Ping showing "Timeout"
This is normal for some servers - they block ping requests

## Keyboard Shortcuts

- **Tab**: Navigate between fields
- **Enter**: Apply DNS (when in DNS input fields)
- **Escape**: Close dialogs

## What You See

### Main Window Sections

**Left Side:**
- Network adapter selector
- Current DNS display
- DNS input fields (Primary/Secondary)
- Apply & Reset buttons
- Popular DNS presets (click to load)

**Right Side:**
- Save configuration box
- Saved configurations (your custom DNS sets)
- Gaming server ping tests

### Button Colors

- **Green buttons**: Apply/Confirm actions
- **Red buttons**: Delete/Reset actions
- **Blue buttons**: Load/Select actions
- **Gray buttons**: Neutral actions

### Ping Test Colors

- **Green text**: Excellent latency (< 50ms)
- **Orange text**: Good latency (50-100ms)
- **Red text**: High latency (> 100ms)

## Example Workflows

### Scenario 1: Switching DNS for Gaming

1. Open DNS Manager Pro
2. Click "Test All" to see current latencies
3. Click "Cloudflare" preset (usually fastest)
4. Click "Apply DNS"
5. Start gaming!

**Time**: 15 seconds

### Scenario 2: Work from Home Setup

1. Set work DNS (e.g., company DNS or Google)
2. Name it "Work DNS"
3. Click Save
4. Set home DNS (e.g., Cloudflare)
5. Name it "Home DNS"
6. Click Save

Now you can switch instantly:
- Going to work? Click "Apply" on "Work DNS"
- Back home? Click "Apply" on "Home DNS"

**Time**: 1 minute setup, 3 seconds to switch forever

### Scenario 3: Finding Best DNS for Your Location

1. Click "Test All"
2. Wait for all results
3. Note which DNS has green (lowest ping)
4. Click that DNS preset
5. Click "Apply DNS"
6. Enjoy faster internet!

**Time**: 30 seconds

## Safety Notes

- **Always safe to reset**: If anything goes wrong, click "Reset to DHCP"
- **No permanent changes**: DNS changes are easily reversible
- **Your data is local**: All saved configs are stored locally in `dns_configs.json`
- **No internet required**: The app works offline (except ping tests)

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [FEATURES.md](FEATURES.md) for complete feature list
- Save your favorite DNS configurations
- Test different DNS servers to find the best for you

## Support

If you encounter issues:
1. Check this Quick Start guide
2. Read the Troubleshooting section
3. Make sure you're running as Administrator
4. Try "Reset to DHCP" to restore defaults

---

**You're all set! Enjoy fast and easy DNS management!** 🚀
