import customtkinter as ctk
from tkinter import messagebox
import subprocess
import json
import os
import socket
import time
import threading
from typing import Dict, List, Optional
import ctypes
import sys

class DNSManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("DNS Manager Pro")

        # Center window on screen
        window_width = 1100
        window_height = 750
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.resizable(True, True)

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Data
        self.config_file = "dns_configs.json"
        self.saved_configs: Dict = {}
        self.current_adapter = None
        self.adapters = []
        self.admin_warning_shown = False

        # Gaming servers for ping tests
        self.gaming_servers = {
            "Fortnite (NA-East)": "qosping-aws-us-east-1.ol.epicgames.com",
            "Fortnite (EU)": "qosping-aws-eu-west-1.ol.epicgames.com",
            "Epic Games": "epicgames.com",
            "Call of Duty (Activision)": "activision.com",
            "EA Servers": "ea.com",
            "Battlefield": "battlefield.com",
            "Steam": "store.steampowered.com",
            "Riot Games": "riotgames.com",
            "Valorant": "playvalorant.com",
            "League of Legends": "leagueoflegends.com",
            "Battle.net": "battle.net",
            "Ubisoft": "ubisoft.com",
            "Apex Legends": "playapex.com",
            "ChatGPT": "chat.openai.com",
            "Gemini (Google)": "gemini.google.com",
            "Claude": "claude.ai",
            "Perplexity": "perplexity.ai",
            "YouTube": "youtube.com",
            "Cloudflare": "1.1.1.1",
            "Google DNS": "8.8.8.8"
        }

        # Popular DNS presets
        self.dns_presets = {
            "Cloudflare": {"primary": "1.1.1.1", "secondary": "1.0.0.1"},
            "Cloudflare Family": {"primary": "1.1.1.3", "secondary": "1.0.0.3"},
            "Google": {"primary": "8.8.8.8", "secondary": "8.8.4.4"},
            "OpenDNS": {"primary": "208.67.222.222", "secondary": "208.67.220.220"},
            "Quad9": {"primary": "9.9.9.9", "secondary": "149.112.112.112"},
            "AdGuard": {"primary": "94.140.14.14", "secondary": "94.140.15.15"},
            "Comodo Secure": {"primary": "8.26.56.26", "secondary": "8.20.247.20"},
            "CleanBrowsing": {"primary": "185.228.168.9", "secondary": "185.228.169.9"},
            "Alternate DNS": {"primary": "76.76.19.19", "secondary": "76.223.122.150"},
        }

        # Load saved configurations
        self.load_configs()

        # Get network adapters
        self.refresh_adapters()

        # Create UI
        self.create_widgets()

        # Check admin rights
        self.check_admin()

    def check_admin(self):
        """Check if running with admin privileges"""
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin and not self.admin_warning_shown:
                self.admin_warning_shown = True
                self.show_warning("⚠️ Administrator rights required!\n\nPlease run this application as Administrator to change DNS settings.")
        except:
            pass

    def create_widgets(self):
        """Create all UI elements"""
        # Main container with padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        title_label = ctk.CTkLabel(
            header_frame,
            text="🌐 DNS Manager Pro",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(side="left")

        # Theme toggle
        self.theme_switch = ctk.CTkSwitch(
            header_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            font=ctk.CTkFont(size=12)
        )
        self.theme_switch.pack(side="right", padx=10)
        self.theme_switch.select()

        # Content area with 2 columns
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # Left column - DNS Configuration
        left_column = ctk.CTkFrame(content_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right column - Saved Configs & Tests
        right_column = ctk.CTkFrame(content_frame)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # === LEFT COLUMN ===

        # Network Adapter Selection
        adapter_frame = ctk.CTkFrame(left_column)
        adapter_frame.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            adapter_frame,
            text="Network Adapter",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        adapter_inner = ctk.CTkFrame(adapter_frame, fg_color="transparent")
        adapter_inner.pack(fill="x", padx=10, pady=(0, 10))

        self.adapter_combo = ctk.CTkComboBox(
            adapter_inner,
            values=self.adapters,
            width=350,
            command=self.on_adapter_change,
            font=ctk.CTkFont(size=13)
        )
        self.adapter_combo.pack(side="left", fill="x", expand=True)

        refresh_btn = ctk.CTkButton(
            adapter_inner,
            text="🔄",
            width=40,
            command=self.refresh_adapters,
            font=ctk.CTkFont(size=16)
        )
        refresh_btn.pack(side="right", padx=(10, 0))

        # Current DNS Display
        current_frame = ctk.CTkFrame(left_column)
        current_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(
            current_frame,
            text="Current DNS",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.current_dns_label = ctk.CTkLabel(
            current_frame,
            text="Select an adapter to view DNS",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        self.current_dns_label.pack(anchor="w", padx=10, pady=(0, 10))

        # DNS Input Section
        input_frame = ctk.CTkFrame(left_column)
        input_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(
            input_frame,
            text="Set DNS Servers",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # Primary DNS
        ctk.CTkLabel(
            input_frame,
            text="Primary DNS:",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", padx=10, pady=(10, 2))

        self.primary_dns_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="e.g., 1.1.1.1",
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.primary_dns_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Secondary DNS
        ctk.CTkLabel(
            input_frame,
            text="Secondary DNS:",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", padx=10, pady=(0, 2))

        self.secondary_dns_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="e.g., 1.0.0.1",
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.secondary_dns_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Action buttons
        btn_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        apply_btn = ctk.CTkButton(
            btn_frame,
            text="Apply DNS",
            command=self.apply_dns,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        apply_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        reset_btn = ctk.CTkButton(
            btn_frame,
            text="Reset to DHCP",
            command=self.reset_dns,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        reset_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # DNS Presets
        presets_frame = ctk.CTkFrame(left_column)
        presets_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        ctk.CTkLabel(
            presets_frame,
            text="Popular DNS Providers",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # Scrollable frame for presets
        presets_scroll = ctk.CTkScrollableFrame(presets_frame, height=200)
        presets_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for name, dns in self.dns_presets.items():
            preset_btn = ctk.CTkButton(
                presets_scroll,
                text=f"{name} ({dns['primary']})",
                command=lambda d=dns: self.load_preset(d),
                font=ctk.CTkFont(size=12),
                height=35,
                anchor="w"
            )
            preset_btn.pack(fill="x", pady=2)

        # === RIGHT COLUMN ===

        # Save Configuration
        save_frame = ctk.CTkFrame(right_column)
        save_frame.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            save_frame,
            text="Save Current Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        save_inner = ctk.CTkFrame(save_frame, fg_color="transparent")
        save_inner.pack(fill="x", padx=10, pady=(0, 10))

        self.config_name_entry = ctk.CTkEntry(
            save_inner,
            placeholder_text="Configuration name...",
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.config_name_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        save_btn = ctk.CTkButton(
            save_inner,
            text="💾 Save",
            command=self.save_config,
            width=80,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        save_btn.pack(side="right")

        # Saved Configurations
        saved_frame = ctk.CTkFrame(right_column)
        saved_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        header_inner = ctk.CTkFrame(saved_frame, fg_color="transparent")
        header_inner.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            header_inner,
            text="Saved Configurations",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")

        refresh_configs_btn = ctk.CTkButton(
            header_inner,
            text="🔄",
            width=30,
            command=self.refresh_saved_configs_ui,
            font=ctk.CTkFont(size=14)
        )
        refresh_configs_btn.pack(side="right")

        self.saved_scroll = ctk.CTkScrollableFrame(saved_frame, height=200)
        self.saved_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.refresh_saved_configs_ui()

        # Ping Tests
        ping_frame = ctk.CTkFrame(right_column)
        ping_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        ping_header = ctk.CTkFrame(ping_frame, fg_color="transparent")
        ping_header.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            ping_header,
            text="Gaming Server Ping Tests",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")

        test_all_btn = ctk.CTkButton(
            ping_header,
            text="Test All",
            command=self.test_all_servers,
            width=90,
            height=30,
            font=ctk.CTkFont(size=12)
        )
        test_all_btn.pack(side="right")

        self.ping_scroll = ctk.CTkScrollableFrame(ping_frame, height=200)
        self.ping_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Create ping test buttons
        self.ping_labels = {}
        for name, server in self.gaming_servers.items():
            server_frame = ctk.CTkFrame(self.ping_scroll, fg_color="transparent")
            server_frame.pack(fill="x", pady=2)

            btn = ctk.CTkButton(
                server_frame,
                text=name,
                command=lambda s=server, n=name: self.ping_server(s, n),
                width=250,
                height=30,
                anchor="w",
                font=ctk.CTkFont(size=12)
            )
            btn.pack(side="left", padx=(0, 5))

            label = ctk.CTkLabel(
                server_frame,
                text="--",
                font=ctk.CTkFont(size=11),
                width=80
            )
            label.pack(side="right")
            self.ping_labels[name] = label

    def toggle_theme(self):
        """Toggle between dark and light mode"""
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def refresh_adapters(self):
        """Get list of network adapters"""
        try:
            result = subprocess.run(
                ['netsh', 'interface', 'show', 'interface'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            self.adapters = []
            lines = result.stdout.split('\n')
            for line in lines[3:]:  # Skip header lines
                parts = line.split()
                if len(parts) >= 4 and parts[0] in ['Enabled', 'Connected']:
                    adapter_name = ' '.join(parts[3:])
                    if adapter_name:
                        self.adapters.append(adapter_name)

            if hasattr(self, 'adapter_combo') and self.adapters:
                self.adapter_combo.configure(values=self.adapters)
                if self.adapters:
                    # Try to find WiFi adapter as default
                    default_adapter = self.adapters[0]
                    for adapter in self.adapters:
                        if 'wi-fi' in adapter.lower() or 'wifi' in adapter.lower() or 'wireless' in adapter.lower():
                            default_adapter = adapter
                            break

                    self.adapter_combo.set(default_adapter)
                    self.current_adapter = default_adapter
                    self.show_current_dns()
        except Exception as e:
            self.show_error(f"Failed to get network adapters: {str(e)}")

    def on_adapter_change(self, choice):
        """Handle adapter selection change"""
        self.current_adapter = choice
        self.show_current_dns()

    def show_current_dns(self):
        """Display current DNS settings for selected adapter"""
        if not self.current_adapter:
            return

        try:
            result = subprocess.run(
                ['netsh', 'interface', 'ip', 'show', 'dns', self.current_adapter],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            dns_servers = []
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Statically Configured DNS Servers:' in line or 'DNS servers configured through DHCP:' in line:
                    continue
                if any(part.replace('.', '').isdigit() for part in line.split()):
                    ip = line.strip().split()[-1]
                    if self.is_valid_ip(ip):
                        dns_servers.append(ip)

            if dns_servers:
                dns_text = f"Primary: {dns_servers[0]}"
                if len(dns_servers) > 1:
                    dns_text += f"\nSecondary: {dns_servers[1]}"
                self.current_dns_label.configure(text=dns_text)
            else:
                self.current_dns_label.configure(text="DNS: DHCP (Automatic)")
        except Exception as e:
            self.current_dns_label.configure(text=f"Error: {str(e)}")

    def is_valid_ip(self, ip: str) -> bool:
        """Validate IP address format"""
        try:
            parts = ip.split('.')
            return len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts)
        except:
            return False

    def apply_dns(self):
        """Apply DNS settings to selected adapter"""
        if not self.current_adapter:
            self.show_error("Please select a network adapter first!")
            return

        primary = self.primary_dns_entry.get().strip()
        secondary = self.secondary_dns_entry.get().strip()

        if not primary:
            self.show_error("Please enter at least a primary DNS server!")
            return

        if not self.is_valid_ip(primary):
            self.show_error("Invalid primary DNS IP address!")
            return

        if secondary and not self.is_valid_ip(secondary):
            self.show_error("Invalid secondary DNS IP address!")
            return

        try:
            # Set primary DNS
            subprocess.run(
                ['netsh', 'interface', 'ip', 'set', 'dns', self.current_adapter, 'static', primary],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Set secondary DNS if provided
            if secondary:
                subprocess.run(
                    ['netsh', 'interface', 'ip', 'add', 'dns', self.current_adapter, secondary, 'index=2'],
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

            self.show_success(f"DNS applied successfully!\n\nPrimary: {primary}" + (f"\nSecondary: {secondary}" if secondary else ""))
            self.show_current_dns()

            # Flush DNS cache
            subprocess.run(['ipconfig', '/flushdns'], creationflags=subprocess.CREATE_NO_WINDOW)
        except subprocess.CalledProcessError as e:
            self.show_error(f"Failed to apply DNS. Make sure you're running as Administrator!\n\nError: {str(e)}")
        except Exception as e:
            self.show_error(f"Error: {str(e)}")

    def reset_dns(self):
        """Reset DNS to DHCP (automatic)"""
        if not self.current_adapter:
            self.show_error("Please select a network adapter first!")
            return

        try:
            subprocess.run(
                ['netsh', 'interface', 'ip', 'set', 'dns', self.current_adapter, 'dhcp'],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            self.show_success("DNS reset to DHCP (automatic) successfully!")
            self.show_current_dns()
            subprocess.run(['ipconfig', '/flushdns'], creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as e:
            self.show_error(f"Failed to reset DNS: {str(e)}")

    def load_preset(self, dns: Dict[str, str]):
        """Load a DNS preset into the input fields"""
        self.primary_dns_entry.delete(0, 'end')
        self.primary_dns_entry.insert(0, dns['primary'])
        self.secondary_dns_entry.delete(0, 'end')
        self.secondary_dns_entry.insert(0, dns['secondary'])

    def save_config(self):
        """Save current DNS configuration"""
        name = self.config_name_entry.get().strip()
        primary = self.primary_dns_entry.get().strip()
        secondary = self.secondary_dns_entry.get().strip()

        if not name:
            self.show_error("Please enter a configuration name!")
            return

        if not primary:
            self.show_error("Please enter at least a primary DNS!")
            return

        if not self.is_valid_ip(primary):
            self.show_error("Invalid primary DNS IP!")
            return

        if secondary and not self.is_valid_ip(secondary):
            self.show_error("Invalid secondary DNS IP!")
            return

        self.saved_configs[name] = {
            'primary': primary,
            'secondary': secondary
        }

        self.save_configs_to_file()
        self.config_name_entry.delete(0, 'end')
        self.refresh_saved_configs_ui()
        self.show_success(f"Configuration '{name}' saved successfully!")

    def load_configs(self):
        """Load saved configurations from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.saved_configs = json.load(f)
        except Exception as e:
            print(f"Error loading configs: {e}")
            self.saved_configs = {}

    def save_configs_to_file(self):
        """Save configurations to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.saved_configs, f, indent=2)
        except Exception as e:
            self.show_error(f"Error saving configs: {e}")

    def refresh_saved_configs_ui(self):
        """Refresh the saved configurations display"""
        # Clear existing widgets
        for widget in self.saved_scroll.winfo_children():
            widget.destroy()

        if not self.saved_configs:
            ctk.CTkLabel(
                self.saved_scroll,
                text="No saved configurations yet",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(pady=20)
            return

        for name, dns in self.saved_configs.items():
            config_frame = ctk.CTkFrame(self.saved_scroll)
            config_frame.pack(fill="x", pady=3)

            info_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)

            ctk.CTkLabel(
                info_frame,
                text=name,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                info_frame,
                text=f"{dns['primary']} | {dns['secondary']}",
                font=ctk.CTkFont(size=11),
                text_color="gray",
                anchor="w"
            ).pack(anchor="w")

            btn_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
            btn_frame.pack(side="right", padx=5)

            load_btn = ctk.CTkButton(
                btn_frame,
                text="Load",
                command=lambda d=dns: self.load_preset(d),
                width=60,
                height=25,
                font=ctk.CTkFont(size=11)
            )
            load_btn.pack(side="left", padx=2)

            apply_btn = ctk.CTkButton(
                btn_frame,
                text="Apply",
                command=lambda d=dns: self.quick_apply(d),
                width=60,
                height=25,
                font=ctk.CTkFont(size=11),
                fg_color="#2ecc71",
                hover_color="#27ae60"
            )
            apply_btn.pack(side="left", padx=2)

            delete_btn = ctk.CTkButton(
                btn_frame,
                text="🗑️",
                command=lambda n=name: self.delete_config(n),
                width=30,
                height=25,
                font=ctk.CTkFont(size=11),
                fg_color="#e74c3c",
                hover_color="#c0392b"
            )
            delete_btn.pack(side="left", padx=2)

    def quick_apply(self, dns: Dict[str, str]):
        """Quickly apply a saved DNS configuration"""
        self.load_preset(dns)
        self.apply_dns()

    def delete_config(self, name: str):
        """Delete a saved configuration"""
        if name in self.saved_configs:
            del self.saved_configs[name]
            self.save_configs_to_file()
            self.refresh_saved_configs_ui()
            self.show_success(f"Configuration '{name}' deleted!")

    def ping_server(self, server: str, name: str):
        """Ping a gaming server"""
        def do_ping():
            label = self.ping_labels[name]
            label.configure(text="Testing...")

            try:
                # Try to resolve hostname first
                try:
                    ip = socket.gethostbyname(server)
                except:
                    ip = server

                # Perform ping
                start_time = time.time()
                result = subprocess.run(
                    ['ping', '-n', '4', ip],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                # Parse average latency
                output = result.stdout
                if 'Average' in output:
                    avg_line = [line for line in output.split('\n') if 'Average' in line][0]
                    latency = avg_line.split('=')[-1].strip().replace('ms', '').strip()

                    # Color code based on latency
                    try:
                        lat_val = int(latency)
                        if lat_val < 50:
                            color = "#2ecc71"  # Green
                        elif lat_val < 100:
                            color = "#f39c12"  # Orange
                        else:
                            color = "#e74c3c"  # Red
                        label.configure(text=f"{latency}ms", text_color=color)
                    except:
                        label.configure(text=f"{latency}ms")
                elif 'unreachable' in output.lower() or 'timed out' in output.lower():
                    label.configure(text="Timeout", text_color="#e74c3c")
                else:
                    label.configure(text="Failed", text_color="#e74c3c")
            except subprocess.TimeoutExpired:
                label.configure(text="Timeout", text_color="#e74c3c")
            except Exception as e:
                label.configure(text="Error", text_color="#e74c3c")

        threading.Thread(target=do_ping, daemon=True).start()

    def test_all_servers(self):
        """Test all gaming servers"""
        for name, server in self.gaming_servers.items():
            self.ping_server(server, name)
            time.sleep(0.1)  # Small delay to stagger requests

    def show_error(self, message: str):
        """Show error message"""
        messagebox.showerror("Error", message)

    def show_success(self, message: str):
        """Show success message"""
        messagebox.showinfo("Success", message)

    def show_warning(self, message: str):
        """Show warning message"""
        messagebox.showwarning("Warning", message)

def main():
    """Main entry point"""
    # Check if running on Windows
    if sys.platform != 'win32':
        print("This application only works on Windows!")
        sys.exit(1)

    app = DNSManager()
    app.mainloop()

if __name__ == "__main__":
    main()
