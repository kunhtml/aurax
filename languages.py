"""
Language definitions and detection for AuraX.
"""

from typing import Dict, List, Tuple, Set
import os
import re

# Define language specifications
# Format: 'language_name': {'extensions': ['.ext1', '.ext2'], 'line_comment': '//', 'block_comment': [('/*', '*/')]}
LANGUAGES: Dict[str, Dict] = {
    'Python': {
        'extensions': ['.py', '.pyw', '.pyx', '.pxd', '.pxi'],
        'line_comment': '#',
        'block_comment': [('"""', '"""'), ("'''", "'''")],
        'color': 'blue'
    },
    'JavaScript': {
        'extensions': ['.js', '.jsx', '.mjs'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'yellow'
    },
    'TypeScript': {
        'extensions': ['.ts', '.tsx'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'cyan'
    },
    'Java': {
        'extensions': ['.java'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'red'
    },
    'C': {
        'extensions': ['.c', '.h'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'green'
    },
    'C++': {
        'extensions': ['.cpp', '.cc', '.cxx', '.hpp', '.hh', '.hxx'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'green'
    },
    'C#': {
        'extensions': ['.cs'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'magenta'
    },
    'Go': {
        'extensions': ['.go'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'cyan'
    },
    'Rust': {
        'extensions': ['.rs'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'red'
    },
    'Ruby': {
        'extensions': ['.rb', '.rake', '.gemspec'],
        'line_comment': '#',
        'block_comment': [('=begin', '=end')],
        'color': 'red'
    },
    'PHP': {
        'extensions': ['.php', '.phtml', '.php3', '.php4', '.php5', '.php7', '.phps'],
        'line_comment': '//',
        'block_comment': [('/*', '*/'), ('<!--', '-->')],
        'color': 'magenta'
    },
    'Swift': {
        'extensions': ['.swift'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'red'
    },
    'Kotlin': {
        'extensions': ['.kt', '.kts'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'magenta'
    },
    'HTML': {
        'extensions': ['.html', '.htm', '.xhtml'],
        'line_comment': None,
        'block_comment': [('<!--', '-->')],
        'color': 'yellow'
    },
    'CSS': {
        'extensions': ['.css'],
        'line_comment': None,
        'block_comment': [('/*', '*/')],
        'color': 'blue'
    },
    'SCSS': {
        'extensions': ['.scss'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'magenta'
    },
    'LESS': {
        'extensions': ['.less'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'magenta'
    },
    'XML': {
        'extensions': ['.xml', '.svg', '.xsl', '.xslt', '.xsd', '.dtd'],
        'line_comment': None,
        'block_comment': [('<!--', '-->')],
        'color': 'yellow'
    },
    'JSON': {
        'extensions': ['.json'],
        'line_comment': None,
        'block_comment': None,
        'color': 'yellow'
    },
    'YAML': {
        'extensions': ['.yaml', '.yml'],
        'line_comment': '#',
        'block_comment': None,
        'color': 'yellow'
    },
    'Markdown': {
        'extensions': ['.md', '.markdown'],
        'line_comment': None,
        'block_comment': None,
        'color': 'white'
    },
    'Shell': {
        'extensions': ['.sh', '.bash', '.zsh', '.ksh'],
        'line_comment': '#',
        'block_comment': None,
        'color': 'green'
    },
    'PowerShell': {
        'extensions': ['.ps1', '.psm1', '.psd1'],
        'line_comment': '#',
        'block_comment': [('<#', '#>')],
        'color': 'blue'
    },
    'Batch': {
        'extensions': ['.bat', '.cmd'],
        'line_comment': 'REM',
        'block_comment': None,
        'color': 'green'
    },
    'SQL': {
        'extensions': ['.sql'],
        'line_comment': '--',
        'block_comment': [('/*', '*/')],
        'color': 'cyan'
    },
    'Perl': {
        'extensions': ['.pl', '.pm', '.t'],
        'line_comment': '#',
        'block_comment': [('=pod', '=cut')],
        'color': 'blue'
    },
    'Lua': {
        'extensions': ['.lua'],
        'line_comment': '--',
        'block_comment': [('--[[', ']]')],
        'color': 'blue'
    },
    'Haskell': {
        'extensions': ['.hs', '.lhs'],
        'line_comment': '--',
        'block_comment': [('{-', '-}')],
        'color': 'magenta'
    },
    'R': {
        'extensions': ['.r', '.R'],
        'line_comment': '#',
        'block_comment': None,
        'color': 'blue'
    },
    'Dart': {
        'extensions': ['.dart'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'cyan'
    },
    'Groovy': {
        'extensions': ['.groovy', '.gradle'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'green'
    },
    'Scala': {
        'extensions': ['.scala', '.sc'],
        'line_comment': '//',
        'block_comment': [('/*', '*/')],
        'color': 'red'
    },
    'Elixir': {
        'extensions': ['.ex', '.exs'],
        'line_comment': '#',
        'block_comment': None,
        'color': 'magenta'
    },
    'Clojure': {
        'extensions': ['.clj', '.cljs', '.cljc', '.edn'],
        'line_comment': ';;',
        'block_comment': None,
        'color': 'cyan'
    },
}

# Create a mapping from file extension to language
EXTENSION_TO_LANGUAGE = {}
for language, specs in LANGUAGES.items():
    for ext in specs['extensions']:
        EXTENSION_TO_LANGUAGE[ext] = language

def detect_language(file_path: str) -> str:
    """
    Detect the programming language of a file based on its extension.

    Args:
        file_path: Path to the file

    Returns:
        The detected language name or 'Unknown'
    """
    _, ext = os.path.splitext(file_path.lower())
    return EXTENSION_TO_LANGUAGE.get(ext, 'Unknown')

def get_language_specs(language: str) -> Dict:
    """
    Get the specifications for a language.

    Args:
        language: The language name

    Returns:
        A dictionary with language specifications
    """
    return LANGUAGES.get(language, {
        'line_comment': None,
        'block_comment': None,
        'color': 'white'
    })

def get_supported_languages() -> List[str]:
    """
    Get a list of all supported languages.

    Returns:
        A list of language names
    """
    return list(LANGUAGES.keys())

def get_supported_extensions() -> List[str]:
    """
    Get a list of all supported file extensions.

    Returns:
        A list of file extensions
    """
    return list(EXTENSION_TO_LANGUAGE.keys())

def is_binary_file(file_path: str) -> bool:
    """
    Check if a file is binary.

    Args:
        file_path: Path to the file

    Returns:
        True if the file is binary, False otherwise
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk
    except Exception:
        return False

def load_custom_languages(config_path: str) -> None:
    """
    Load custom language definitions from a configuration file.

    Args:
        config_path: Path to the configuration file
    """
    # This would be implemented to load custom language definitions
    # from a JSON or YAML configuration file
    pass
