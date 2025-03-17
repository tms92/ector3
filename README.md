# Ecotr3

## Overview

Ecotr3 is a professional command-line tool for visualizing, analyzing, and managing directory structures. The name combines "directory" and "tree," reflecting the tool's purpose of providing hierarchical directory exploration with advanced capabilities.

## Key Features

- **Directory Visualization** (`ector3 print`): Generate a tree representation of directory structures with customizable depth
- **Statistical Analysis** (`--stats`): Obtain comprehensive metrics including file counts, directory depth, and file type distribution
- **Output Generation** (`ector3 create`): Save directory trees to text files for documentation and sharing
- **Clipboard Integration** (`ector3 copy`): Copy directory trees directly to clipboard for quick sharing
- **Exclusion Management** (`ector3 ignorefile`): Configure file/directory patterns to exclude from visualization

## Installation

### From PyPI (Recommended)

```bash
pip install ecotr3
From Source
bashCopiagit clone https://github.com/tms92/ecotr3.git
cd ecotr3
pip install .
Usage
Basic Directory Visualization
bashCopia# Display directory tree in terminal
ector3 print

# Limit tree depth to 2 levels
ector3 print --depth 2
Directory Analysis with Statistics
bashCopia# Display directory tree with detailed statistics
ector3 print --stats

# Combine depth limitation with statistics
ector3 print --stats --depth 3
Output and Sharing
bashCopia# Save directory tree to a text file
ector3 create

# Save directory tree with statistics to a text file
ector3 create --stats

# Copy directory tree to clipboard
ector3 copy
Exclusion Configuration
bashCopia# Create .e3ignore file template
ector3 ignorefile create
After creating the .e3ignore file, add patterns of files and directories you want to exclude:
Copia# Example .e3ignore file
node_modules/
*.log
__pycache__
.git/
Help Documentation
bashCopia# Display help information
ector3 help
Development Setup
Prerequisites

Python 3.7 or higher
Git

Setting Up Development Environment

Clone the repository:
bashCopiagit clone https://github.com/tms92/ecotr3.git
cd ecotr3

Install development dependencies:
bashCopiapip install -r requirements.txt

Install the package in development mode:
bashCopiapip install -e .


Running Tests
bashCopiapython -m pytest
Project Structure
Copiaecotr3/
│
├── src/                # Source code
│   ├── main.py         # CLI entry point
│   ├── tree_generator.py   # Directory tree generation
│   └── ignore_handler.py   # Exclusion pattern handling
│
├── tests/              # Test suite
│   └── test_*.py       # Test modules
│
├── setup.py            # Package configuration
├── requirements.txt    # Development dependencies
├── README.md           # Project documentation
└── .gitignore          # Git exclusion patterns
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

License
This project is licensed under the MIT License - see the LICENSE file for details.
Contact
Project Link: https://github.com/tms92/ecotr3