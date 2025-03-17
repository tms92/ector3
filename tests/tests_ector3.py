#!/usr/bin/env python3
"""
Test suite for Ecotr3 - Directory Structure Visualization Tool

This module contains unit and integration tests for verifying 
the functionality of the Ecotr3 tool.
"""

import os
import sys
import tempfile
import shutil
import pytest

# Add the project root to Python path for importing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tree_generator import generate_directory_tree, should_ignore
from src.ignore_handler import load_ignore_file, validate_ignore_pattern, is_path_ignored

class TestEcotr3:
    """
    Comprehensive test class for Ecotr3 functionality.
    """

    @pytest.fixture
    def temp_dir(self):
        """
        Create a temporary directory for testing.
        
        Yields:
            str: Path to the temporary directory
        """
        # Create a temporary directory
        test_dir = tempfile.mkdtemp()
        yield test_dir
        
        # Clean up the temporary directory after test
        shutil.rmtree(test_dir)

    def create_test_structure(self, temp_dir):
        """
        Create a sample directory structure for testing.
        
        Args:
            temp_dir (str): Base directory to create test structure in
        """
        # Create sample directory structure
        os.makedirs(os.path.join(temp_dir, 'src'))
        os.makedirs(os.path.join(temp_dir, 'tests'))
        os.makedirs(os.path.join(temp_dir, '.git'))
        
        # Create some sample files
        with open(os.path.join(temp_dir, 'README.md'), 'w') as f:
            f.write('# Ecotr3 Project')
        
        with open(os.path.join(temp_dir, 'src', 'main.py'), 'w') as f:
            f.write('# Main application entry point')
        
        with open(os.path.join(temp_dir, 'tests', 'test_file.py'), 'w') as f:
            f.write('# Test file')

    def test_generate_directory_tree(self, temp_dir):
        """
        Test directory tree generation functionality.
        """
        # Create test directory structure
        self.create_test_structure(temp_dir)
        
        # Generate directory tree
        ignore_patterns = ['.git', '__pycache__']
        tree = generate_directory_tree(temp_dir, ignore_patterns)
        
        # Assertions
        assert os.path.basename(temp_dir) in tree
        assert 'src' in tree
        assert 'tests' in tree
        assert 'README.md' in tree
        assert '.git' not in tree  # Should be ignored

    def test_should_ignore(self, temp_dir):
        """
        Test ignore pattern matching functionality.
        """
        ignore_patterns = [
            '*.log', 
            '.git', 
            '__pycache__'
        ]
        
        # Test various paths
        assert should_ignore(os.path.join(temp_dir, '.git'), ignore_patterns) == True
        assert should_ignore(os.path.join(temp_dir, 'app.log'), ignore_patterns) == True
        assert should_ignore(os.path.join(temp_dir, 'src', 'main.py'), ignore_patterns) == False

    def test_load_ignore_file(self, temp_dir):
        """
        Test loading of ignore file with custom and default patterns.
        """
        # Create a sample .e3ignore file
        ignore_file_path = os.path.join(temp_dir, '.e3ignore')
        with open(ignore_file_path, 'w') as f:
            f.write("# Custom ignore patterns\n")
            f.write("*.tmp\n")
            f.write("build/\n")
        
        # Load ignore patterns
        os.chdir(temp_dir)
        ignore_patterns = load_ignore_file()
        
        # Assertions
        assert '*.tmp' in ignore_patterns
        assert 'build/' in ignore_patterns
        assert '.git' in ignore_patterns  # Default patterns
        assert '__pycache__' in ignore_patterns  # Default patterns

    def test_validate_ignore_pattern(self):
        """
        Test conversion of glob patterns to regex.
        """
        # Test various pattern conversions
        assert validate_ignore_pattern('*.py') is not None
        assert validate_ignore_pattern('.git/') is not None
        assert validate_ignore_pattern('# Comment') is None
        assert validate_ignore_pattern('') is None

    def test_is_path_ignored(self):
        """
        Test path ignore logic.
        """
        ignore_patterns = [
            '*.log', 
            '.git/', 
            'build/'
        ]
        
        # Test various paths
        assert is_path_ignored('app.log', ignore_patterns) == True
        assert is_path_ignored('.git/config', ignore_patterns) == True
        assert is_path_ignored('build/test.txt', ignore_patterns) == True
        assert is_path_ignored('src/main.py', ignore_patterns) == False

def main():
    """
    Run tests if script is executed directly.
    """
    pytest.main([__file__])

if __name__ == '__main__':
    main()