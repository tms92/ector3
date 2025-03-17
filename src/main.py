#!/usr/bin/env python3
"""
Main entry point for Ecotr3 - Directory Structure Visualization Tool

This module handles command-line interface and routing for Ecotr3 functionality.
"""

import argparse
import sys
import pyperclip  # For clipboard operations
import os

from .tree_generator import generate_directory_tree
from .ignore_handler import load_ignore_file

def print_directory_tree():
    """
    Print directory tree to console based on current directory and ignore rules.
    """
    ignore_patterns = load_ignore_file()
    tree = generate_directory_tree(os.getcwd(), ignore_patterns)
    print(tree)

def create_output_file():
    """
    Create an output file with directory tree representation.
    """
    ignore_patterns = load_ignore_file()
    tree = generate_directory_tree(os.getcwd(), ignore_patterns)
    
    # Generate filename based on current directory name
    current_dir_name = os.path.basename(os.getcwd())
    output_filename = f"{current_dir_name}_ecotr3.txt"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(tree)
        print(f"Directory tree saved to {output_filename}")
    except IOError as e:
        print(f"Error creating output file: {e}")
        sys.exit(1)

def copy_to_clipboard():
    """
    Copy directory tree to system clipboard.
    """
    ignore_patterns = load_ignore_file()
    tree = generate_directory_tree(os.getcwd(), ignore_patterns)
    
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
    help_text = """
Ecotr3 - Directory Structure Visualization Tool

Usage:
  ector3 print     - Display directory tree in console
  ector3 create    - Create output file with directory tree
  ector3 copy      - Copy directory tree to clipboard
  ector3 help      - Show this help information
  ector3 ignorefile create - Create .e3ignore configuration file

For more information, visit: https://github.com/tms92/ecotr3
"""
    print(help_text)

def main():
    """
    Main CLI entry point for Ecotr3.
    Parses arguments and routes to appropriate functions.
    """
    parser = argparse.ArgumentParser(description='Ecotr3 - Directory Structure Visualization Tool')
    parser.add_argument('command', nargs='?', default='help', 
                        choices=['print', 'create', 'copy', 'help', 'ignorefile'],
                        help='Command to execute')
    parser.add_argument('subcommand', nargs='?', help='Subcommand for specific actions')

    args = parser.parse_args()

    # Route to appropriate function based on command
    if args.command == 'print':
        print_directory_tree()
    elif args.command == 'create':
        create_output_file()
    elif args.command == 'copy':
        copy_to_clipboard()
    elif args.command == 'help':
        show_help()
    elif args.command == 'ignorefile':
        if args.subcommand == 'create':
            create_ignore_file()
        else:
            print("Invalid subcommand. Use 'ector3 ignorefile create'")

if __name__ == '__main__':
    main()