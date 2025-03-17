#!/usr/bin/env python3
"""
Ignore Handler module for Ecotr3 - Directory Structure Visualization Tool

This module provides functionality to load and process .e3ignore configuration files,
allowing users to specify files and directories to exclude from tree view.
"""

import os
import re

def load_ignore_file(ignore_filename='.e3ignore'):
    """
    Load and parse the .e3ignore configuration file.

    Args:
        ignore_filename (str, optional): Path to the ignore file. 
                                         Defaults to '.e3ignore' in current directory.

    Returns:
        list: A list of ignore patterns
    """
    # Default ignore patterns if no ignore file exists
    default_ignore_patterns = [
        '.git',         # Git directory
        '__pycache__',  # Python cache directory
        '*.pyc',        # Compiled Python files
        '*.log',        # Log files
        '.DS_Store',    # macOS system files
    ]

    # If no custom ignore file exists, return default patterns
    if not os.path.exists(ignore_filename):
        return default_ignore_patterns

    try:
        with open(ignore_filename, 'r', encoding='utf-8') as f:
            # Read lines, strip whitespace, and filter out comments and empty lines
            ignore_patterns = [
                line.strip() 
                for line in f 
                if line.strip() and not line.strip().startswith('#')
            ]

        # Combine default and custom ignore patterns
        return default_ignore_patterns + ignore_patterns

    except IOError as e:
        # If there's an error reading the file, log it and return default patterns
        print(f"Warning: Could not read {ignore_filename}. Using default ignore patterns.")
        print(f"Error details: {e}")
        return default_ignore_patterns

def validate_ignore_pattern(pattern):
    """
    Validate and potentially convert a glob-style ignore pattern to a regex pattern.

    Args:
        pattern (str): Ignore pattern to validate

    Returns:
        str: Validated regex pattern
    """
    # Remove leading/trailing whitespace
    pattern = pattern.strip()

    # Ignore empty or comment lines
    if not pattern or pattern.startswith('#'):
        return None

    # Convert glob pattern to regex
    # Escape special regex characters except * and ?
    regex_pattern = re.escape(pattern)
    
    # Replace escaped * with .*
    regex_pattern = regex_pattern.replace(r'\*', '.*')
    
    # Replace escaped ? with a single character wildcard
    regex_pattern = regex_pattern.replace(r'\?', '.')
    
    # If pattern ends with /, it's a directory pattern
    if pattern.endswith('/'):
        regex_pattern += '.*'

    return f'^{regex_pattern}$'

def is_path_ignored(path, ignore_patterns):
    """
    Check if a given path should be ignored based on ignore patterns.

    Args:
        path (str): Full path to check
        ignore_patterns (list): List of ignore patterns

    Returns:
        bool: True if path should be ignored, False otherwise
    """
    # Normalize the path (remove leading ./ or .\ if present)
    normalized_path = path.lstrip('./\\')

    for pattern in ignore_patterns:
        # Convert glob pattern to regex
        regex_pattern = validate_ignore_pattern(pattern)
        
        if regex_pattern:
            # Check if the path matches the pattern
            if re.match(regex_pattern, normalized_path, re.IGNORECASE):
                return True

    return False

# Optional: If script is run directly, demonstrate functionality
if __name__ == '__main__':
    # Example usage
    current_ignore_patterns = load_ignore_file()
    print("Current ignore patterns:")
    for pattern in current_ignore_patterns:
        print(f"- {pattern}")