#!/usr/bin/env python3
"""
Main entry point for Ecotr3 - Directory Structure Visualization Tool

This module handles command-line interface and routing for Ecotr3 functionality.
"""

import argparse
import sys
try:
    import pyperclip  # For clipboard operations
except ImportError:
    print("Warning: pyperclip module not found. Clipboard functionality will be disabled.")
    print("Please install it using: pip install pyperclip")
    pyperclip = None
import os

from .tree_generator import generate_directory_tree
from .ignore_handler import load_ignore_file

def print_directory_tree(stats=False, max_depth=None):
    """
    Print directory tree to console based on current directory and ignore rules.
    
    Args:
        stats (bool): Whether to include directory statistics
        max_depth (int, optional): Maximum depth of directory traversal
    """
    ignore_patterns = load_ignore_file()
    tree = generate_directory_tree(
        os.getcwd(), 
        ignore_patterns, 
        max_depth=max_depth,
        include_stats=stats
    )
    print(tree)

def create_output_file(stats=False, max_depth=None):
    """
    Create an output file with directory tree representation.
    
    Args:
        stats (bool): Whether to include directory statistics
        max_depth (int, optional): Maximum depth of directory traversal
    """
    ignore_patterns = load_ignore_file()
    tree = generate_directory_tree(
        os.getcwd(), 
        ignore_patterns, 
        max_depth=max_depth,
        include_stats=stats
    )
    
    # Generate filename based on current directory name
    current_dir_name = os.path.basename(os.getcwd())
    stats_suffix = "_with_stats" if stats else ""
    output_filename = f"{current_dir_name}_ecotr3{stats_suffix}.txt"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(tree)
        print(f"Directory tree saved to {output_filename}")
    except IOError as e:
        print(f"Error creating output file: {e}")
        sys.exit(1)

def copy_to_clipboard(stats=False, max_depth=None):
    """
    Copy directory tree to system clipboard.
    
    Args:
        stats (bool): Whether to include directory statistics
        max_depth (int, optional): Maximum depth of directory traversal
    """
    if pyperclip is None:
        print("Error: pyperclip module is required for clipboard functionality.")
        print("Please install it using: pip install pyperclip")
        sys.exit(1)
    
    ignore_patterns = load_ignore_file()
    tree = generate_directory_tree(
        os.getcwd(), 
        ignore_patterns, 
        max_depth=max_depth,
        include_stats=stats
    )
    
    try:
        pyperclip.copy(tree)
        print("Directory tree copied to clipboard")
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        sys.exit(1)

def create_ignore_file():
    """
    Create .e3ignore configuration file.
    """
    ignore_filename = '.e3ignore'
    
    if os.path.exists(ignore_filename):
        print(f"{ignore_filename} already exists. Skipping creation.")
        return
    
    try:
        with open(ignore_filename, 'w', encoding='utf-8') as f:
            f.write("# Ecotr3 Ignore File\n")
            f.write("# Add files and directories to exclude from tree view\n")
            f.write("\n# Example entries:\n")
            f.write("# .git\n")
            f.write("# node_modules/\n")
            f.write("# *.log\n")
        print(f"{ignore_filename} created successfully")
    except IOError as e:
        print(f"Error creating {ignore_filename}: {e}")
        sys.exit(1)

def show_help():
    """
    Display help information for Ecotr3.
    """
    version = get_version()
    help_text = f"""
Ecotr3 - Directory Structure Visualization Tool (v{version})

Usage:
  ector3 print [--stats] [--depth DEPTH]  - Display directory tree in console
  ector3 create [--stats] [--depth DEPTH] - Create output file with directory tree
  ector3 copy [--stats] [--depth DEPTH]   - Copy directory tree to clipboard
  ector3 help                             - Show this help information
  ector3 ignorefile create                - Create .e3ignore configuration file

Options:
  --stats          - Include directory statistics (file count, size, etc.)
  --depth DEPTH    - Limit directory traversal to specified depth

For more information, visit: https://github.com/tms92/ecotr3
"""
    print(help_text)

def get_version():
    """
    Reads the version from the VERSION file.
    
    Returns:
        str: The current version of the application
    """
    # Try multiple possible locations for the VERSION file
    possible_paths = [
        # Current directory
        'VERSION',
        # One directory up (package root when installed)
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION'),
        # Two directories up (package root during development)
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'VERSION'),
        # Absolute path from package directory
        os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'VERSION')
    ]

    for path in possible_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                version = f.read().strip()
                return version
        except (IOError, FileNotFoundError):
            continue
            
    return "unknown"

def main():
    """
    Main CLI entry point for Ecotr3.
    Parses arguments and routes to appropriate functions.
    """
    parser = argparse.ArgumentParser(description='Ecotr3 - Directory Structure Visualization Tool')
    parser.add_argument('command', nargs='?', default='help', 
                        choices=['print', 'create', 'copy', 'help', 'ignorefile', 'version'],
                        help='Command to execute')
    parser.add_argument('subcommand', nargs='?', help='Subcommand for specific actions')
    parser.add_argument('--stats', action='store_true', help='Include directory statistics')
    parser.add_argument('--depth', type=int, help='Maximum depth of directory traversal')

    args = parser.parse_args()

    # Route to appropriate function based on command
    if args.command == 'print':
        print_directory_tree(stats=args.stats, max_depth=args.depth)
    elif args.command == 'create':
        create_output_file(stats=args.stats, max_depth=args.depth)
    elif args.command == 'copy':
        copy_to_clipboard(stats=args.stats, max_depth=args.depth)
    elif args.command == 'help':
        show_help()
    elif args.command == 'version':
        print(f"Ecotr3 version {get_version()}")
    elif args.command == 'ignorefile':
        if args.subcommand == 'create':
            create_ignore_file()
        else:
            print("Invalid subcommand. Use 'ector3 ignorefile create'")