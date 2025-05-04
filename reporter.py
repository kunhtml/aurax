"""
Report generation for AuraX.
"""

import json
import os
import math
import shutil
import datetime
import tempfile
from typing import Dict, List, Tuple
from colorama import Fore, Style, Back, init
from rich.console import Console
from rich.table import Table
from jinja2 import Environment, FileSystemLoader
import pdfkit

from languages import LANGUAGES

# Initialize colorama
init(autoreset=True)

class Reporter:
    """
    Class for generating reports from line count data.
    """

    def __init__(self, results: Dict[str, Dict[str, int]]):
        """
        Initialize the Reporter.

        Args:
            results: The line count results
        """
        self.results = results
        self.meta = results.get('_meta', {})

    def get_color(self, language: str) -> str:
        """
        Get the color for a language.

        Args:
            language: The language name

        Returns:
            The ANSI color code
        """
        if language == 'Total':
            return Fore.WHITE + Style.BRIGHT

        color_name = LANGUAGES.get(language, {}).get('color', 'white')

        color_map = {
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE
        }

        return color_map.get(color_name, Fore.CYAN)

    def format_number(self, num: int, color_type: str = 'code') -> str:
        """
        Format a number with color based on its value and type.

        Args:
            num: The number to format
            color_type: The type of number ('code', 'comment', 'blank', 'percent')

        Returns:
            The formatted number string
        """
        if num == 0:
            return f"{Fore.BLACK}{num}"

        if color_type == 'code':
            return f"{Fore.GREEN}{num}"
        elif color_type == 'comment':
            return f"{Fore.YELLOW}{num}"
        elif color_type == 'blank':
            return f"{Fore.MAGENTA}{num}"
        elif color_type == 'percent':
            if num < 0.1:
                return f"{Fore.CYAN}{num:.2f}"
            elif num < 0.5:
                return f"{Fore.GREEN}{num:.2f}"
            elif num < 1.0:
                return f"{Fore.YELLOW}{num:.2f}"
            elif num < 3.0:
                return f"{Fore.MAGENTA}{num:.2f}"
            else:
                return f"{Fore.RED}{num:.2f}"
        else:
            return f"{Fore.WHITE}{num}"

    def format_percentage(self, percentage: float) -> str:
        """
        Format a percentage value.

        Args:
            percentage: The percentage value

        Returns:
            The formatted percentage string
        """
        return self.format_number(percentage, 'percent')

    def to_console(self, use_unicode: bool = True) -> None:
        """
        Print the results to the console using rich for aligned tables without horizontal lines.

        Args:
            use_unicode: Use Unicode characters for box borders if True, else use ASCII.
        """
        # Create console and table
        console = Console()
        table = Table(show_header=True, header_style="bold cyan", box=None, padding=(0, 2))

        # Add columns
        table.add_column("Language", style="cyan", justify="left")
        table.add_column("Files", style="white", justify="right")
        table.add_column("Code", style="green", justify="right")
        table.add_column("Comment", style="yellow", justify="right")
        table.add_column("Blank", style="magenta", justify="right")
        table.add_column("%", style="cyan", justify="right")

        # Sort languages by code lines (descending)
        sorted_languages = sorted(
            [lang for lang in self.results.keys() if lang not in ('_meta', 'Total')],
            key=lambda lang: self.results[lang]['code'],
            reverse=True
        )

        # Calculate total lines for percentage
        total_code = self.results.get('Total', {}).get('code', 0)

        # Add language rows
        for language in sorted_languages:
            if language == '_meta':
                continue

            data = self.results[language]

            # Calculate percentage of total code
            percentage = (data['code'] / total_code * 100) if total_code > 0 else 0

            # Format comment string for languages that don't support comments
            comment_str = (
                "N/A"
                if language in ['JSON', 'Markdown', 'Jinja2 Template']
                else str(data['comment'])
            )

            # Add row to table
            table.add_row(
                language,
                str(data['files']),
                str(data['code']),
                comment_str,
                str(data['blank']),
                f"{percentage:.2f}"
            )

        # Add total row
        if 'Total' in self.results:
            total_data = self.results['Total']
            table.add_row(
                "[bold]Total[/bold]",
                f"[bold white]{total_data['files']}[/bold white]",
                f"[bold green]{total_data['code']}[/bold green]",
                f"[bold yellow]{total_data['comment']}[/bold yellow]",
                f"[bold magenta]{total_data['blank']}[/bold magenta]",
                ""
            )

            # Add empty row as separator
            table.add_row("", "", "", "", "", "")

            # Add summary information
            project_size = total_data['total'] * 100 / 1024 / 1024
            language_count = len(sorted_languages)

            table.add_row("[bold cyan]Summary Information[/bold cyan]", "", "", "", "", "")
            table.add_row("[white][+] [green]Code[/green][/white]", "", f"[green]{total_data['code']:,} lines[/green]", "", "", "")
            table.add_row("[white][+] [yellow]Comments[/yellow][/white]", "", f"[yellow]{total_data['comment']:,} lines[/yellow]", "", "", "")
            table.add_row("[white][+] [magenta]Empty[/magenta][/white]", "", f"[magenta]{total_data['blank']:,} lines[/magenta]", "", "", "")
            table.add_row("[white][+] [cyan]Language(s) used[/cyan][/white]", "", f"[cyan]{language_count} language(s)[/cyan]", "", "", "")
            table.add_row("[white][+] [blue]Total Project Size[/blue][/white]", "", f"[blue]{project_size:.2f} MB[/blue]", "", "", "")

        # Print the table
        console.print(table)

        # Print performance metrics
        if self.meta:
            print(f"{Fore.GREEN}[INFO] Finished in {self.meta['elapsed_time']:.2f}s")

    def to_json(self, output_path: str) -> None:
        """
        Export the results to a JSON file.

        Args:
            output_path: Path to the output file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)

        print(f"Results exported to {output_path}")

    def to_markdown(self, output_path: str) -> None:
        """
        Export the results to a Markdown file.

        Args:
            output_path: Path to the output file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Code Analysis Report\n\n")

            # Write summary
            f.write("## Summary\n\n")
            f.write(f"- Total Files: {self.results['Total']['files']}\n")
            f.write(f"- Total Lines of Code: {self.results['Total']['code']}\n")
            f.write(f"- Total Comment Lines: {self.results['Total']['comment']}\n")
            f.write(f"- Total Blank Lines: {self.results['Total']['blank']}\n")
            f.write(f"- Total Lines: {self.results['Total']['total']}\n\n")

            # Write performance metrics
            if self.meta:
                f.write("## Performance\n\n")
                f.write(f"- Processing Time: {self.meta['elapsed_time']:.2f} seconds\n")
                f.write(f"- Files per Second: {self.meta['files_per_second']:.2f}\n")
                f.write(f"- Lines per Second: {self.meta['lines_per_second']:.2f}\n\n")

            # Write detailed table
            f.write("## Details\n\n")
            f.write("| Language | Files | Code | Comment | Blank | Total |\n")
            f.write("|----------|-------|------|---------|-------|-------|\n")

            # Sort languages by code lines (descending)
            sorted_languages = sorted(
                [lang for lang in self.results.keys() if lang not in ('_meta', 'Total')],
                key=lambda lang: self.results[lang]['code'],
                reverse=True
            )

            # Add language data
            for language in sorted_languages:
                if language == '_meta':
                    continue

                data = self.results[language]

                f.write(f"| {language} | {data['files']} | {data['code']} | {data['comment']} | {data['blank']} | {data['total']} |\n")

            # Add total row
            if 'Total' in self.results:
                total_data = self.results['Total']
                f.write(f"| **Total** | **{total_data['files']}** | **{total_data['code']}** | **{total_data['comment']}** | **{total_data['blank']}** | **{total_data['total']}** |\n")

        print(f"Results exported to {output_path}")

    def to_html(self, output_path: str) -> None:
        """
        Export the results to an HTML file with charts.

        Args:
            output_path: Path to the output file
        """
        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('report_template.html')

        # Sort languages by code lines (descending)
        sorted_languages = sorted(
            [lang for lang in self.results.keys() if lang not in ('_meta', 'Total')],
            key=lambda lang: self.results[lang]['code'],
            reverse=True
        )

        # Prepare data for the template
        languages_data = {}
        for language in sorted_languages:
            if language == '_meta':
                continue
            languages_data[language] = self.results[language]

        # Get version from utils
        from utils import get_version

        # Render the template
        html_content = template.render(
            languages=languages_data,
            total=self.results.get('Total', {}),
            meta=self.meta,
            version=get_version(),
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML report exported to {output_path}")

    def to_pdf(self, output_path: str) -> None:
        """
        Export the results to a PDF file with charts.

        Args:
            output_path: Path to the output file
        """
        # First generate HTML content
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('report_template.html')

        # Sort languages by code lines (descending)
        sorted_languages = sorted(
            [lang for lang in self.results.keys() if lang not in ('_meta', 'Total')],
            key=lambda lang: self.results[lang]['code'],
            reverse=True
        )

        # Prepare data for the template
        languages_data = {}
        for language in sorted_languages:
            if language == '_meta':
                continue
            languages_data[language] = self.results[language]

        # Get version from utils
        from utils import get_version

        # Render the template
        html_content = template.render(
            languages=languages_data,
            total=self.results.get('Total', {}),
            meta=self.meta,
            version=get_version(),
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        # Create a temporary HTML file
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as temp_html:
            temp_html_path = temp_html.name
            temp_html.write(html_content)

        try:
            # Convert HTML to PDF using pdfkit
            options = {
                'quiet': '',
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': 'UTF-8',
                'no-outline': None,
                'enable-local-file-access': None
            }

            try:
                # Try to convert HTML to PDF
                pdfkit.from_file(temp_html_path, output_path, options=options)
                print(f"PDF report exported to {output_path}")
            except OSError as e:
                # If wkhtmltopdf is not installed, inform the user
                print(f"Error generating PDF: {e}")
                print("To generate PDF reports, you need to install wkhtmltopdf:")
                print("1. Download from: https://wkhtmltopdf.org/downloads.html")
                print("2. Add the installation directory to your PATH")
                print("3. Try again")

                # Save HTML as fallback
                html_fallback_path = output_path.replace('.pdf', '.html')
                with open(html_fallback_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"HTML report saved as fallback to {html_fallback_path}")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_html_path):
                os.unlink(temp_html_path)
