# 3D Filament Manager

![3D Filament Manager](assets/logo.png)

A desktop application for managing your 3D printing filament inventory. Keep track of materials, colors, usage, costs, and slicer settings in one place.

## ✨ Features

* **🌐 Multi-Language Support**: Available in English and Italian
* **🎨 Modern UI**: Clean interface with emoji icons and theme support (light/dark mode)
* **📊 Comprehensive Filament Management**:
  * Store detailed filament information (brand, material, color, diameter, etc.)
  * Track filament usage and remaining quantity
  * Calculate material costs
  * Price tracking and history
  * Interactive price analysis with visualizations
  * Vendor price comparison
* **⚙️ Slicer Integration**:
  * Save and manage slicer profiles (Cura, PrusaSlicer, eQuidiSlicer)
  * Custom print profiles for different printers
* **🔍 Advanced Search & Filtering**:
  * Search by any filament property
  * Sort by any column
  * Filter by material type, color, or custom tags
* **📂 Import/Export**:
  * Backup and restore your filament library
  * Share profiles with others
  * Bulk import/export support
* **🔒 Data Security**:
  * Settings saved in `config/` directory
  * No internet connection required
  * Local data storage

## 🚀 Requirements

* Python 3.8+
* Required packages (automatically installed):
  * `lxml` - Fast XML processing
  * `pillow` - Image processing for icons
  * `matplotlib` - Data visualization for price analysis

## 🛠️ Installation

### Prerequisites

* Python 3.8 or higher
* Git (optional, for development)

### Installation Steps

1. **Clone the repository** (or download as ZIP):

   ```bash
   git clone https://github.com/Nsfr750/3D_Filament_Manager.git
   cd 3D_Filament_Manager
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   python main.py
   ```

### Data Storage

* Filament profiles are stored in the `fdm/` directory
* Application settings are saved in the `config/` directory
* Logs are written to the `logs/` directory

## 🤝 Contributing

We welcome contributions! Here's how you can help:

* Report bugs by opening an [issue](https://github.com/Nsfr750/3D_Filament_Manager/issues)
* Suggest new features or improvements
* Submit pull requests with code changes
* Help improve documentation
* Translate the application to new languages

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
* Use type hints for better code clarity
* Write docstrings for all public functions and classes

## 📜 License

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.

## 🙏 Support

If you find this project useful, consider supporting its development:

* ⭐ Star the repository
* 🐛 Report issues
* 💡 Suggest new features
* 💰 [Sponsor the project on GitHub](https://github.com/sponsors/Nsfr750)

## 📞 Contact

* GitHub: [@Nsfr750](https://github.com/Nsfr750)
* Email: nsfr750@yandex.com

---

### Support the Developer

If you find this application useful, please consider supporting the developer:

* **PayPal**: [https://paypal.me/3dmega](https://paypal.me/3dmega)
* **GitHub**: [https://github.com/Nsfr750](https://github.com/Nsfr750)
