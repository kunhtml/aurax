"""
Utility functions for AuraX.
"""

import os
import sys
import argparse
from typing import List, Dict, Any

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        The parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='AuraX: A fast, cross-platform tool for counting lines of code',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to the directory or file to analyze'
    )

    parser.add_argument(
        '--exclude',
        type=str,
        default='node_modules,dist,build,venv,.git,__pycache__',
        help='Comma-separated list of directories to exclude'
    )

    parser.add_argument(
        '--exclude-files',
        type=str,
        default='',
        help='Comma-separated list of file patterns to exclude'
    )

    parser.add_argument(
        '--format',
        type=str,
        choices=['console', 'json', 'md'],
        default='console',
        help='Output format'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='aurax-report',
        help='Output file path (without extension)'
    )

    parser.add_argument(
        '--workers',
        type=int,
        default=8,
        help='Number of worker threads'
    )

    parser.add_argument(
        '--update',
        action='store_true',
        help='Update AuraX to the latest version'
    )

    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information'
    )

    return parser.parse_args()

def get_version() -> str:
    """
    Get the current version of AuraX.

    Returns:
        The version string
    """
    return '1.0.0'

def print_version() -> None:
    """
    Print version information.
    """
    version = get_version()
    print(f"AuraX v{version}")
    print("A fast, cross-platform tool for counting lines of code")
    print("https://github.com/yourusername/aurax")

def is_valid_path(path: str) -> bool:
    """
    Check if a path exists.

    Args:
        path: The path to check

    Returns:
        True if the path exists, False otherwise
    """
    return os.path.exists(path)

def format_number(num: int) -> str:
    """
    Format a number with thousands separators.

    Args:
        num: The number to format

    Returns:
        The formatted number string
    """
    return f"{num:,}"

def format_time(seconds: float) -> str:
    """
    Format a time duration.

    Args:
        seconds: The time in seconds

    Returns:
        The formatted time string
    """
    if seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} s"
    else:
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes} m {seconds:.2f} s"
