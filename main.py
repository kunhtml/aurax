#!/usr/bin/env python3
"""
AuraX: A fast, cross-platform tool for counting lines of code.
"""

import os
import sys
import time
from colorama import init, Fore, Style

from counter import LineCounter
from reporter import Reporter
from updater import Updater
from utils import parse_arguments, get_version, print_version, is_valid_path
from config import Config
from languages import load_custom_languages, get_supported_languages

def main():
    """
    Main entry point for AuraX.
    """
    # Initialize colorama
    init()

    # Parse command-line arguments
    args = parse_arguments()

    # Show version information
    if args.version:
        print_version()
        return 0

    # Update the tool
    if args.update:
        updater = Updater(get_version())
        updater.update()
        return 0

    # Load configuration
    config = Config()

    # Load custom languages
    custom_languages_path = os.path.expanduser('~/.aurax-languages.json')
    if os.path.exists(custom_languages_path):
        load_custom_languages(custom_languages_path)

    # Check if the path exists
    if not is_valid_path(args.path):
        print(f"{Fore.RED}Error: Path '{args.path}' does not exist{Style.RESET_ALL}")
        return 1

    # Parse exclude directories
    exclude_dirs = args.exclude.split(',') if args.exclude else []

    # Parse exclude file patterns
    exclude_files = args.exclude_files.split(',') if args.exclude_files else []

    # Create the line counter
    counter = LineCounter(exclude_dirs=exclude_dirs, exclude_files=exclude_files)

    # Count lines
    print(f"{Fore.CYAN}Analyzing '{args.path}'...{Style.RESET_ALL}")
    results = counter.count_directory(args.path, num_workers=args.workers)

    # Create the reporter
    reporter = Reporter(results)

    # Generate the report
    if args.format == 'console':
        reporter.to_console()
    elif args.format == 'json':
        output_path = f"{args.output}.json"
        reporter.to_json(output_path)
    elif args.format == 'md':
        output_path = f"{args.output}.md"
        reporter.to_markdown(output_path)

    return 0

if __name__ == '__main__':
    sys.exit(main())
