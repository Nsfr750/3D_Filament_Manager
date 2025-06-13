# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-13

### Added

- **Complete Application Rewrite**: Migrated from a single-file script to a modular, multi-file architecture for improved maintainability and scalability.
- **Full-Featured GUI**: Developed a new graphical user interface using Python's native `tkinter` library.
- **Filament List**: Implemented a `ttk.Treeview` to display all filament profiles with sortable columns.
- **Dynamic Filtering**: Added a search bar to filter the filament list in real-time.
- **Detailed View**: Created a tabbed panel to show detailed information and slicer settings for the selected filament.
- **CRUD Functionality**: Implemented "Add", "Edit", and "Delete" operations for filament profiles.
- **Import/Export**: Added functionality to import and export filament profiles as `.zip` archives.
- **Localization**: Integrated dual-language support for English and Italian.
- **Dialogs**: Created "About", "Help", and "Sponsor" dialogs.
- **Robust Logging**: Implemented comprehensive logging for debugging and error tracking.

### Fixed

- **Critical Edit Dialog Crash**: Resolved a `KeyError` that occurred when opening the "Edit Filament" dialog.
- **Blank Edit Dialog**: Fixed a bug where the edit dialog would open with empty fields.
- **Data Saving Errors**: Corrected multiple `KeyError` crashes that prevented filament edits from being saved.
- **Column Sorting**: Fixed and enhanced the sorting logic to work correctly for all columns, including numeric and text data.
- **Sponsor Dialog**: Ensured the sponsor dialog appears correctly when triggered from the menu.
- **UI Stability**: Addressed various minor bugs and data type mismatches to improve overall application stability.
