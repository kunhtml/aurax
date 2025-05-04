"""
Core counting logic for AuraX.
"""

import os
import re
from typing import Dict, List, Tuple, Set, Generator
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm

from languages import detect_language, get_language_specs, is_binary_file

class LineCounter:
    """
    Class for counting lines of code, comments, and blank lines in files.
    """

    def __init__(self, exclude_dirs: List[str] = None, exclude_files: List[str] = None):
        """
        Initialize the LineCounter.

        Args:
            exclude_dirs: List of directory names to exclude
            exclude_files: List of file patterns to exclude
        """
        self.exclude_dirs = exclude_dirs or ['node_modules', 'dist', 'build', 'venv', '.git', '__pycache__']
        self.exclude_files = exclude_files or []
        self.exclude_patterns = [re.compile(pattern) for pattern in self.exclude_files]

    def should_exclude(self, path: str) -> bool:
        """
        Check if a path should be excluded.

        Args:
            path: The path to check

        Returns:
            True if the path should be excluded, False otherwise
        """
        # Check if the path contains any excluded directory
        for excluded_dir in self.exclude_dirs:
            if f'/{excluded_dir}/' in path.replace('\\', '/') or path.replace('\\', '/').endswith(f'/{excluded_dir}'):
                return True

        # Check if the file matches any excluded pattern
        filename = os.path.basename(path)
        for pattern in self.exclude_patterns:
            if pattern.match(filename):
                return True

        return False

    def find_files(self, path: str) -> Generator[str, None, None]:
        """
        Find all files in a directory recursively.

        Args:
            path: The directory path

        Yields:
            Paths to files
        """
        if os.path.isfile(path):
            if not self.should_exclude(path):
                yield path
        else:
            for root, dirs, files in os.walk(path):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if d not in self.exclude_dirs]

                for file in files:
                    file_path = os.path.join(root, file)
                    if not self.should_exclude(file_path) and not is_binary_file(file_path):
                        yield file_path

    def count_lines(self, file_path: str) -> Dict[str, int]:
        """
        Count lines of code, comments, and blank lines in a file.

        Args:
            file_path: Path to the file

        Returns:
            A dictionary with counts of code, comments, and blank lines
        """
        language = detect_language(file_path)
        if language == 'Unknown':
            return {
                'language': 'Unknown',
                'code': 0,
                'comment': 0,
                'blank': 0,
                'total': 0
            }

        specs = get_language_specs(language)
        line_comment = specs.get('line_comment')
        block_comments = specs.get('block_comment', [])

        code_lines = 0
        comment_lines = 0
        blank_lines = 0

        in_block_comment = False
        current_block_comment_end = None

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()

                    # Check for blank lines
                    if not line:
                        blank_lines += 1
                        continue

                    # Handle block comments
                    if in_block_comment:
                        comment_lines += 1
                        if current_block_comment_end in line:
                            in_block_comment = False
                            # Check if there's code after the end of the block comment
                            end_pos = line.find(current_block_comment_end) + len(current_block_comment_end)
                            code_after_comment = line[end_pos:].strip()
                            if code_after_comment and not (line_comment and code_after_comment.startswith(line_comment)):
                                code_lines += 1
                            current_block_comment_end = None
                        continue

                    # Check for the start of block comments
                    block_comment_started = False
                    for start, end in block_comments or []:
                        if start in line:
                            comment_lines += 1
                            block_comment_started = True
                            # Check if the block comment ends on the same line
                            start_pos = line.find(start) + len(start)
                            if end in line[start_pos:]:
                                # Check if there's code after the end of the block comment
                                end_pos = line.find(end, start_pos) + len(end)
                                code_after_comment = line[end_pos:].strip()
                                if code_after_comment and not (line_comment and code_after_comment.startswith(line_comment)):
                                    code_lines += 1
                            else:
                                in_block_comment = True
                                current_block_comment_end = end
                            break

                    if block_comment_started:
                        continue

                    # Check for line comments
                    if line_comment and line.startswith(line_comment):
                        comment_lines += 1
                        continue

                    # If we've reached here, it's a line of code
                    code_lines += 1
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return {
                'language': language,
                'code': 0,
                'comment': 0,
                'blank': 0,
                'total': 0
            }

        return {
            'language': language,
            'code': code_lines,
            'comment': comment_lines,
            'blank': blank_lines,
            'total': code_lines + comment_lines + blank_lines
        }

    def count_directory(self, path: str, num_workers: int = 8) -> Dict[str, Dict[str, int]]:
        """
        Count lines in all files in a directory.

        Args:
            path: The directory path
            num_workers: Number of worker threads

        Returns:
            A dictionary with counts per language
        """
        start_time = time.time()
        files = list(self.find_files(path))

        results = {}
        total_files = len(files)

        print(f"Found {total_files} files to analyze")

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            with tqdm(total=total_files, desc="Counting lines", unit="file") as pbar:
                future_to_file = {executor.submit(self.count_lines, file): file for file in files}

                for future in future_to_file:
                    result = future.result()
                    language = result['language']

                    if language not in results:
                        results[language] = {
                            'files': 0,
                            'code': 0,
                            'comment': 0,
                            'blank': 0,
                            'total': 0
                        }

                    results[language]['files'] += 1
                    results[language]['code'] += result['code']
                    results[language]['comment'] += result['comment']
                    results[language]['blank'] += result['blank']
                    results[language]['total'] += result['total']

                    pbar.update(1)

        # Calculate totals
        totals = {
            'files': sum(lang_data['files'] for lang_data in results.values()),
            'code': sum(lang_data['code'] for lang_data in results.values()),
            'comment': sum(lang_data['comment'] for lang_data in results.values()),
            'blank': sum(lang_data['blank'] for lang_data in results.values()),
            'total': sum(lang_data['total'] for lang_data in results.values())
        }

        results['Total'] = totals

        elapsed_time = time.time() - start_time
        results['_meta'] = {
            'elapsed_time': elapsed_time,
            'files_per_second': total_files / elapsed_time if elapsed_time > 0 else 0,
            'lines_per_second': totals['total'] / elapsed_time if elapsed_time > 0 else 0
        }

        return results
