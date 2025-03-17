# Ecotr3

## Overview

Ecotr3 is an innovative command-line tool for visualizing, managing, and navigating directory structures. The name is a wordplay merging "director" (folder) and "tree", reflecting the tool's nature of directory exploration.

## Prerequisites

- Python 3.7+
- pip

## Installation

```bash
pip install ecotr3
```

## Features

- **Directory Visualization** (`ector3 print`): Generates a tree representation of the current directory structure
- **Output File Creation** (`ector3 create`): Generates a text file with the directory tree representation
- **Clipboard Copy** (`ector3 copy`): Copies the textual representation of the directory tree to the clipboard
- **Support and Documentation** (`ector3 help`): Provides a quick usage guide
- **Exclusion File Management** (`ector3 ignorefile create`): Allows specifying files and folders to exclude

## Usage Examples

### Basic Usage

```bash
# Display directory structure
ector3 print

# Create output file with directory tree
ector3 create

# Copy directory structure to clipboard
ector3 copy
```

### Ignore File Configuration

Create a `.e3ignore` file to exclude specific files or directories:

```bash
# Create .e3ignore file
ector3 ignorefile create
```

Example `.e3ignore` contents:
```
# Ignore node modules
node_modules/

# Ignore log files
*.log

# Ignore specific directories
.git/
__pycache__/
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature-name`)
5. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/tms92/ecotr3.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest
```

## License

[To be defined - Placeholder for license information]

## Contact

[Insert contact information or project maintainer details]