# Ecotr3

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

Ecotr3 is a professional command-line tool for visualizing, analyzing, and managing directory structures. The name combines "directory" and "tree," reflecting the tool's purpose of providing hierarchical directory exploration with advanced capabilities.

Designed for developers, system administrators, and power users, Ecotr3 offers a comprehensive solution for understanding complex file systems, documenting project structures, and sharing directory layouts with precision and clarity.

## Key Features

- **Directory Visualization** (`ector3 print`): Generate a tree representation of directory structures with customizable depth
- **Statistical Analysis** (`--stats`): Obtain comprehensive metrics including file counts, directory depth, total size, and file type distribution
- **Output Generation** (`ector3 create`): Save directory trees to text files for documentation and sharing
- **Clipboard Integration** (`ector3 copy`): Copy directory trees directly to system clipboard for quick sharing
- **Exclusion Management** (`ector3 ignorefile`): Configure file/directory patterns to exclude from visualization using glob patterns

## Installation

### From PyPI (Recommended)

```bash
pip install ecotr3
```

### From Source

```bash
git clone https://github.com/tms92/ecotr3.git
cd ecotr3
pip install .
```

## System Requirements

- Python 3.7 or higher
- External dependency: `pyperclip` (for clipboard operations)

## Usage Guide

### Basic Directory Visualization

```bash
# Display directory tree in terminal
ector3 print

# Limit tree depth to 2 levels
ector3 print --depth 2
```

### Directory Analysis with Statistics

```bash
# Display directory tree with detailed statistics
ector3 print --stats

# Combine depth limitation with statistics
ector3 print --stats --depth 3
```

### Output and Sharing

```bash
# Save directory tree to a text file
ector3 create

# Save directory tree with statistics to a text file
ector3 create --stats

# Copy directory tree to clipboard
ector3 copy
```

### Exclusion Configuration

```bash
# Create .e3ignore file template
ector3 ignorefile create
```

After creating the `.e3ignore` file, add patterns of files and directories you want to exclude:

```
# Example .e3ignore file
node_modules/
*.log
__pycache__
.git/
```

### Help Documentation

```bash
# Display help information
ector3 help
```

## Detailed Feature Documentation

### Directory Tree Generation

The core `generate_directory_tree` function supports:
- Visual representation with appropriate branching symbols (├── and └──)
- Efficient handling of deeply nested directories
- Depth limiting for complex structures
- Alphabetical sorting of files and directories
- Proper handling of permissions and inaccessible directories

### Exclusion System

The ignore pattern management system implements:
- Automatic loading of patterns from `.e3ignore`
- Default patterns for common elements (.git, *.pyc, etc.)
- Support for glob patterns (wildcards * and ?)
- Efficient conversion of glob patterns to regular expressions
- Validation of user-supplied patterns

### Directory Statistics

The statistical analysis module provides:
- Accurate file and directory counting (excluding ignored items)
- Total size calculation with human-readable formatting
- Maximum tree depth tracking
- File type distribution analysis by extension
- Sorted presentation of most common extensions

## Project Structure

```
ecotr3/
│
├── src/                # Source code
│   ├── main.py         # CLI entry point
│   ├── tree_generator.py   # Directory tree generation
│   └── ignore_handler.py   # Exclusion pattern handling
│
├── tests/              # Test suite
│   ├── tests_ector3.py    # Core tests
│   └── tests_directory_statistics.py  # Statistics functionality tests
│
├── setup.py            # Package configuration
├── requirements.txt    # Development dependencies
└── README.md           # Project documentation
```

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git

### Setting Up Development Environment

Clone the repository:
```bash
git clone https://github.com/tms92/ecotr3.git
cd ecotr3
```

Install development dependencies:
```bash
pip install -r requirements.txt
```

Install the package in development mode:
```bash
pip install -e .
```

### Running Tests

```bash
python -m pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

When contributing, please:
- Follow the existing code style
- Add tests for new functionality
- Update documentation to reflect your changes
- Ensure all tests pass before submitting

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Project Link: [https://github.com/tms92/ecotr3](https://github.com/tms92/ecotr3)

---

*Ecotr3: Explore your directories with clarity and insight.*