# AuraX

A fast, cross-platform, and portable tool for counting lines of code in software projects.

## Features

- **Cross-platform**: Works on Windows, macOS, and Linux
- **Portable**: Single file executable with no additional dependencies
- **Fast**: Processes over 1 million lines of code in under 5 seconds
- **Comprehensive**: Supports ~103 programming languages, extensible via configuration
- **Open Source**: Contribute, fork, or create pull requests to add features
- **Online Updates**: Update the tool directly from the command line
- **Multiple Report Formats**: Export results in JSON and Markdown formats
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

# Exclude specific directories
python main.py /path/to/project --exclude node_modules,dist,build

# Update the tool
python main.py --update
```

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
