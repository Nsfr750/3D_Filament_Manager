# Contributing to 3D Filament Manager

First off, thank you for considering contributing to 3D Filament Manager! It's people like you that make this project great.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs
- Ensure the bug was not already reported by searching on GitHub under [Issues](https://github.com/Nsfr750/3D_Filament_Manager/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/Nsfr750/3D_Filament_Manager/issues/new). Be sure to include:
  - A clear and descriptive title
  - Steps to reproduce the issue
  - Expected vs. actual behavior
  - Screenshots if applicable
  - Your operating system and Python version

### Suggesting Enhancements
- Open a new issue with the enhancement suggestion
- Clearly describe the feature and why it would be useful
- Include any relevant examples or mockups

### Pull Requests
1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

### Prerequisites
See [PREREQUISITES.md](PREREQUISITES.md) for required software and setup instructions.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Nsfr750/3D_Filament_Manager.git
   cd 3D_Filament_Manager
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

### Testing
- Run tests: `pytest`
- Run with coverage: `pytest --cov=src tests/`

### Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for better code documentation
- Keep lines under 88 characters (Black formatter default)

## Commit Message Guidelines
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Reference issues and pull requests liberally

## License
By contributing, you agree that your contributions will be licensed under its GNU General Public License v3.0.
