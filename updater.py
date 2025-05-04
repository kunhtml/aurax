"""
Online update functionality for AuraX.
"""

import os
import sys
import requests
import json
import shutil
from typing import Dict, Tuple, Optional

class Updater:
    """
    Class for handling online updates of the AuraX tool.
    """

    def __init__(self, current_version: str, repo_url: str = "https://api.github.com/repos/yourusername/aurax"):
        """
        Initialize the Updater.

        Args:
            current_version: The current version of the tool
            repo_url: The GitHub repository API URL
        """
        self.current_version = current_version
        self.repo_url = repo_url

    def check_for_updates(self) -> Tuple[bool, Optional[str]]:
        """
        Check if updates are available.

        Returns:
            A tuple of (update_available, latest_version)
        """
        try:
            response = requests.get(f"{self.repo_url}/releases/latest")
            response.raise_for_status()

            release_data = response.json()
            latest_version = release_data.get('tag_name', '').lstrip('v')

            if not latest_version:
                return False, None

            # Compare versions
            current_parts = [int(p) for p in self.current_version.split('.')]
            latest_parts = [int(p) for p in latest_version.split('.')]

            # Pad with zeros if needed
            while len(current_parts) < len(latest_parts):
                current_parts.append(0)
            while len(latest_parts) < len(current_parts):
                latest_parts.append(0)

            for current, latest in zip(current_parts, latest_parts):
                if latest > current:
                    return True, latest_version
                elif current > latest:
                    return False, latest_version

            return False, latest_version

        except Exception as e:
            print(f"Error checking for updates: {e}")
            return False, None

    def update(self) -> bool:
        """
        Update the tool to the latest version.

        Returns:
            True if the update was successful, False otherwise
        """
        update_available, latest_version = self.check_for_updates()

        if not update_available:
            print(f"You are already using the latest version ({self.current_version})")
            return False

        print(f"Updating from version {self.current_version} to {latest_version}...")

        try:
            # Get the download URL for the latest release
            response = requests.get(f"{self.repo_url}/releases/latest")
            response.raise_for_status()

            release_data = response.json()
            assets = release_data.get('assets', [])

            download_url = None
            for asset in assets:
                if asset.get('name', '').endswith('.py') or asset.get('name', '').endswith('.exe'):
                    download_url = asset.get('browser_download_url')
                    break

            if not download_url:
                print("Could not find download URL for the latest version")
                return False

            # Download the latest version
            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            # Determine the output path
            if getattr(sys, 'frozen', False):
                # Running as a bundled executable
                output_path = sys.executable
                backup_path = f"{output_path}.bak"

                # Create a backup of the current executable
                shutil.copy2(output_path, backup_path)

                # Write the new executable
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"Update successful! Backup saved to {backup_path}")

            else:
                # Running as a Python script
                script_path = os.path.abspath(sys.argv[0])
                backup_path = f"{script_path}.bak"

                # Create a backup of the current script
                shutil.copy2(script_path, backup_path)

                # Write the new script
                with open(script_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"Update successful! Backup saved to {backup_path}")

            return True

        except Exception as e:
            print(f"Error updating: {e}")
            return False
