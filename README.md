# AuraX

A fast, cross-platform, and portable tool for counting lines of code in software projects.

## Features

- **Cross-platform**: Works on Windows, macOS, and Linux
- **Portable**: Single file executable with no additional dependencies
- **Fast**: Processes over 1 million lines of code in under 5 seconds
- **Comprehensive**: Supports ~103 programming languages, extensible via configuration
- **Open Source**: Contribute, fork, or create pull requests to add features
- **Online Updates**: Update the tool directly from the command line
- **Multiple Report Formats**: Export results in JSON, Markdown, HTML with interactive charts, and PDF
- **Convenient Shorthand Commands**: Use `--html` and `--pdf` flags for quick report generation
- **Beautiful CLI**: Attractive and intuitive command-line interface

## Installation

```bash
# Clone the repository
git clone https://github.com/kunhtml/aurax.git
cd aurax

# Install dependencies
pip install -r requirements.txt

# Run the tool
python main.py [OPTIONS] [PATH]
```

## Usage

```bash
# Count lines in the current directory
python main.py .

# Count lines in a specific directory
python main.py /path/to/project

# Export results to JSON
python main.py /path/to/project --format json --output results.json

# Export results to Markdown
python main.py /path/to/project --format md --output results.md

# Export results to HTML with interactive charts (full syntax)
python main.py /path/to/project --format html --output results.html

# Export results to HTML with interactive charts (shorthand)
python main.py /path/to/project --html

# Export results to PDF (shorthand)
python main.py /path/to/project --pdf

# Exclude specific directories
python main.py /path/to/project --exclude node_modules,dist,build

# Update the tool
python main.py --update
```

## Report Formats

AuraX supports multiple report formats to help you analyze and share your code statistics:

### Console Output

The default output format displays results directly in your terminal with color-coded information and a clean, easy-to-read layout.

### JSON

Export detailed results to a JSON file for further processing or integration with other tools:

```bash
python main.py /path/to/project --format json --output results.json
```

### Markdown

Generate a well-formatted Markdown report that can be easily included in documentation or GitHub READMEs:

```bash
python main.py /path/to/project --format md --output results.md
```

### HTML with Interactive Charts

Create a beautiful HTML report with interactive charts for visualizing your codebase:

```bash
# Full syntax
python main.py /path/to/project --format html --output results.html

# Shorthand syntax
python main.py /path/to/project --html
```

The HTML report includes:

- Detailed tables with code statistics
- Interactive pie charts showing language distribution
- Breakdown of code, comment, and blank lines
- Performance metrics
- Responsive design that works on all devices

### PDF Reports

Generate professional PDF reports that can be easily shared and printed:

```bash
# Full syntax
python main.py /path/to/project --format pdf --output results.pdf

# Shorthand syntax
python main.py /path/to/project --pdf
```

The PDF report contains the same information as the HTML report but in a format suitable for printing and sharing with stakeholders who may not have access to a web browser.

> **Note:** PDF generation requires [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) to be installed on your system. If not installed, AuraX will save an HTML report as a fallback.

## Supported Languages

AuraX supports approximately 103 programming languages out of the box, including:

- Python
- JavaScript/TypeScript
- Java
- C/C++
- C#
- Go
- Rust
- Ruby
- PHP
- Swift
- Kotlin
- And many more...

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
