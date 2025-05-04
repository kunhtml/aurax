"""
Configuration handling for AuraX.
"""

import os
import json
from typing import Dict, List, Any, Optional

class Config:
    """
    Class for handling configuration settings.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Config.

        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path or os.path.expanduser('~/.aurax.json')
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.

        Returns:
            The configuration dictionary
        """
        if not os.path.exists(self.config_path):
            return self.get_default_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Merge with default config to ensure all keys exist
            default_config = self.get_default_config()
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value

            return config

        except Exception as e:
            print(f"Error loading configuration: {e}")
            return self.get_default_config()

    def save_config(self) -> bool:
        """
        Save configuration to file.

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)

            return True

        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False

    def get_default_config(self) -> Dict[str, Any]:
        """
        Get the default configuration.

        Returns:
            The default configuration dictionary
        """
        return {
            'exclude_dirs': ['node_modules', 'dist', 'build', 'venv', '.git', '__pycache__'],
            'exclude_files': [],
            'num_workers': 8,
            'default_format': 'console',
            'custom_languages': {}
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: The configuration key
            default: The default value if the key doesn't exist

        Returns:
            The configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: The configuration key
            value: The configuration value
        """
        self.config[key] = value
        self.save_config()

    def get_exclude_dirs(self) -> List[str]:
        """
        Get the list of directories to exclude.

        Returns:
            The list of directories
        """
        return self.get('exclude_dirs', [])

    def get_exclude_files(self) -> List[str]:
        """
        Get the list of file patterns to exclude.

        Returns:
            The list of file patterns
        """
        return self.get('exclude_files', [])

    def get_num_workers(self) -> int:
        """
        Get the number of worker threads.

        Returns:
            The number of worker threads
        """
        return self.get('num_workers', 8)

    def get_custom_languages(self) -> Dict[str, Dict[str, Any]]:
        """
        Get custom language definitions.

        Returns:
            The custom language definitions
        """
        return self.get('custom_languages', {})
