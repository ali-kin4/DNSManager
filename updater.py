"""
Auto-update system for DNS Manager Pro
Handles checking for updates and installing them automatically
"""

import os
import sys
import json
import urllib.request
import urllib.error
import zipfile
import shutil
import subprocess
import tempfile
from typing import Optional, Dict, Tuple
from pathlib import Path
import threading

from version import __version__, RELEASES_API_URL, GITHUB_REPO


class UpdateManager:
    """Manages application updates from GitHub releases"""

    def __init__(self):
        self.current_version = __version__
        self.is_frozen = getattr(sys, 'frozen', False)
        self.app_dir = self._get_app_directory()

    def _get_app_directory(self) -> Path:
        """Get the application directory"""
        if self.is_frozen:
            return Path(sys.executable).parent
        return Path(__file__).parent

    def check_for_updates(self, timeout=10) -> Optional[Dict]:
        """
        Check GitHub for latest release
        Returns: dict with update info or None
        """
        try:
            headers = {'User-Agent': 'DNS-Manager-Pro'}
            req = urllib.request.Request(RELEASES_API_URL, headers=headers)

            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = json.loads(response.read().decode())

                latest_version = data.get('tag_name', '').lstrip('v')

                if self._is_newer_version(latest_version):
                    return {
                        'version': latest_version,
                        'current_version': self.current_version,
                        'release_notes': data.get('body', 'No release notes available'),
                        'download_url': self._get_download_url(data),
                        'published_at': data.get('published_at', ''),
                        'html_url': data.get('html_url', '')
                    }
                return None

        except urllib.error.URLError as e:
            print(f"Network error checking for updates: {e}")
            return None
        except Exception as e:
            print(f"Error checking for updates: {e}")
            return None

    def _is_newer_version(self, latest: str) -> bool:
        """Compare version strings"""
        try:
            current_parts = [int(x) for x in self.current_version.split('.')]
            latest_parts = [int(x) for x in latest.split('.')]

            # Pad shorter version with zeros
            max_len = max(len(current_parts), len(latest_parts))
            current_parts += [0] * (max_len - len(current_parts))
            latest_parts += [0] * (max_len - len(latest_parts))

            return latest_parts > current_parts
        except:
            return False

    def _get_download_url(self, release_data: Dict) -> Optional[str]:
        """Extract the appropriate download URL from release assets"""
        assets = release_data.get('assets', [])

        # Look for installer first, then exe, then zip
        for asset in assets:
            name = asset.get('name', '').lower()
            if name.endswith('.exe') and 'setup' in name:
                return asset.get('browser_download_url')

        for asset in assets:
            name = asset.get('name', '').lower()
            if name.endswith('.exe'):
                return asset.get('browser_download_url')

        for asset in assets:
            name = asset.get('name', '').lower()
            if name.endswith('.zip'):
                return asset.get('browser_download_url')

        return release_data.get('zipball_url')

    def download_update(self, download_url: str, progress_callback=None) -> Optional[Path]:
        """
        Download update file
        Returns: Path to downloaded file or None
        """
        try:
            # Create temp directory
            temp_dir = Path(tempfile.gettempdir()) / 'dns_manager_update'
            temp_dir.mkdir(exist_ok=True)

            # Determine file extension
            if download_url.endswith('.exe'):
                filename = 'dns_manager_setup.exe'
            else:
                filename = 'dns_manager_update.zip'

            file_path = temp_dir / filename

            # Download with progress
            headers = {'User-Agent': 'DNS-Manager-Pro'}
            req = urllib.request.Request(download_url, headers=headers)

            with urllib.request.urlopen(req) as response:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0

                with open(file_path, 'wb') as f:
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)

                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress, downloaded, total_size)

            return file_path

        except Exception as e:
            print(f"Error downloading update: {e}")
            return None

    def install_update(self, update_file: Path, silent=False) -> bool:
        """
        Install the downloaded update
        Returns: True if successful
        """
        try:
            if update_file.suffix == '.exe':
                # Run installer
                if silent:
                    subprocess.Popen([str(update_file), '/VERYSILENT', '/CLOSEAPPLICATIONS', '/RESTARTAPPLICATIONS'])
                else:
                    subprocess.Popen([str(update_file)])
                return True

            elif update_file.suffix == '.zip':
                # Extract and replace files
                return self._install_from_zip(update_file)

            return False

        except Exception as e:
            print(f"Error installing update: {e}")
            return False

    def _install_from_zip(self, zip_path: Path) -> bool:
        """Extract ZIP and replace application files"""
        try:
            # Create backup
            backup_dir = self.app_dir / 'backup'
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            backup_dir.mkdir(exist_ok=True)

            # Backup critical files
            for item in self.app_dir.iterdir():
                if item.name not in ['backup', 'dns_configs.json', 'logo.ico']:
                    if item.is_file():
                        shutil.copy2(item, backup_dir / item.name)
                    elif item.is_dir() and item.name != '__pycache__':
                        shutil.copytree(item, backup_dir / item.name, dirs_exist_ok=True)

            # Extract new files
            temp_extract = self.app_dir / 'temp_update'
            temp_extract.mkdir(exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract)

            # Find the actual content directory (might be nested)
            content_dir = temp_extract
            subdirs = list(temp_extract.iterdir())
            if len(subdirs) == 1 and subdirs[0].is_dir():
                content_dir = subdirs[0]

            # Copy new files
            for item in content_dir.iterdir():
                dest = self.app_dir / item.name
                if item.is_file():
                    shutil.copy2(item, dest)
                elif item.is_dir():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(item, dest)

            # Cleanup
            shutil.rmtree(temp_extract)

            return True

        except Exception as e:
            print(f"Error installing from ZIP: {e}")
            # Try to restore backup
            if backup_dir.exists():
                for item in backup_dir.iterdir():
                    dest = self.app_dir / item.name
                    if item.is_file():
                        shutil.copy2(item, dest)
                    elif item.is_dir():
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)
            return False

    def check_git_repo(self) -> bool:
        """Check if app is running from a git repository"""
        git_dir = self.app_dir / '.git'
        return git_dir.exists()

    def update_via_git(self) -> Tuple[bool, str]:
        """Update via git pull (if in a git repo)"""
        try:
            if not self.check_git_repo():
                return False, "Not a git repository"

            # Stash local changes
            result = subprocess.run(['git', 'stash'],
                                  capture_output=True,
                                  text=True,
                                  cwd=str(self.app_dir))

            # Pull latest changes
            result = subprocess.run(['git', 'pull', 'origin', 'main'],
                                  capture_output=True,
                                  text=True,
                                  cwd=str(self.app_dir))

            if result.returncode == 0:
                return True, "Updated successfully via git"
            else:
                return False, result.stderr

        except FileNotFoundError:
            return False, "Git not installed"
        except Exception as e:
            return False, str(e)

    def restart_app(self):
        """Restart the application"""
        try:
            if self.is_frozen:
                # Restart executable
                subprocess.Popen([sys.executable])
            else:
                # Restart Python script
                subprocess.Popen([sys.executable] + sys.argv)

            # Exit current instance
            sys.exit(0)
        except Exception as e:
            print(f"Error restarting app: {e}")


class UpdateChecker(threading.Thread):
    """Background thread for checking updates"""

    def __init__(self, callback):
        super().__init__(daemon=True)
        self.callback = callback
        self.updater = UpdateManager()

    def run(self):
        """Check for updates in background"""
        update_info = self.updater.check_for_updates()
        if update_info and self.callback:
            self.callback(update_info)
