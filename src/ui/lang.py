"""
Multilingual support for the 3D Filament Manager application.

This module provides internationalization (i18n) capabilities, allowing the application
to be displayed in multiple languages. It includes:
- Built-in translations for English and Italian
- Support for adding new languages
- Persistent language preference storage
- Simple translation function (tr) for UI strings

The module automatically loads the user's language preference from a config file
and falls back to English if the requested language is not available.
"""

import json
import os

LANGUAGES = {
    'en': {
        # Main Window
        'title': '3D Filament Manager',
        'file': 'File',
        'view': 'View',
        'dark_mode': 'Dark Mode',
        'language': 'Language',
        'reload_filaments': 'Reload Filaments',
        'help': 'Help',
        'import_filaments': 'Import Filaments',
        'export_filaments': 'Export Filaments',
        'exit': 'Exit',
        'about': 'About',
        'filter_placeholder': 'Filter by brand, material, or color...',
        'search_label': 'Search:',
        'add_filament': 'Add Filament',
        'edit_filament': 'Edit Filament',
        'delete_filament': 'Delete Filament',
        'details_title': 'Details',
        'properties_title': 'Properties',
        'slicer_settings': 'Slicer Settings',
        'tools': 'Tools',
        'price_tracker': 'Price Tracker',
        'barcode_utility': 'Barcode Utility',

        # Treeview Columns
        'col_brand': 'Brand',
        'col_material': 'Material',
        'col_color': 'Color',
        'col_remaining': 'Remaining (%)',
        'col_cost': 'Cost (€/kg)',
        'col_diameter': 'Diameter (mm)',
        'col_density': 'Density (g/cm³)',
        'col_initial_qty': 'Initial Qty (g)',
        'col_spool_weight': 'Spool W. (g)',
        'col_print_temp': 'Print T. (°C)',
        'col_bed_temp': 'Bed T. (°C)',
        'col_max_flow': 'Max F. (mm³/s)',
        'col_filename': 'Filename',

        # Details Panel
        'detail_brand': 'Brand',
        'detail_material': 'Material',
        'detail_color': 'Color',
        'detail_description': 'Description',
        'detail_diameter': 'Diameter',
        'detail_density': 'Density',
        'detail_initial_qty': 'Initial Quantity',
        'detail_spool_weight': 'Spool Weight',
        'detail_cost': 'Cost',
        'detail_cost_per_kg': 'Cost per Kg',
        'detail_cost_per_meter': 'Cost per Meter',
        'detail_remaining': 'Remaining',
        'detail_remaining_qty': 'Remaining Quantity',
        'detail_last_used': 'Last Used',
        'detail_slicer_settings': 'Slicer Settings',
        'detail_notes': 'Notes',

        # Add/Edit Dialog
        'add_dialog_title': 'Add New Filament',
        'edit_dialog_title': 'Edit Filament',
        'label_brand': 'Brand',
        'label_material': 'Material',
        'label_color': 'Color',
        'label_diameter': 'Diameter (mm)',
        'label_density': 'Density (g/cm³)',
        'label_initial_qty': 'Initial Quantity (g)',
        'label_spool_weight': 'Spool Weight (g)',
        'label_cost': 'Cost (€/kg)',
        'label_slicer_settings': 'Slicer Settings',
        'label_notes': 'Notes',
        'apply': 'Apply',
        'cancel': 'Cancel',

        # Dialogs & Messages
        'app_title': '3D Filament Manager',
        'about_description': 'A simple tool to manage 3D printing filaments.',
        'created_by': 'Created by',
        'help_dialog_title': 'Help',
        'about_dialog_title': 'About 3D Filament Manager',
        'version': 'Version',
        'author': 'Author',
        'confirm_deletion_title': 'Confirm Deletion',
        'confirm_deletion_msg': 'Are you sure you want to delete this filament?',
        'error_title': 'Error',
        'no_filament_selected_msg': 'No filament selected.',
        'save_error_msg': 'Could not save filament.',
        'import_success_title': 'Import Successful',
        'import_success_msg': 'Filaments imported successfully.',
        'export_success_title': 'Export Successful',
        'export_success_msg': 'Filaments exported successfully.',
        'import_error_title': 'Import Error',
        'import_error_msg': 'Failed to import filaments.',
        'export_error_title': 'Export Error',
        'export_error_msg': 'Failed to export filaments.',
        'delete_error_msg': 'Failed to delete filament.',
        'import_zip_title': 'Import from Zip',
        'export_zip_title': 'Export to Zip',
        'select_zip_title': 'Select ZIP file',
        'select_zip_prompt': 'Select ZIP file to import',
        'save_zip_title': 'Save ZIP file',
        'save_zip_prompt': 'Save filaments as ZIP',
        'language_change_title': 'Language Change',
        'language_change_msg': 'Language has been changed. Please restart the application for the changes to take full effect.',
        'not_available': 'N/A',
        'never': 'Never',
        'no_slicer_settings': 'No specific slicer settings.',

        # Help Dialog
        'help_title': 'How to use the Filament Manager:',
        'help_main_list': 'The main list shows all your filament profiles.',
        'help_sort': 'Click column headers to sort.',
        'help_search': 'Use the search box to filter filaments.',
        'help_select': 'Select a filament to see its details on the right.',
        'help_add': 'Use \'Add New\' to create a new filament profile.',
        'help_edit': 'Select a filament and click \'Edit Selected\' to modify it.',
        'help_import_export': 'Use File > Import/Export to backup or restore your filament library from a .zip file.',

        # Error Messages
        'no_filament_selected_title': 'No Selection',
        'no_filament_selected_msg': 'Please select a filament from the list.',

        # Backup Dialog
        'backup': 'Backup',
        'create_backup': 'Create Backup',
        'restore_backup': 'Restore Backup',
        'manage_backups': 'Manage Backups',
        'backup_created': 'Backup created successfully!',
        'backup_restored': 'Backup restored successfully!',
        'backup_failed': 'Failed to create backup',
        'restore_failed': 'Failed to restore backup',
        'no_backups': 'No backups available',
        'backup_list': 'Available Backups',
        'backup_date': 'Backup Date',
        'backup_size': 'Size',
        'backup_actions': 'Actions',
        'restore': 'Restore',
        'delete': 'Delete',
        'close': 'Close',
        'automatic_backups': 'Automatic Backups',
        'backup_frequency': 'Backup Frequency',
        'max_backups': 'Maximum Backups',
        'include_logs': 'Include Logs',
        'backup_on_startup': 'Backup on Startup',
        'backup_on_exit': 'Backup on Exit',
        'backup_now': 'Backup Now',
        'select_backup': 'Select Backup to Restore',
        'confirm_restore': 'Are you sure you want to restore this backup? All current data will be replaced!',
        'confirm_delete': 'Are you sure you want to delete this backup? This action cannot be undone!',
        'backup_settings': 'Backup Settings',
        'backup_location': 'Backup Location',
        'browse': 'Browse',
        'select_folder': 'Select Backup Folder',
        'create_backup_now': 'Create Backup Now',
        'restore_selected': 'Restore Selected',
        'delete_selected': 'Delete Selected',
        'import_backup': 'Import Backup',
        'settings': 'Settings',
        'appearance': 'Appearance',
        'backup': 'Backup',
        'paths': 'Paths',
        'enable_backups': 'Enable automatic backups',
        'backup_frequency': 'Backup frequency',
        'on_startup': 'On startup',
        'daily': 'Daily',
        'weekly': 'Weekly',
        'monthly': 'Monthly',
        'max_backups_to_keep': 'Maximum backups to keep',
        'select_backup_directory': 'Select Backup Directory',
        'select_fdm_directory': 'Select FDM Files Directory',
        'backup_directory': 'Backup Directory',
        'fdm_files_directory': 'FDM Files Directory',
        'browse': 'Browse',
        'default_paths_note': 'Note: Leave empty to use default paths',

        # Sponsor Dialog
        'thank_you_for_using': 'Thank you for using',
        'app_title': '3D Filament Manager',
        'if_you_find_useful': 'This application is developed and maintained by a single developer.\n',
        'your_contribution_helps': 'Your contribution helps keep the project alive and allows for new features and improvements.',
        'sponsor': 'Sponsor',
        'sponsor_on_github': 'Sponsor on GitHub',
        'join_discord': 'Join Discord',
        'buy_me_a_coffee': 'Donate on Paypal',
        'join_the_patreon': 'Join the Patreon',
        'close': 'Close',
        'language_menu': 'Language',
        'english': 'English',
        'italian': 'Italian',
    },
    'it': {
        # Main Window
        'title': 'Manager Filamenti 3D',
        'file': 'File',
        'view': 'Visualizza',
        'dark_mode': 'Modalità Scura',
        'language': 'Lingua',
        'reload_filaments': 'Ricarica Filamenti',
        'help': 'Aiuto',
        'import_filaments': 'Importa Filamenti',
        'export_filaments': 'Esporta Filamenti',
        'exit': 'Esci',
        'about': 'Informazioni',
        'filter_placeholder': 'Filtra per marca, materiale, o colore...',
        'search_label': 'Cerca:',
        'add_filament': 'Aggiungi Filamento',
        'edit_filament': 'Modifica Filamento',
        'delete_filament': 'Elimina Filamento',
        'details_title': 'Dettagli',
        'properties_title': 'Proprietà',
        'slicer_settings': 'Impostazioni Slicer',
        'tools': 'Strumenti',
        'price_tracker': 'Tracker Prezzo',
        'barcode_utility': 'Gestione CodiceBarre',

        # Treeview Columns
        'col_brand': 'Marca',
        'col_material': 'Materiale',
        'col_color': 'Colore',
        'col_remaining': 'Rimanente (%)',
        'col_cost': 'Costo (€/kg)',
        'col_diameter': 'Diametro (mm)',
        'col_density': 'Densità (g/cm³)',
        'col_initial_qty': 'Qtà Iniziale (g)',
        'col_spool_weight': 'Peso Bobina (g)',
        'col_print_temp': 'Temp. Stampa (°C)',
        'col_bed_temp': 'Temp. Piatto (°C)',
        'col_max_flow': 'Flusso Max (mm³/s)',
        'col_filename': 'Nome File',

        # Details Panel
        'detail_brand': 'Marca',
        'detail_material': 'Materiale',
        'detail_color': 'Colore',
        'detail_description': 'Descrizione',
        'detail_diameter': 'Diametro',
        'detail_density': 'Densità',
        'detail_initial_qty': 'Quantità Iniziale',
        'detail_spool_weight': 'Peso Bobina',
        'detail_cost': 'Costo',
        'detail_cost_per_kg': 'Costo al Kg',
        'detail_cost_per_meter': 'Costo al Metro',
        'detail_remaining': 'Rimanente',
        'detail_remaining_qty': 'Quantità Rimanente',
        'detail_last_used': 'Ultimo Utilizzo',
        'detail_slicer_settings': 'Impostazioni Slicer',
        'detail_notes': 'Note',

        # Add/Edit Dialog
        'add_dialog_title': 'Aggiungi Nuovo Filamento',
        'edit_dialog_title': 'Modifica Filamento',
        'label_brand': 'Marca',
        'label_material': 'Materiale',
        'label_color': 'Colore',
        'label_diameter': 'Diametro (mm)',
        'label_density': 'Densità (g/cm³)',
        'label_initial_qty': 'Quantità Iniziale (g)',
        'label_spool_weight': 'Peso Bobina (g)',
        'label_cost': 'Costo (€/kg)',
        'label_slicer_settings': 'Impostazioni Slicer',
        'label_notes': 'Note',
        'apply': 'Applica',
        'cancel': 'Annulla',

        # Dialogs & Messages
        'app_title': 'Manager Filamenti 3D',
        'about_description': 'Un semplice strumento per gestire i filamenti di stampa 3D.',
        'created_by': 'Creato da',
        'help_dialog_title': 'Aiuto',
        'about_dialog_title': 'Informazioni su Manager Filamenti 3D',
        'version': 'Versione',
        'author': 'Autore',
        'confirm_deletion_title': 'Conferma Eliminazione',
        'confirm_deletion_msg': 'Sei sicuro di voler eliminare questo filamento?',
        'error_title': 'Errore',
        'no_filament_selected_msg': 'Nessun filamento selezionato.',
        'save_error_msg': 'Impossibile salvare il filamento.',
        'import_success_title': 'Importazione Riuscita',
        'import_success_msg': 'Filamenti importati con successo.',
        'export_success_title': 'Esportazione Riuscita',
        'export_success_msg': 'Filamenti esportati con successo.',
        'import_error_title': 'Errore di Importazione',
        'import_error_msg': 'Impossibile importare i filamenti.',
        'export_error_title': 'Errore di Esportazione',
        'export_error_msg': 'Impossibile esportare i filamenti.',
        'delete_error_msg': 'Impossibile eliminare il filamento.',
        'import_zip_title': 'Importa da Zip',
        'export_zip_title': 'Esporta in Zip',
        'select_zip_title': 'Seleziona file ZIP',
        'select_zip_prompt': 'Seleziona file ZIP da importare',
        'save_zip_title': 'Salva file ZIP',
        'save_zip_prompt': 'Salva filamenti come ZIP',
        'language_change_title': 'Cambio Lingua',
        'language_change_msg': 'La lingua è stata cambiata. Riavvia l\'applicazione per rendere effettive le modifiche.',
        'not_available': 'N/D',
        'never': 'Mai',
        'no_slicer_settings': 'Nessuna impostazione specifica dello slicer.',

        # Help Dialog
        'help_title': 'Come usare il Manager Filamenti:',
        'help_main_list': 'La lista principale mostra tutti i tuoi profili filamento.',
        'help_sort': 'Clicca sulle intestazioni delle colonne per ordinare.',
        'help_search': 'Usa la casella di ricerca per filtrare i filamenti.',
        'help_select': 'Seleziona un filamento per vedere i suoi dettagli sulla destra.',
        'help_add': 'Usa \'Aggiungi Nuovo\' per creare un nuovo profilo filamento.',
        'help_edit': 'Seleziona un filamento e clicca \'Modifica Selezionato\' per modificarlo.',
        'help_import_export': 'Usa File > Importa/Esporta per fare il backup o ripristinare la tua libreria filamenti da un file .zip.',
        'backup_management': 'Gestione Backup',
        'backup': 'Backup',
        'create_backup': 'Crea Backup',
        'create_backup_now': 'Crea Backup Ora',
        'restore_selected': 'Ripristina Backup Selezionato',
        'delete_selected': 'Elimina Backup Selezionato',
        'import_backup': 'Importa Backup',
        'restore_backup': 'Ripristina Backup',
        'manage_backups': 'Gestisci Backup',
        'backup_created': 'Backup creato con successo!',
        'backup_restored': 'Backup ripristinato con successo!',
        'backup_failed': 'Creazione del backup fallita',
        'restore_failed': 'Ripristino del backup fallito',
        'no_backups': 'Nessun backup disponibile',
        'backup_list': 'Backup disponibili',
        'backup_date': 'Data del Backup',
        'backup_size': 'Dimensione',
        'backup_actions': 'Azioni',
        'restore': 'Ripristina',
        'delete': 'Elimina',
        'close': 'Chiudi',
        'automatic_backups': 'Backup Automatici',
        'backup_frequency': 'Frequenza Backup',
        'max_backups': 'Numero Massimo di Backup',
        'include_logs': 'Includi Log',
        'backup_on_startup': 'Backup all\'avvio',
        'backup_on_exit': 'Backup all\'uscita',
        'backup_now': 'Esegui Backup Ora',
        'select_backup': 'Seleziona il Backup da Ripristinare',
        'confirm_restore': 'Sei sicuro di voler ripristinare questo backup? Tutti i dati correnti verranno sostituiti!',
        'confirm_delete': 'Sei sicuro di voler eliminare questo backup? Questa azione non può essere annullata!',
        'backup_settings': 'Impostazioni Backup',
        'backup_location': 'Posizione Backup',
        'browse': 'Sfoglia',
        'select_folder': 'Seleziona Cartella di Backup',
        'restore_backup': 'Ripristina Backup',
        'manage_backups': 'Gestisci Backup',
        'backup_created': 'Backup creato con successo!',
        'backup_restored': 'Backup ripristinato con successo!',
        'backup_failed': 'Impossibile creare il backup',
        'restore_failed': 'Impossibile ripristinare il backup',
        'no_backups': 'Nessun backup disponibile',
        'backup_list': 'Backup disponibili',
        'backup_date': 'Data del Backup',
        'backup_size': 'Dimensione',
        'backup_actions': 'Azioni',
        'restore': 'Ripristina',
        'delete': 'Elimina',
        'close': 'Chiudi',
        'automatic_backups': 'Backup Automatici',
        'backup_frequency': 'Frequenza Backup',
        'max_backups': 'Numero Massimo di Backup',
        'include_logs': 'Includi Log',
        'backup_on_startup': 'Backup all\'Avvio',
        'backup_on_exit': 'Backup all\'Uscita',
        'backup_now': 'Esegui Backup Ora',
        'select_backup': 'Seleziona il Backup da Ripristinare',
        'confirm_restore': 'Sei sicuro di voler ripristinare questo backup? Tutti i dati attuali verranno sostituiti!',
        'confirm_delete': 'Sei sicuro di voler eliminare questo backup? Questa azione non può essere annullata!',
        'backup_settings': 'Impostazioni Backup',
        'backup_location': 'Cartella di Backup',
        'browse': 'Sfoglia',
        'select_folder': 'Seleziona Cartella di Backup',
        
        # Settings Dialog
        'settings': 'Impostazioni',
        'appearance': 'Aspetto',
        'paths': 'Percorsi',
        'enable_backups': 'Abilita backup automatici',
        'backup_frequency': 'Frequenza backup',
        'on_startup': "All'avvio",
        'daily': 'Quotidiano',
        'weekly': 'Settimanale',
        'monthly': 'Mensile',
        'max_backups_to_keep': 'Numero massimo di backup da conservare',
        'select_backup_directory': 'Seleziona la cartella di backup',
        'select_fdm_directory': 'Seleziona la cartella dei file FDM',
        'backup_directory': 'Cartella di backup',
        'fdm_files_directory': 'Cartella file FDM',
        'browse': 'Sfoglia',
        'save': 'Salva',
        'cancel': 'Annulla',
        'default_paths_note': 'Nota: Lascia vuoto per utilizzare i percorsi predefiniti',

        # Error Messages
        'no_filament_selected_title': 'Nessuna Selezione',
        'no_filament_selected_msg': 'Per favore seleziona un filamento dalla lista.',

        # Sponsor Dialog
        'thank_you_for_using': 'Grazie per usare',
        'app_title': '3D Filament Manager',
        'if_you_find_useful': 'Questa applicazione è sviluppata e gestita da un unico sviluppatore.\n',
        'your_contribution_helps': 'Il tuo contributo aiuta a mantenere vivo il progetto e consente l\'introduzione di nuove funzionalità e miglioramenti.',
        'sponsor': 'Sponsorizza',
        'sponsor_on_github': 'Sponsorizza su GitHub',
        'join_discord': 'Unisciti a Discord',
        'buy_me_a_coffee': 'Donazione con Paypal',
        'join_the_patreon': 'Unisciti a Patreon',
        'close': 'Chiudi',
        'language_menu': 'Lingua',
        'english': 'Inglese',
        'italian': 'Italiano',
    }
}

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.3d_filament_manager_lang.json')

_current_lang = 'en'

def _load_lang() -> None:
    """
    Load the user's language preference from the configuration file.
    
    This function reads the language code from the config file located at
    ~/.3d_filament_manager_lang.json. If the file doesn't exist or contains
    an invalid language code, it falls back to English ('en') as the default.
    
    The function updates the global _current_lang variable with the loaded language code.
    """
    global _current_lang
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                data = json.load(f)
                _current_lang = data.get('language', 'en')
        except (json.JSONDecodeError, IOError):
            _current_lang = 'en'

def _save_lang(lang_code: str) -> None:
    """
    Save the specified language code to the configuration file.
    
    Args:
        lang_code: The language code to save (e.g., 'en', 'it').
        
    The function creates or updates the config file at ~/.3d_filament_manager_lang.json
    with the specified language code. This ensures the user's language preference
    persists between application sessions.
    """
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump({'language': lang_code}, f)
    except IOError:
        pass

def set_language(lang_code: str) -> None:
    """
    Change the application's current language.
    
    Args:
        lang_code: The language code to switch to (e.g., 'en', 'it').
                  Must be one of the available languages returned by get_available_languages().
                  
    The function updates the current language and saves the preference to the config file.
    If the specified language is not available, it falls back to English ('en') and
    raises a ValueError.
    
    Raises:
        ValueError: If the specified language code is not supported.
    """
    global _current_lang
    if lang_code in LANGUAGES:
        _current_lang = lang_code
        _save_lang(_current_lang)

def get_available_languages() -> list[str]:
    """
    Get a list of all available language codes in the application.
    
    Returns:
        A list of language code strings (e.g., ['en', 'it']).
        
    Example:
        >>> get_available_languages()
        ['en', 'it']
    """
    return list(LANGUAGES.keys())

def get_language() -> str:
    """
    Get the currently active language code.
    
    Returns:
        str: The current language code (e.g., 'en' for English, 'it' for Italian).
        
    The returned value will always be one of the language codes available in LANGUAGES.
    """
    return _current_lang

def tr(key: str, **kwargs) -> str:
    """
    Translate a text key to the current application language.
    
    This is the main translation function used throughout the application to get
    localized strings. It looks up the provided key in the current language's
    dictionary and returns the corresponding translation.
    
    Args:
        key: The translation key to look up in the current language dictionary.
        **kwargs: Optional format arguments to be substituted into the translated string.
                 The string should contain Python format placeholders (e.g., {name})
                 which will be replaced by the named arguments.
                 
    Returns:
        str: The translated string with any format placeholders replaced by the
             provided keyword arguments.
             
    Example:
        # In English: 'Hello, {name}!' with name='John' becomes 'Hello, John!'
        greeting = tr('greeting', name='John')
        
    Note:
        If the key is not found in the current language, it will fall back to English.
        If the key is not found in English, it will return the key itself.
    """
    text = LANGUAGES.get(_current_lang, LANGUAGES['en']).get(key, key)
    return text.format(**kwargs)

_load_lang()
