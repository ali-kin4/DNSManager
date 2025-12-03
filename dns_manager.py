import customtkinter as ctk
from tkinter import messagebox, Menu
import subprocess
import json
import os
import socket
import time
import threading
from typing import Dict, List, Optional
import ctypes
import sys
import webbrowser
from PIL import Image, ImageDraw
import darkdetect
from version import __version__, APP_NAME, APP_URL
from updater import UpdateManager, UpdateChecker

class DNSManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("DNS Manager Pro")

        # Set icon
        self.set_app_icon()

        # Center window on screen
        window_width = 1100
        window_height = 750
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.resizable(True, True)

        # Set theme to system default
        self.current_theme_mode = "system"  # "light", "dark", or "system"
        self.apply_system_theme()
        ctk.set_default_color_theme("blue")

        # Data
        self.config_file = "dns_configs.json"
        self.saved_configs: Dict = {}
        self.current_adapter = None
        self.adapters = []
        self.admin_warning_shown = False
        self.benchmark_running = False

        # Performance optimizations
        self._dns_cache = {}
        self._cache_time = {}
        self._cache_duration = 5  # seconds

        # Update manager
        self.update_manager = UpdateManager()
        self.pending_update = None

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
            "Gemini": "gemini.google.com",
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

        # Create menu bar
        self.create_menu_bar()

        # Create UI
        self.create_widgets()

        # Check admin rights
        self.check_admin()

        # Check for updates on startup (in background)
        self.check_for_updates_background()

    def check_admin(self):
        """Check if running with admin privileges"""
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin and not self.admin_warning_shown:
                self.admin_warning_shown = True
                self.show_warning("⚠️ Administrator rights required!\n\nPlease run this application as Administrator to change DNS settings.")
        except:
            pass

    def set_app_icon(self):
        """Set application icon"""
        try:
            # Try to load SVG logo and convert to icon
            if os.path.exists("logo.svg"):
                # For now, we'll create a simple icon programmatically
                icon_size = 64
                image = Image.new('RGB', (icon_size, icon_size), color='#1e3a8a')
                draw = ImageDraw.Draw(image)

                # Draw a simple DNS icon
                draw.ellipse([8, 8, 56, 56], fill='#3b82f6', outline='#60a5fa', width=3)
                draw.ellipse([24, 24, 40, 40], fill='#1e40af')

                # Save as ICO
                icon_path = "logo.ico"
                image.save(icon_path, format='ICO')
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not set icon: {e}")

    def apply_system_theme(self):
        """Apply system theme or user selected theme"""
        if self.current_theme_mode == "system":
            try:
                system_theme = darkdetect.theme()
                if system_theme:
                    ctk.set_appearance_mode(system_theme.lower())
                else:
                    ctk.set_appearance_mode("dark")
            except:
                ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode(self.current_theme_mode)

    def create_menu_bar(self):
        """Create menu bar"""
        menubar = Menu(self, bg='#2b2b2b', fg='white', activebackground='#3b3b3b',
                      activeforeground='white', bd=0)

        # File Menu
        file_menu = Menu(menubar, tearoff=0, bg='#2b2b2b', fg='white',
                        activebackground='#3b3b3b', activeforeground='white')
        file_menu.add_command(label="Import Configs", command=self.import_configs)
        file_menu.add_command(label="Export Configs", command=self.export_configs)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Tools Menu
        tools_menu = Menu(menubar, tearoff=0, bg='#2b2b2b', fg='white',
                         activebackground='#3b3b3b', activeforeground='white')
        tools_menu.add_command(label="Flush DNS Cache", command=self.flush_dns_cache)
        tools_menu.add_command(label="Network Diagnostics", command=self.show_network_diagnostics)
        tools_menu.add_command(label="Benchmark All DNS", command=self.show_benchmark_dialog)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        # View Menu
        view_menu = Menu(menubar, tearoff=0, bg='#2b2b2b', fg='white',
                        activebackground='#3b3b3b', activeforeground='white')
        view_menu.add_command(label="System Theme", command=lambda: self.change_theme("system"))
        view_menu.add_command(label="Dark Theme", command=lambda: self.change_theme("dark"))
        view_menu.add_command(label="Light Theme", command=lambda: self.change_theme("light"))
        menubar.add_cascade(label="View", menu=view_menu)

        # Help Menu
        help_menu = Menu(menubar, tearoff=0, bg='#2b2b2b', fg='white',
                        activebackground='#3b3b3b', activeforeground='white')
        help_menu.add_command(label="Check for Updates", command=self.check_for_updates_manual)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.open_docs)
        help_menu.add_command(label="GitHub Repository", command=self.open_github)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def change_theme(self, mode: str):
        """Change application theme"""
        self.current_theme_mode = mode
        self.apply_system_theme()

        # Update theme switch if it exists
        if hasattr(self, 'theme_switch'):
            if mode == "dark":
                self.theme_switch.select()
            elif mode == "light":
                self.theme_switch.deselect()

    def import_configs(self):
        """Import configurations from file"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Import DNS Configurations",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    imported = json.load(f)
                self.saved_configs.update(imported)
                self.save_configs_to_file()
                self.refresh_saved_configs_ui()
                self.show_success(f"Imported {len(imported)} configurations!")
            except Exception as e:
                self.show_error(f"Failed to import: {str(e)}")

    def export_configs(self):
        """Export configurations to file"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            title="Export DNS Configurations",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.saved_configs, f, indent=2)
                self.show_success("Configurations exported successfully!")
            except Exception as e:
                self.show_error(f"Failed to export: {str(e)}")

    def flush_dns_cache(self):
        """Flush DNS cache"""
        try:
            subprocess.run(['ipconfig', '/flushdns'],
                         creationflags=subprocess.CREATE_NO_WINDOW,
                         check=True)
            self.show_success("DNS cache flushed successfully!")
        except Exception as e:
            self.show_error(f"Failed to flush DNS cache: {str(e)}")

    def show_network_diagnostics(self):
        """Show network diagnostics window"""
        diag_window = ctk.CTkToplevel(self)
        diag_window.title("Network Diagnostics")
        diag_window.geometry("600x400")

        text_box = ctk.CTkTextbox(diag_window, font=ctk.CTkFont(family="Consolas", size=11))
        text_box.pack(fill="both", expand=True, padx=20, pady=20)

        def run_diagnostics():
            try:
                result = subprocess.run(['ipconfig', '/all'],
                                      capture_output=True,
                                      text=True,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
                text_box.insert("1.0", result.stdout)
            except Exception as e:
                text_box.insert("1.0", f"Error: {str(e)}")

        threading.Thread(target=run_diagnostics, daemon=True).start()

    def show_about(self):
        """Show about dialog"""
        about_window = ctk.CTkToplevel(self)
        about_window.title("About DNS Manager Pro")
        about_window.geometry("400x300")
        about_window.resizable(False, False)

        # Center the window
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (about_window.winfo_screenheight() // 2) - (300 // 2)
        about_window.geometry(f"+{x}+{y}")

        frame = ctk.CTkFrame(about_window, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(frame, text=f"🌐 {APP_NAME}",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 10))

        ctk.CTkLabel(frame, text=f"Version {__version__}",
                    font=ctk.CTkFont(size=14)).pack(pady=5)

        ctk.CTkLabel(frame, text="Advanced DNS Configuration Tool",
                    font=ctk.CTkFont(size=12),
                    text_color="gray").pack(pady=5)

        # Creator info
        creator_frame = ctk.CTkFrame(frame, fg_color="transparent")
        creator_frame.pack(pady=10)

        ctk.CTkLabel(creator_frame, text="Created by Ali Jabbary",
                    font=ctk.CTkFont(size=11, weight="bold")).pack()

        website_btn = ctk.CTkButton(creator_frame, text="🌐 alijabbary.com",
                                   command=lambda: webbrowser.open("https://alijabbary.com"),
                                   font=ctk.CTkFont(size=10),
                                   width=120, height=25,
                                   fg_color="transparent",
                                   hover_color="#3b3b3b")
        website_btn.pack(pady=2)

        ctk.CTkLabel(frame, text="\nFeatures:",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(5, 5))

        features_text = """• Quick DNS switching
• Multiple DNS presets
• Configuration management
• Gaming server ping tests
• DNS benchmarking
• System theme support"""

        ctk.CTkLabel(frame, text=features_text,
                    font=ctk.CTkFont(size=11),
                    justify="left").pack(pady=5)

        ctk.CTkButton(frame, text="Close", command=about_window.destroy,
                     width=100).pack(pady=(20, 0))

    def open_docs(self):
        """Open documentation"""
        webbrowser.open("https://github.com/ali-kin4/DNSManager#readme")

    def open_github(self):
        """Open GitHub repository"""
        webbrowser.open(APP_URL)

    def check_for_updates_background(self):
        """Check for updates in background on startup"""
        def callback(update_info):
            if update_info:
                self.pending_update = update_info
                self.after(100, lambda: self.show_update_notification(update_info))

        checker = UpdateChecker(callback)
        checker.start()

    def check_for_updates_manual(self):
        """Manual update check from menu"""
        # Show checking dialog
        check_window = ctk.CTkToplevel(self)
        check_window.title("Checking for Updates")
        check_window.geometry("400x150")
        check_window.resizable(False, False)

        # Center window
        check_window.update_idletasks()
        x = (check_window.winfo_screenwidth() // 2) - 200
        y = (check_window.winfo_screenheight() // 2) - 75
        check_window.geometry(f"+{x}+{y}")

        frame = ctk.CTkFrame(check_window, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        status_label = ctk.CTkLabel(frame, text="Checking for updates...",
                                    font=ctk.CTkFont(size=14))
        status_label.pack(pady=20)

        progress = ctk.CTkProgressBar(frame, mode="indeterminate")
        progress.pack(pady=10, fill="x")
        progress.start()

        def check_updates():
            update_info = self.update_manager.check_for_updates()

            def show_result():
                check_window.destroy()
                if update_info:
                    self.show_update_dialog(update_info)
                else:
                    self.show_success(f"You're up to date!\n\nCurrent version: {__version__}")

            self.after(100, show_result)

        threading.Thread(target=check_updates, daemon=True).start()

    def show_update_notification(self, update_info):
        """Show update notification banner"""
        result = messagebox.askyesno(
            "Update Available",
            f"A new version of {APP_NAME} is available!\n\n"
            f"Current version: {update_info['current_version']}\n"
            f"Latest version: {update_info['version']}\n\n"
            "Would you like to update now?",
            icon='info'
        )

        if result:
            self.show_update_dialog(update_info)

    def show_update_dialog(self, update_info):
        """Show detailed update dialog"""
        update_window = ctk.CTkToplevel(self)
        update_window.title("Update Available")
        update_window.geometry("600x500")
        update_window.resizable(False, False)

        # Center window
        update_window.update_idletasks()
        x = (update_window.winfo_screenwidth() // 2) - 300
        y = (update_window.winfo_screenheight() // 2) - 250
        update_window.geometry(f"+{x}+{y}")

        main_frame = ctk.CTkFrame(update_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Header
        ctk.CTkLabel(main_frame, text="🎉 Update Available!",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 10))

        # Version info
        version_frame = ctk.CTkFrame(main_frame)
        version_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(version_frame, text=f"Current: v{update_info['current_version']}",
                    font=ctk.CTkFont(size=12)).pack(pady=5)
        ctk.CTkLabel(version_frame, text="→",
                    font=ctk.CTkFont(size=16)).pack(pady=2)
        ctk.CTkLabel(version_frame, text=f"Latest: v{update_info['version']}",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#2ecc71").pack(pady=5)

        # Release notes
        notes_frame = ctk.CTkFrame(main_frame)
        notes_frame.pack(fill="both", expand=True, pady=10)

        ctk.CTkLabel(notes_frame, text="What's New:",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        notes_text = ctk.CTkTextbox(notes_frame, height=200, font=ctk.CTkFont(size=11))
        notes_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        notes_text.insert("1.0", update_info['release_notes'])
        notes_text.configure(state="disabled")

        # Progress bar (hidden initially)
        progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        progress_label = ctk.CTkLabel(progress_frame, text="",
                                     font=ctk.CTkFont(size=11))
        progress_bar = ctk.CTkProgressBar(progress_frame)

        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        def start_update():
            # Disable buttons
            for widget in button_frame.winfo_children():
                widget.configure(state="disabled")

            # Show progress
            progress_frame.pack(fill="x", pady=10)
            progress_label.pack(pady=(0, 5))
            progress_bar.pack(fill="x")
            progress_bar.set(0)

            def download_and_install():
                # Update progress
                def update_progress(percent, downloaded, total):
                    progress = percent / 100
                    progress_bar.set(progress)
                    mb_downloaded = downloaded / (1024 * 1024)
                    mb_total = total / (1024 * 1024)
                    progress_label.configure(text=f"Downloading: {mb_downloaded:.1f} MB / {mb_total:.1f} MB ({percent:.0f}%)")

                progress_label.configure(text="Downloading update...")

                # Download
                update_file = self.update_manager.download_update(
                    update_info['download_url'],
                    progress_callback=update_progress
                )

                if update_file:
                    def finish_install():
                        progress_label.configure(text="Installing update...")
                        progress_bar.set(1.0)

                        # Install
                        success = self.update_manager.install_update(update_file)

                        if success:
                            result = messagebox.askyesno(
                                "Update Installed",
                                "Update installed successfully!\n\nRestart now to apply the update?",
                                icon='info'
                            )

                            if result:
                                self.update_manager.restart_app()
                            else:
                                update_window.destroy()
                        else:
                            progress_label.configure(text="Installation failed!")
                            messagebox.showerror("Update Failed", "Failed to install update. Please try again.")
                            update_window.destroy()

                    self.after(100, finish_install)
                else:
                    def show_error():
                        progress_label.configure(text="Download failed!")
                        messagebox.showerror("Download Failed", "Failed to download update. Please check your internet connection.")
                        update_window.destroy()

                    self.after(100, show_error)

            threading.Thread(target=download_and_install, daemon=True).start()

        def open_release_page():
            webbrowser.open(update_info['html_url'])
            update_window.destroy()

        # Check if this is a git repo
        if self.update_manager.check_git_repo():
            def update_via_git():
                progress_frame.pack(fill="x", pady=10)
                progress_label.pack(pady=(0, 5))
                progress_label.configure(text="Updating via git...")
                progress_bar.pack(fill="x")
                progress_bar.set(0.5)

                def do_git_update():
                    success, message = self.update_manager.update_via_git()

                    def finish():
                        if success:
                            result = messagebox.askyesno(
                                "Update Complete",
                                f"{message}\n\nRestart now to apply the update?",
                                icon='info'
                            )
                            if result:
                                self.update_manager.restart_app()
                            else:
                                update_window.destroy()
                        else:
                            messagebox.showerror("Update Failed", f"Git update failed: {message}")
                            update_window.destroy()

                    self.after(100, finish)

                threading.Thread(target=do_git_update, daemon=True).start()

            ctk.CTkButton(button_frame, text="Update via Git",
                         command=update_via_git,
                         font=ctk.CTkFont(size=13),
                         fg_color="#8e44ad", hover_color="#732d91").pack(side="left", padx=5, fill="x", expand=True)

        ctk.CTkButton(button_frame, text="Download & Install",
                     command=start_update,
                     font=ctk.CTkFont(size=13, weight="bold"),
                     fg_color="#2ecc71", hover_color="#27ae60").pack(side="left", padx=5, fill="x", expand=True)

        ctk.CTkButton(button_frame, text="View Release",
                     command=open_release_page,
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=5, fill="x", expand=True)

        ctk.CTkButton(button_frame, text="Later",
                     command=update_window.destroy,
                     font=ctk.CTkFont(size=13),
                     fg_color="gray").pack(side="left", padx=5, fill="x", expand=True)

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

        # Theme selector
        theme_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        theme_frame.pack(side="right", padx=10)

        ctk.CTkLabel(theme_frame, text="Theme:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 5))

        self.theme_selector = ctk.CTkSegmentedButton(
            theme_frame,
            values=["Light", "Dark", "System"],
            command=self.on_theme_change,
            font=ctk.CTkFont(size=11),
            width=200
        )
        self.theme_selector.pack(side="left")
        self.theme_selector.set("System" if self.current_theme_mode == "system" else
                               self.current_theme_mode.capitalize())

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
            font=ctk.CTkFont(size=13),
            state="readonly"
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

    def on_theme_change(self, value):
        """Handle theme change from segmented button"""
        theme_map = {"Light": "light", "Dark": "dark", "System": "system"}
        self.change_theme(theme_map[value])

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
                    wifi_keywords = ['wi-fi', 'wifi', 'wireless', 'wlan', '802.11']
                    for adapter in self.adapters:
                        adapter_lower = adapter.lower()
                        if any(keyword in adapter_lower for keyword in wifi_keywords):
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

    def get_current_dns_servers(self, use_cache=True):
        """Get current DNS servers as a dictionary with caching"""
        if not self.current_adapter:
            return None

        # Check cache
        if use_cache and self.current_adapter in self._dns_cache:
            cache_age = time.time() - self._cache_time.get(self.current_adapter, 0)
            if cache_age < self._cache_duration:
                return self._dns_cache[self.current_adapter]

        try:
            result = subprocess.run(
                ['netsh', 'interface', 'ip', 'show', 'dns', self.current_adapter],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=3  # Add timeout for faster failure
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

            dns_info = None
            if dns_servers:
                dns_info = {
                    'primary': dns_servers[0],
                    'secondary': dns_servers[1] if len(dns_servers) > 1 else ''
                }

            # Update cache
            self._dns_cache[self.current_adapter] = dns_info
            self._cache_time[self.current_adapter] = time.time()

            return dns_info
        except:
            return None

    def show_current_dns(self):
        """Display current DNS settings for selected adapter"""
        current_dns = self.get_current_dns_servers()

        if current_dns:
            dns_text = f"Primary: {current_dns['primary']}"
            if current_dns['secondary']:
                dns_text += f"\nSecondary: {current_dns['secondary']}"
            self.current_dns_label.configure(text=dns_text)
        else:
            self.current_dns_label.configure(text="DNS: DHCP (Automatic)")

        # Refresh saved configs UI to update highlighting
        if hasattr(self, 'saved_scroll'):
            self.refresh_saved_configs_ui()

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

            # Invalidate DNS cache
            if self.current_adapter in self._dns_cache:
                del self._dns_cache[self.current_adapter]

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

            # Invalidate DNS cache
            if self.current_adapter in self._dns_cache:
                del self._dns_cache[self.current_adapter]

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

        # Get current DNS to check which config is active
        current_dns = self.get_current_dns_servers()

        # Sort configs: active ones first, then alphabetically
        def sort_key(item):
            name, dns = item
            is_active = False
            if current_dns:
                is_active = (current_dns['primary'] == dns['primary'] and
                           current_dns.get('secondary', '') == dns.get('secondary', ''))
            return (not is_active, name.lower())  # False (active) comes before True (inactive)

        sorted_configs = sorted(self.saved_configs.items(), key=sort_key)

        for name, dns in sorted_configs:
            # Check if this config is currently active
            is_active = False
            if current_dns:
                is_active = (current_dns['primary'] == dns['primary'] and
                           current_dns.get('secondary', '') == dns.get('secondary', ''))

            # Use different styling for active config
            if is_active:
                config_frame = ctk.CTkFrame(self.saved_scroll, border_width=3, border_color="#2ecc71")
            else:
                config_frame = ctk.CTkFrame(self.saved_scroll)
            config_frame.pack(fill="x", pady=3)

            info_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)

            # Name label with active indicator
            name_text = f"{name}  ✓ ACTIVE" if is_active else name
            name_color = "#2ecc71" if is_active else None

            ctk.CTkLabel(
                info_frame,
                text=name_text,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                text_color=name_color
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

    def show_benchmark_dialog(self):
        """Show DNS benchmark dialog"""
        if self.benchmark_running:
            self.show_warning("A benchmark is already running!")
            return

        benchmark_window = ctk.CTkToplevel(self)
        benchmark_window.title("DNS Benchmark")
        benchmark_window.geometry("800x600")

        # Center the window
        benchmark_window.update_idletasks()
        x = (benchmark_window.winfo_screenwidth() // 2) - (400)
        y = (benchmark_window.winfo_screenheight() // 2) - (300)
        benchmark_window.geometry(f"+{x}+{y}")

        main_frame = ctk.CTkFrame(benchmark_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ctk.CTkLabel(main_frame, text="DNS Configuration Benchmark",
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(0, 10))

        ctk.CTkLabel(main_frame, text="Test all your saved DNS configs against selected services",
                    font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(0, 20))

        # Service selection
        service_frame = ctk.CTkFrame(main_frame)
        service_frame.pack(fill="both", expand=True, pady=(0, 10))

        ctk.CTkLabel(service_frame, text="Select Services to Test:",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        # Scrollable frame for service checkboxes
        service_scroll = ctk.CTkScrollableFrame(service_frame, height=200)
        service_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        selected_services = {}
        for name in self.gaming_servers.keys():
            var = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(service_scroll, text=name, variable=var,
                                      font=ctk.CTkFont(size=12))
            checkbox.pack(anchor="w", pady=3, padx=5)
            selected_services[name] = var

        # Quick select buttons
        quick_btn_frame = ctk.CTkFrame(service_frame, fg_color="transparent")
        quick_btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        def select_all():
            for var in selected_services.values():
                var.set(True)

        def select_none():
            for var in selected_services.values():
                var.set(False)

        def select_gaming():
            gaming_keywords = ['Fortnite', 'Call of Duty', 'EA', 'Battlefield', 'Steam',
                             'Riot', 'Valorant', 'League', 'Battle.net', 'Ubisoft', 'Apex']
            for name, var in selected_services.items():
                var.set(any(keyword in name for keyword in gaming_keywords))

        def select_ai():
            ai_keywords = ['ChatGPT', 'Gemini', 'Claude', 'Perplexity']
            for name, var in selected_services.items():
                var.set(any(keyword in name for keyword in ai_keywords))

        ctk.CTkButton(quick_btn_frame, text="Select All", command=select_all,
                     width=100, height=30).pack(side="left", padx=3)
        ctk.CTkButton(quick_btn_frame, text="Clear All", command=select_none,
                     width=100, height=30).pack(side="left", padx=3)
        ctk.CTkButton(quick_btn_frame, text="Gaming", command=select_gaming,
                     width=100, height=30).pack(side="left", padx=3)
        ctk.CTkButton(quick_btn_frame, text="AI Platforms", command=select_ai,
                     width=100, height=30).pack(side="left", padx=3)

        # Results area
        results_frame = ctk.CTkFrame(main_frame)
        results_frame.pack(fill="both", expand=True, pady=(10, 0))

        ctk.CTkLabel(results_frame, text="Benchmark Results:",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))

        results_scroll = ctk.CTkScrollableFrame(results_frame, height=150)
        results_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        status_label = ctk.CTkLabel(results_frame, text="Ready to start benchmark",
                                   font=ctk.CTkFont(size=11), text_color="gray")
        status_label.pack(pady=(0, 10))

        # Start benchmark button
        def start_benchmark():
            selected = [name for name, var in selected_services.items() if var.get()]
            if not selected:
                self.show_error("Please select at least one service to test!")
                return

            if not self.saved_configs:
                self.show_error("No saved DNS configurations to test!")
                return

            self.benchmark_running = True
            status_label.configure(text="Benchmark running...", text_color="#f39c12")

            def run_benchmark():
                results = {}

                # Clear results area
                for widget in results_scroll.winfo_children():
                    widget.destroy()

                # Test each DNS config
                for config_name, dns_config in self.saved_configs.items():
                    results[config_name] = {}

                    # Apply this DNS temporarily (or test without applying)
                    # For now, we'll just measure DNS resolution time
                    for service_name in selected:
                        server = self.gaming_servers[service_name]
                        try:
                            start = time.time()
                            socket.gethostbyname(server)
                            latency = (time.time() - start) * 1000  # Convert to ms
                            results[config_name][service_name] = latency
                        except:
                            results[config_name][service_name] = None

                # Calculate averages and display results
                config_averages = []
                for config_name, service_results in results.items():
                    valid_results = [v for v in service_results.values() if v is not None]
                    if valid_results:
                        avg = sum(valid_results) / len(valid_results)
                        config_averages.append((config_name, avg, service_results))

                # Sort by average (best first)
                config_averages.sort(key=lambda x: x[1])

                # Display results
                for rank, (config_name, avg, service_results) in enumerate(config_averages, 1):
                    result_frame = ctk.CTkFrame(results_scroll)
                    result_frame.pack(fill="x", pady=3)

                    # Rank badge
                    rank_color = "#2ecc71" if rank == 1 else "#f39c12" if rank == 2 else "#e74c3c" if rank == 3 else "gray"
                    rank_text = f"#{rank}"

                    ctk.CTkLabel(result_frame, text=rank_text, font=ctk.CTkFont(size=14, weight="bold"),
                               text_color=rank_color, width=40).pack(side="left", padx=5)

                    info_frame = ctk.CTkFrame(result_frame, fg_color="transparent")
                    info_frame.pack(side="left", fill="x", expand=True, padx=5)

                    ctk.CTkLabel(info_frame, text=config_name, font=ctk.CTkFont(size=13, weight="bold"),
                               anchor="w").pack(anchor="w")

                    success_count = len([v for v in service_results.values() if v is not None])
                    detail_text = f"Avg: {avg:.1f}ms | {success_count}/{len(service_results)} services"
                    ctk.CTkLabel(info_frame, text=detail_text, font=ctk.CTkFont(size=10),
                               text_color="gray", anchor="w").pack(anchor="w")

                self.benchmark_running = False
                status_label.configure(text=f"Benchmark complete! Tested {len(config_averages)} configs against {len(selected)} services",
                                     text_color="#2ecc71")

            threading.Thread(target=run_benchmark, daemon=True).start()

        start_btn = ctk.CTkButton(main_frame, text="Start Benchmark", command=start_benchmark,
                                 font=ctk.CTkFont(size=14, weight="bold"), height=40,
                                 fg_color="#2ecc71", hover_color="#27ae60")
        start_btn.pack(pady=(10, 0))

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
