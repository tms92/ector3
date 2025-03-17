#!/usr/bin/env python3
"""
Tree Generator module for Ecotr3 - Directory Structure Visualization Tool

This module provides functionality to generate a text-based tree representation
of directory structures, with support for ignoring specific files and directories.
"""

import os
import fnmatch

def should_ignore(path, ignore_patterns):
    """
    Check if a file or directory should be ignored based on ignore patterns.

    Args:
        path (str): Path to the file or directory to check
        ignore_patterns (list): List of ignore patterns

    Returns:
        bool: True if the path should be ignored, False otherwise
    """
    # Get the base name of the path
    base_name = os.path.basename(path)

    # Check against each ignore pattern
    for pattern in ignore_patterns:
        # Support both file/directory names and path patterns
        if fnmatch.fnmatch(base_name, pattern) or fnmatch.fnmatch(path, pattern):
            return True
    
    return False

def generate_directory_tree(root_dir, ignore_patterns=None, max_depth=None):
    """
    Generate a text representation of the directory tree.

    Args:
        root_dir (str): Root directory to start generating the tree from
        ignore_patterns (list, optional): Patterns of files/directories to ignore
        max_depth (int, optional): Maximum depth of directory traversal

    Returns:
        str: Formatted text representation of the directory tree
    """
    # Initialize default ignore patterns if not provided
    if ignore_patterns is None:
        ignore_patterns = [
            '.git', 
            '__pycache__', 
            '*.pyc', 
            '*.log', 
            '.DS_Store'
        ]

    # Normalize the root directory path
    root_dir = os.path.abspath(root_dir)
    
    # Tree output will be built in this list
    tree_lines = [os.path.basename(root_dir)]

    def _generate_tree(directory, prefix='', depth=0):
        """
        Recursive helper function to generate tree structure.

        Args:
            directory (str): Current directory being processed
            prefix (str): Prefix for current tree level (for formatting)
            depth (int): Current depth in the directory tree
        """
        # Check if max depth is reached
        if max_depth is not None and depth > max_depth:
            return

        # Get sorted list of entries, excluding ignored items
        try:
            entries = sorted(os.listdir(directory))
        except PermissionError:
            # Skip directories we can't access
            return
        except FileNotFoundError:
            # Skip if directory no longer exists
            return

        # Count of processed entries to manage last item formatting
        processed_entries = 0
        total_valid_entries = sum(
            1 for entry in entries 
            if not should_ignore(os.path.join(directory, entry), ignore_patterns)
        )

        for entry in entries:
            full_path = os.path.join(directory, entry)

            # Skip ignored entries
            if should_ignore(full_path, ignore_patterns):
                continue

            # Determine tree branching symbols
            processed_entries += 1
            is_last = processed_entries == total_valid_entries
            branch = '└── ' if is_last else '├── '
            new_prefix = prefix + ('    ' if is_last else '│   ')

            # Add the entry to tree lines
            tree_lines.append(f"{prefix}{branch}{entry}")

            # Recursively process subdirectories
            if os.path.isdir(full_path):
                _generate_tree(full_path, new_prefix, depth + 1)

    # Start generating tree from root directory
    _generate_tree(root_dir)

    # Convert tree lines to a single string
    return '\n'.join(tree_lines)

# Optional: If script is run directly, demonstrate functionality
if __name__ == '__main__':
    print(generate_directory_tree(os.getcwd()))