#!/usr/bin/env python3
"""
Additional tests for enhanced directory statistics functionality in Ecotr3
"""

import os
import sys
import tempfile
import shutil
import pytest

# Add the project root to Python path for importing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tree_generator import generate_directory_tree, calculate_directory_stats, format_size

class TestDirectoryStatistics:
    """Test class for enhanced directory statistics functionality"""

    @pytest.fixture
    def complex_temp_dir(self):
        """
        Create a temporary directory with a complex structure for testing.
        
        Yields:
            str: Path to the temporary directory
        """
        # Create a temporary directory
        test_dir = tempfile.mkdtemp()
        
        # Create a more complex structure for statistics testing
        os.makedirs(os.path.join(test_dir, 'src', 'modules'))
        os.makedirs(os.path.join(test_dir, 'docs', 'api'))
        os.makedirs(os.path.join(test_dir, 'tests', 'unit'))
        os.makedirs(os.path.join(test_dir, '.git'))
        os.makedirs(os.path.join(test_dir, 'build'))
        
        # Create various file types
        with open(os.path.join(test_dir, 'README.md'), 'w') as f:
            f.write('# Test Project\n' * 100)  # Make it have some size
            
        with open(os.path.join(test_dir, 'src', 'main.py'), 'w') as f:
            f.write('print("Hello World")\n' * 50)
            
        with open(os.path.join(test_dir, 'src', 'modules', 'helper.py'), 'w') as f:
            f.write('def helper(): pass\n' * 30)
            
        with open(os.path.join(test_dir, 'docs', 'index.html'), 'w') as f:
            f.write('<html><body>Documentation</body></html>\n' * 20)
            
        with open(os.path.join(test_dir, 'tests', 'test_main.py'), 'w') as f:
            f.write('def test_main(): assert True\n' * 25)
        
        yield test_dir
        
        # Clean up the temporary directory after test
        shutil.rmtree(test_dir)

    def test_calculate_directory_stats(self, complex_temp_dir):
        """Test directory statistics calculation"""
        ignore_patterns = ['.git', 'build']
        stats = calculate_directory_stats(complex_temp_dir, ignore_patterns)
        
        # Verify basic stats are calculated
        assert stats['file_count'] > 0
        assert stats['dir_count'] > 0
        assert stats['total_size'] > 0
        assert stats['max_depth'] >= 2
        
        # Verify extensions are tracked
        assert '.py' in stats['extensions']
        assert '.md' in stats['extensions']
        assert '.html' in stats['extensions']
        
        # Verify ignored directories aren't counted
        for entry in os.listdir(complex_temp_dir):
            if entry == '.git' or entry == 'build':
                path = os.path.join(complex_temp_dir, entry)
                # Create a file in the ignored directory to verify it's not counted
                with open(os.path.join(path, 'test.txt'), 'w') as f:
                    f.write('test')
        
        # Calculate stats again
        stats_after = calculate_directory_stats(complex_temp_dir, ignore_patterns)
        
        # The stats should be the same since we're ignoring .git and build
        assert stats['file_count'] == stats_after['file_count']
        assert stats['dir_count'] == stats_after['dir_count']

    def test_format_size(self):
        """Test size formatting function"""
        assert format_size(0) == "0 B"
        assert format_size(1023) == "1023 B"
        assert format_size(1024) == "1 KB"
        assert format_size(1536) == "1.5 KB"
        assert format_size(1048576) == "1 MB"
        assert format_size(1073741824) == "1 GB"
        assert format_size(1099511627776) == "1 TB"

    def test_tree_with_statistics(self, complex_temp_dir):
        """Test tree generation with statistics"""
        ignore_patterns = ['.git', 'build']
        
        # Generate tree without stats
        tree_without_stats = generate_directory_tree(
            complex_temp_dir, 
            ignore_patterns
        )
        
        # Generate tree with stats
        tree_with_stats = generate_directory_tree(
            complex_temp_dir, 
            ignore_patterns, 
            include_stats=True
        )
        
        # The tree with stats should be longer
        assert len(tree_with_stats) > len(tree_without_stats)
        
        # Check for statistics section
        assert "Directory Statistics:" in tree_with_stats
        assert "Total Files:" in tree_with_stats
        assert "Total Directories:" in tree_with_stats
        assert "Total Size:" in tree_with_stats
        assert "Top File Extensions:" in tree_with_stats
        
        # Verify that .py extension appears in the stats (should be common in our test data)
        assert ".py:" in tree_with_stats

    def test_tree_with_depth_limit(self, complex_temp_dir):
        """Test tree generation with depth limitation"""
        # Generate tree with depth limit 1
        tree_depth_1 = generate_directory_tree(
            complex_temp_dir, 
            max_depth=1,
            include_stats=True
        )
        
        # Generate tree with no depth limit
        tree_full = generate_directory_tree(
            complex_temp_dir, 
            include_stats=True
        )
        
        # The full tree should be longer
        assert len(tree_full) > len(tree_depth_1)
        
        # Depth-limited tree should still have statistics
        assert "Directory Statistics:" in tree_depth_1
        
        # The depth-limited tree should not contain files at level 3
        # For example, src/modules/helper.py should not be in the depth-limited tree
        assert "modules" in tree_depth_1  # Level 1 directory should be listed
        assert "helper.py" not in tree_depth_1  # But not its contents


if __name__ == '__main__':
    pytest.main([__file__])