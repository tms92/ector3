#!/usr/bin/env python3
"""
Enhanced Tree Generator module for Ecotr3 - Directory Structure Visualization Tool

This module provides functionality to generate a text-based tree representation
of directory structures with advanced statistics, supporting file exclusion patterns.
"""

import os
import fnmatch
from collections import defaultdict


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


def calculate_directory_stats(directory, ignore_patterns=None):
    """
    Calculate directory statistics recursively.

    Args:
        directory (str): Directory to analyze
        ignore_patterns (list, optional): Patterns of files/directories to ignore

    Returns:
        dict: Statistics including file count, directory count, total size, etc.
    """
    stats = defaultdict(int)
    stats['max_depth'] = 0
    stats['extensions'] = defaultdict(int)
    
    def _analyze_directory(current_dir, current_depth=0):
        # Update max depth
        stats['max_depth'] = max(stats['max_depth'], current_depth)
        
        try:
            entries = os.listdir(current_dir)
        except (PermissionError, FileNotFoundError):
            return
            
        for entry in entries:
            full_path = os.path.join(current_dir, entry)
            
            # Skip ignored entries
            if ignore_patterns and should_ignore(full_path, ignore_patterns):
                continue
                
            if os.path.isdir(full_path):
                stats['dir_count'] += 1
                _analyze_directory(full_path, current_depth + 1)
            else:
                stats['file_count'] += 1
                try:
                    stats['total_size'] += os.path.getsize(full_path)
                    # Track file extensions
                    _, ext = os.path.splitext(entry)
                    if ext:
                        stats['extensions'][ext.lower()] += 1
                except (OSError, FileNotFoundError):
                    pass
    
    _analyze_directory(directory)
    return stats


def format_size(size_bytes):
    """
    Format size in bytes to human-readable format.

    Args:
        size_bytes (int): Size in bytes

    Returns:
        str: Human-readable size string (e.g., "4.2 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024 or unit == 'TB':
            return f"{size_bytes:.2f} {unit}".rstrip('0').rstrip('.') + ' ' + unit
        size_bytes /= 1024


def generate_directory_tree(root_dir, ignore_patterns=None, max_depth=None, include_stats=False):
    """
    Generate a text representation of the directory tree with optional statistics.

    Args:
        root_dir (str): Root directory to start generating the tree from
        ignore_patterns (list, optional): Patterns of files/directories to ignore
        max_depth (int, optional): Maximum depth of directory traversal
        include_stats (bool, optional): Whether to include directory statistics

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

    # Statistics for the directory structure
    stats = None
    if include_stats:
        stats = calculate_directory_stats(root_dir, ignore_patterns)

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

    # Append statistics if requested
    if include_stats and stats:
        tree_lines.append("\n" + "=" * 40)
        tree_lines.append("Directory Statistics:")
        tree_lines.append(f"Total Files: {stats['file_count']}")
        tree_lines.append(f"Total Directories: {stats['dir_count']}")
        tree_lines.append(f"Maximum Depth: {stats['max_depth']}")
        tree_lines.append(f"Total Size: {format_size(stats['total_size'])}")
        
        # Add most common file extensions
        if stats['extensions']:
            tree_lines.append("\nTop File Extensions:")
            sorted_extensions = sorted(
                stats['extensions'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]  # Show top 5 extensions
            
            for ext, count in sorted_extensions:
                tree_lines.append(f"  {ext}: {count} files")

    # Convert tree lines to a single string
    return '\n'.join(tree_lines)

# Optional: If script is run directly, demonstrate functionality
if __name__ == '__main__':
    print(generate_directory_tree(os.getcwd(), include_stats=True))