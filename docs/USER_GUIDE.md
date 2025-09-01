# User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Main Interface](#main-interface)
3. [Filament Management](#filament-management)
4. [Backup & Restore](#backup--restore)
5. [Settings](#settings)
6. [Keyboard Shortcuts](#keyboard-shortcuts)

## Getting Started

### First Launch
When you first launch the 3D Filament Manager, it will create the necessary directories and configuration files in your user application data folder.

### Application Layout
The main window is divided into the following sections:
- **Menu Bar**: Access to all application features
- **Toolbar**: Quick access to common actions
- **Filament List**: Displays all your filaments in a sortable table
- **Status Bar**: Shows current status and statistics

## Main Interface

### Menu Options

#### File Menu
- **New Filament**: Add a new filament to your inventory
- **Import/Export**: Manage data import/export
- **Backup/Restore**: Create or restore backups
- **Exit**: Close the application

#### Edit Menu
- **Edit Selected**: Edit the currently selected filament
- **Delete Selected**: Remove the selected filament
- **Duplicate**: Create a copy of the selected filament

#### View Menu
- **Dark/Light Theme**: Toggle between dark and light themes
- **Language**: Change the application language
- **Refresh**: Update the filament list

## Filament Management

### Adding a New Filament
1. Click "New Filament" in the File menu or press `Ctrl+N`
2. Fill in the filament details:
   - Material type (PLA, ABS, PETG, etc.)
   - Color
   - Brand
   - Weight
   - Purchase date
   - Purchase price
   - Notes
3. Click "Save" to add the filament to your inventory

### Editing a Filament
1. Select a filament from the list
2. Click "Edit" or press `Ctrl+E`
3. Modify the desired fields
4. Click "Save" to apply changes

### Filtering and Sorting
- Use the search box to filter filaments by name, brand, or material
- Click on column headers to sort the list
- Use the filter options to show/hide specific filament types

## Backup & Restore

### Creating a Backup
1. Go to File > Backup/Restore > Create Backup
2. Choose a location to save the backup file
3. Click "Save"

### Restoring from Backup
1. Go to File > Backup/Restore > Restore Backup
2. Select a backup file (.bak)
3. Click "Open" to restore

## Settings

### Application Settings
Access settings via File > Settings

#### General
- **Default Unit System**: Choose between metric and imperial units
- **Auto-save**: Enable/disable auto-save
- **Check for Updates**: Configure update checking

#### Display
- **Theme**: Dark or Light
- **Language**: Application language
- **Date Format**: Choose your preferred date format

#### Backup
- **Auto-backup**: Enable/disable automatic backups
- **Backup Location**: Choose where to store backups
- **Max Backups**: Set maximum number of backups to keep

## Keyboard Shortcuts

### General
- `Ctrl+N`: New Filament
- `Ctrl+E`: Edit Selected
- `Delete`: Delete Selected
- `Ctrl+F`: Search
- `F5`: Refresh
- `F1`: Help
- `Alt+F4`: Exit

### Navigation
- `↑/↓`: Navigate through filaments
- `Home/End`: Jump to first/last filament
- `Page Up/Down`: Scroll through list

---

For additional help or to report issues, please visit our [GitHub repository](https://github.com/Nsfr750/3D_Filament_Manager).
