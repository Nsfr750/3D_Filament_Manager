import tkinter as tk
from tkinter import ttk
import webbrowser
from .lang import tr

def show_sponsor_dialog(parent):
    """Displays the Sponsor dialog box."""
    dialog = tk.Toplevel(parent)
    dialog.title(tr('sponsor'))

    main_frame = tk.Frame(dialog, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    message = (
        f"{tr('thank_you_for_using')} {tr('app_title')}\n\n"
        f"{tr('if_you_find_useful')}\n"
        f"{tr('your_contribution_helps')}"
    )

    label = tk.Label(main_frame, text=message, wraplength=350, justify=tk.CENTER)
    label.pack(pady=(0, 20))

    button_frame = tk.Frame(main_frame)
    button_frame.pack()

    buttons = [
        (tr('sponsor_on_github'), "https://github.com/sponsors/Nsfr750"),
        (tr('join_discord'), "https://discord.gg/BvvkUEP9"),
        (tr('buy_me_a_coffee'), "https://paypal.me/3dmega"),
        (tr('join_the_patreon'), "https://www.patreon.com/Nsfr750")
    ]

    for text, url in buttons:
        btn = ttk.Button(button_frame, text=text, command=lambda u=url: webbrowser.open(u))
        btn.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X)

    close_button = ttk.Button(dialog, text=tr('close'), command=dialog.destroy)
    close_button.pack(pady=10)

    dialog.transient(parent)
    dialog.grab_set()
    parent.wait_window(dialog)
