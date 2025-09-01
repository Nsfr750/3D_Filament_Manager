# Prerequisites for 3D Filament Manager

This document outlines the software and system requirements needed to develop and run the 3D Filament Manager application.

## System Requirements

### Operating Systems
- Windows 10/11 (64-bit)
- Linux (Ubuntu 20.04+ or equivalent)
- macOS 10.15 (Catalina) or later

### Hardware
- Minimum 4GB RAM (8GB recommended)
- At least 500MB free disk space
- Display with 1280x720 resolution or higher

## Required Software

### Python
- Python 3.8 or higher
  - [Download Python](https://www.python.org/downloads/)
  - Verify installation:
    ```bash
    python --version
    python -m pip --version
    ```

### Git
- Git for version control
  - [Download Git](https://git-scm.com/downloads)
  - Verify installation:
    ```bash
    git --version
    ```

### Virtual Environment
- Python's built-in `venv` module or `conda`
  - Verify venv is available:
    ```bash
    python -m venv --help
    ```

## Development Tools (Recommended)

### Code Editor/IDE
- [Visual Studio Code](https://code.visualstudio.com/) with Python extension
- [PyCharm Community/Professional](https://www.jetbrains.com/pycharm/)
- [Sublime Text](https://www.sublimetext.com/) with Python packages

### Version Control Clients
- [GitHub Desktop](https://desktop.github.com/)
- [SourceTree](https://www.sourcetreeapp.com/)
- [GitKraken](https://www.gitkraken.com/)

## Python Dependencies

### Required Packages
All required packages are listed in `requirements.txt`. Install them using:
```bash
pip install -r requirements.txt
```

### Development Dependencies
For development, install additional tools from `requirements-dev.txt`:
```bash
pip install -r requirements-dev.txt
```

## Optional Tools

### Database Management
- [DB Browser for SQLite](https://sqlitebrowser.org/) (if using SQLite)
- [DBeaver Community](https://dbeaver.io/) (for other databases)

### Documentation
- [Sphinx](https://www.sphinx-doc.org/) for documentation generation
- [MkDocs](https://www.mkdocs.org/) for project documentation

## Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Nsfr750/3D_Filament_Manager.git
   cd 3D_Filament_Manager
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

## Verifying the Setup

Run the test suite to verify everything is working:
```bash
pytest
```

## Troubleshooting

### Common Issues
- **Python not found**: Ensure Python is in your system PATH
- **Permission errors**: Use `sudo` on Linux/macOS or run as administrator on Windows
- **Dependency conflicts**: Use a fresh virtual environment

### Getting Help
- Check the [GitHub Issues](https://github.com/Nsfr750/3D_Filament_Manager/issues)
- Open a new issue if your problem isn't documented
