# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-08-25

### Added in v1.2.0

* **Price Analysis**: Added interactive price analysis with visualizations
* **Price Tracking**: Implemented price history tracking for filaments
* **Vendor Comparison**: Added vendor price comparison chart
* **Price Statistics**: Added price statistics (min, max, avg, trend)
* **Time Range Filtering**: Added time-based filtering for price history

### Changed in v1.2.0

* **Dependencies**: Added matplotlib for data visualization
* **UI**: Enhanced price tracker dialog with new analysis features
* **Documentation**: Updated README with new features and requirements

## [1.1.1] - 2025-08-24

### Fixed in v1.1.1

* **Backup Dialog**: Fixed theme initialization error when opening backup management
* **Italian Localization**: Added missing translations for backup dialog strings
* **Error Handling**: Improved error handling in backup management

## [1.1.0] - 2025-08-24

### Added in v1.1.0

* **Enhanced UI**: Added emoji icons to menu items for better visual feedback
* **Improved Settings**: All settings are now saved in the `config/` directory
* **Dark/Light Theme Toggle**: Added a theme toggle with appropriate icons

### Changed in v1.1.0

* **Code Quality**: Improved code organization and removed unused dependencies
* **Dependencies**: Updated and optimized project dependencies
* **Documentation**: Updated README and CHANGELOG with latest changes

### Fixed in v1.1.0

* **Menu System**: Fixed menu implementation to use standard Tkinter Menu
* **Settings Persistence**: Ensured settings are properly saved and loaded

## [1.0.0] - 2025-06-13

### Added in v1.0.0

* **Complete Application Rewrite**: Migrated from a single-file script to a modular, multi-file architecture for improved maintainability and scalability.
* **Full-Featured GUI**: Developed a new graphical user interface using Python's native `tkinter` library.
* **Filament List**: Implemented a `ttk.Treeview` to display all filament profiles with sortable columns.
* **Dynamic Filtering**: Added a search bar to filter the filament list in real-time.
* **Detailed View**: Created a tabbed panel to show detailed information and slicer settings for the selected filament.
* **CRUD Functionality**: Implemented "Add", "Edit", and "Delete" operations for filament profiles.
* **Import/Export**: Added functionality to import and export filament profiles as `.zip` archives.
* **Localization**: Integrated dual-language support for English and Italian.
* **Dialogs**: Created "About", "Help", and "Sponsor" dialogs.
* **Robust Logging**: Implemented comprehensive logging for debugging and error tracking.

### Fixed in v1.0.0

* **Critical Edit Dialog Crash**: Resolved a `KeyError` that occurred when opening the "Edit Filament" dialog.
* **Blank Edit Dialog**: Fixed a bug where the edit dialog would open with empty fields.
* **Data Saving Errors**: Corrected multiple `KeyError` crashes that prevented filament edits from being saved.
* **Column Sorting**: Fixed and enhanced the sorting logic to work correctly for all columns, including numeric and text data.
* **Sponsor Dialog**: Ensured the sponsor dialog appears correctly when triggered from the menu.
* **UI Stability**: Addressed various minor bugs and data type mismatches to improve overall application stability.
