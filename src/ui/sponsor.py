import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import os
import logging
import base64
import tempfile
import io

# Try to import qrcode for QR code generation
try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    qrcode = None
    HAS_QRCODE = False
    logging.debug("qrcode not available - QR code generation will be disabled")

logger = logging.getLogger(__name__)

class LinkLabel(tk.Label):
    """A clickable link label that opens URLs in the default web browser."""
    def __init__(self, master=None, url=None, text=None, **kwargs):
        super().__init__(master, **{k: v for k, v in kwargs.items() if k != 'cursor'})
        self.url = url
        self.default_color = self.cget('fg')
        self.link_color = '#0000ff'  # Blue color for links
        
        if text is None and url:
            text = url
            
        self.config(
            text=text or '',
            fg=self.link_color,
            cursor='hand2',
            font=('TkDefaultFont', 10, 'underline')
        )
        
        self.bind('<Button-1>', self.open_link)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def open_link(self, event=None):
        if self.url:
            webbrowser.open(self.url)
    
    def on_enter(self, event):
        self.config(fg='#ff0000')  # Red on hover
    
    def on_leave(self, event):
        self.config(fg=self.link_color)

class SponsorDialog(tk.Toplevel):
    def __init__(self, parent=None, language_manager=None, dark_mode=False):
        super().__init__(parent)
        self.parent = parent
        self.language_manager = language_manager
        self.dark_mode = dark_mode
        self.tr = language_manager.tr if language_manager else lambda key, default: default
        
        self.title(self.tr("sponsor.window_title", "Support Development"))
        self.minsize(500, 400)
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Main container
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(
            main_frame,
            text=self.tr("sponsor.title", "Support 3D Filament Manager"),
            font=('TkDefaultFont', 14, 'bold')
        )
        title.pack(pady=(0, 20))
        
        # Message
        message = ttk.Label(
            main_frame,
            text=self.tr(
                "sponsor.message",
                "If you find this application useful, please consider supporting its development.\n\n"
                "Your support helps cover hosting costs and encourages further development."
            ),
            wraplength=450,
            justify=tk.CENTER
        )
        message.pack(pady=(0, 20))
        
        # Donation methods frame
        methods_frame = ttk.Frame(main_frame)
        methods_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # GitHub Sponsors
        ttk.Label(methods_frame, text=self.tr("sponsor.links.github_sponsors", "GitHub Sponsors:")).pack(pady=5)
        LinkLabel(methods_frame, url="https://github.com/sponsors/Nsfr750").pack(pady=5)
        
        # PayPal
        ttk.Label(methods_frame, text=self.tr("sponsor.links.paypal", "PayPal:")).pack(pady=5)
        LinkLabel(methods_frame, url="https://paypal.me/3dmega").pack(pady=5)
        
        # Monero
        monero_frame = ttk.Frame(methods_frame)
        monero_frame.pack(pady=10)
        
        ttk.Label(monero_frame, text=self.tr("sponsor.monero.label", "Monero:")).pack()
        
        monero_address = "47Jc6MC47WJVFhiQFYwHyBNQP5BEsjUPG6tc8R37FwcTY8K5Y3LvFzveSXoGiaDQSxDrnCUBJ5WBj6Fgmsfix8VPD4w3gXF"
        monero_display = "XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR"
        
        address_frame = ttk.Frame(monero_frame)
        address_frame.pack(pady=5, ipadx=10, ipady=5)
        
        monero_label = ttk.Label(
            address_frame,
            text=monero_display,
            font=('Courier', 10),
            # background='#f0f0f0',
            relief='solid',
            borderwidth=1,
            padding=5
        )
        monero_label.pack()
        
        # Generate QR Code (only if qrcode is available)
        if HAS_QRCODE:
            try:
                # Generate QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=5,
                    border=4,
                )
                qr.add_data(f'monero:{monero_address}')
                qr.make(fit=True)
                
                # Create QR code image as a string buffer
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Save to a bytes buffer
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                
                # Create a base64-encoded string of the image
                b64_data = base64.b64encode(buffer.read()).decode('utf-8')
                
                # Create a Tkinter PhotoImage from the base64 data
                self.qr_photo = tk.PhotoImage(data=b64_data)
                
                # Display the QR code
                qr_label = ttk.Label(monero_frame, image=self.qr_photo)
                qr_label.image = self.qr_photo  # Keep a reference
                qr_label.pack(pady=10)
                
                # Add copy to clipboard button
                copy_btn = ttk.Button(
                    monero_frame,
                    text=self.tr("sponsor.copy_address", "Copy Address"),
                    command=lambda: self.copy_to_clipboard(monero_address)
                )
                copy_btn.pack(pady=5)
                
            except Exception as e:
                logging.error(f"Error generating QR code: {e}")
                logging.exception("QR code generation error")
        
        # Add Close button at the bottom right
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', padx=5, pady=10, side='bottom', anchor='e')
        
        # Configure the red button style
        style = ttk.Style()
        style.configure('Red.TButton', 
                       foreground='white',
                       background='red',
                       font=('TkDefaultFont', 10, 'bold'))
        
        close_btn = ttk.Button(
            button_frame,
            text=self.tr("sponsor.close", "Close"),
            command=self.destroy,
            style='Red.TButton'
        )
        close_btn.pack(side='right', padx=5)
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard and show confirmation."""
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo(
            self.tr("sponsor.copied", "Copied"),
            self.tr("sponsor.address_copied", "Address copied to clipboard!")
        )

def show_sponsor_dialog(parent=None, language_manager=None, dark_mode=False):
    """Show the sponsor/donation dialog."""
    dialog = SponsorDialog(parent, language_manager=language_manager, dark_mode=dark_mode)
    return dialog

if __name__ == "__main__":
    # Example usage
    root = tk.Tk()
    app = SponsorDialog(root)
    root.mainloop()