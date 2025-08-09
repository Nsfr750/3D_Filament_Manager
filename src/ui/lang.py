# Simple multilanguage support for English and Italian

import json
import os

LANGUAGES = {
    'en': {
        # Main Window
        'title': '3D Filament Manager',
        'file': '🗃️ File',
        'view': '👁️‍🗨️ View',
        'dark_mode': 'Dark Mode',
        'language': '🌐 Language',
        'reload_filaments': 'Reload Filaments',
        'help': '❓ Help',
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

        # Sponsor Dialog
        'thank_you_for_using': 'Thank you for using',
        'app_title': '3D Filament Manager',
        'if_you_find_useful': 'This application is developed and maintained by a single developer.\nYour support helps keep the project alive and allows for new features and improvements.',
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
        'file': '🗃️ File',
        'view': '👁️‍🗨️ Visualizza',
        'dark_mode': 'Modalità Scura',
        'language': '🌐 Lingua',
        'reload_filaments': 'Ricarica Filamenti',
        'help': '❓ Aiuto',
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

        # Error Messages
        'no_filament_selected_title': 'Nessuna Selezione',
        'no_filament_selected_msg': 'Per favore seleziona un filamento dalla lista.',

        # Sponsor Dialog
        'thank_you_for_using': 'Grazie per usare',
        'app_title': '3D Filament Manager',
        'if_you_find_useful': 'Questa applicazione è sviluppata e gestita da un unico sviluppatore.\nIl tuo sostegno contribuisce a mantenere vivo il progetto e consente l\'introduzione di nuove funzionalità e miglioramenti.',
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

def _load_lang():
    """Load language preference from config file."""
    global _current_lang
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                data = json.load(f)
                _current_lang = data.get('language', 'en')
        except (json.JSONDecodeError, IOError):
            _current_lang = 'en'

def _save_lang(lang_code):
    """Save language preference to config file."""
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump({'language': lang_code}, f)
    except IOError:
        pass

def set_language(lang_code):
    """Set the application language."""
    global _current_lang
    if lang_code in LANGUAGES:
        _current_lang = lang_code
        _save_lang(_current_lang)

def get_available_languages():
    """Get a list of available language codes."""
    return list(LANGUAGES.keys())

def get_language():
    """Get the current application language."""
    return _current_lang

def tr(key, **kwargs):
    """Translate a key to the current language."""
    text = LANGUAGES.get(_current_lang, LANGUAGES['en']).get(key, key)
    return text.format(**kwargs)

_load_lang()
