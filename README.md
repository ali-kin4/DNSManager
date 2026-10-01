# DNS Manager Pro

A Windows desktop utility for switching, testing, and managing DNS configurations from one interface.

DNS Manager Pro replaces repetitive Control Panel and command-line steps with saved configurations, provider presets, benchmarking, and built-in diagnostics. It uses Windows `netsh` commands and requires administrator privileges when changing system DNS settings.

## Capabilities

- Switch between custom DNS configurations and DHCP.
- Save, load, delete, import, and export DNS presets.
- Use built-in presets for providers including Cloudflare, Google, Quad9, OpenDNS, and AdGuard.
- Detect and manage multiple Windows network adapters.
- Benchmark saved DNS configurations across selected services.
- Run network and service-latency diagnostics without blocking the interface.
- Follow the active configuration with clear status feedback.
- Use light, dark, or system-matched themes.
- Check for application updates.

## Install

### Windows release

Download the installer or portable executable from [GitHub Releases](https://github.com/ali-kin4/DNSManager/releases).

DNS changes require administrator privileges. If you use the portable build, launch it with **Run as administrator**.

### Run from source

Requirements:

- Windows 10 or 11
- Python 3.8 or newer
- Administrator privileges for DNS changes

```bash
git clone https://github.com/ali-kin4/DNSManager.git
cd DNSManager
python -m pip install -r requirements.txt
python dns_manager.py
```

## Typical workflow

1. Select the active network adapter.
2. Choose a provider preset or enter primary and secondary DNS addresses.
3. Save the configuration if you want to reuse it.
4. Benchmark or test the configuration.
5. Apply it, or select **Reset to DHCP** to return to automatic settings.

Saved configurations are stored locally in `dns_configs.json`, which is created when needed.

## Build

The repository includes PyInstaller and Inno Setup configuration for producing a portable executable and a Windows installer.

```bat
build.bat
```

See [BUILD.md](BUILD.md) for the complete build process and [DISTRIBUTION.md](DISTRIBUTION.md) for release guidance.

## Project structure

- `dns_manager.py` — desktop interface and DNS-management logic
- `updater.py` — release checking and update workflow
- `test_app.py` — component and environment checks
- `installer.iss` — Windows installer configuration
- `dns_manager.spec` — PyInstaller configuration
- `QUICKSTART.md` — task-oriented usage guide
- `FEATURES.md` — detailed feature documentation

## Safety notes

- DNS changes affect network connectivity; keep a known-good configuration available.
- Use **Reset to DHCP** if a manual configuration causes connection problems.
- Benchmark results depend on location, network conditions, and whether a service responds to the selected test method.
- Review third-party DNS providers' privacy and filtering policies before choosing one.

## License

Released under the [MIT License](LICENSE).

## Author

Built and maintained by [Ali Jabbary](https://alijabbary.com), who creates practical AI, scientific-computing, and technical tools.

Questions and bug reports are welcome through [GitHub Issues](https://github.com/ali-kin4/DNSManager/issues).
