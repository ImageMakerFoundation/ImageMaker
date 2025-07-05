import hashlib
import hmac
import re
import struct
from decimal import Decimal, getcontext

from ecdsa import SECP256k1, SigningKey
from ecdsa.util import string_to_number

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

ICON = 'icon.png'

PALETTE = (
    (0x00, 0x00, 0x00),
    (0x86, 0x86, 0x86),
    (0x65, 0x36, 0x00),
    (0x00, 0x65, 0x00),
    (0x00, 0x00, 0xca),
    (0x36, 0x00, 0x97),
    (0xdc, 0x00, 0x00),
    (0xff, 0xff, 0x00),

    (0x45, 0x45, 0x45),
    (0xb9, 0xb9, 0xb9),
    (0x97, 0x65, 0x36),
    (0x00, 0xa8, 0x00),
    (0x00, 0x97, 0xff),
    (0xff, 0x00, 0x97),
    (0xff, 0x65, 0x00),
    (0xff, 0xff, 0xff),
)

PIXEL_SIZE = 20
PALETTE_RECT_SIZE = 30

CBASE_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

UINT40_MAX = (1 << 40) - 1
UINT96_MAX = (1 << 96) - 1

getcontext().prec = 50

UI_BGCOLOR = '#0b0b0b'
UI_TEXTCOLOR = '#f8f8f8'
UI_HIGHLIGHT = '#d4af37'
UI_DARK_HIGHLIGHT = '#b8912d'
UI_BORDER_COLOR = UI_HIGHLIGHT
UI_HEADER_BG = '#111'
UI_LIGHT_HEADER_BG = '#222'

UI_MONOSPACE_FONT = ('Courier New', 11)


def wei_to_eth(wei):
    eth = Decimal(wei) / Decimal('1000000000000000000')
    return format(eth, 'f')


def derive_bip32_child_key(seed, path):
    I = hmac.new(b'Bitcoin seed', seed, hashlib.sha512).digest()
    priv_key = I[:32]
    chain_code = I[32:]

    def CKD_priv(k_par, c_par, index):
        if index >= 0x80000000:
            data = b'\x00' + k_par + struct.pack('>L', index)
        else:
            pubkey = SigningKey.from_string(k_par, curve=SECP256k1).verifying_key.to_string('compressed')
            data = pubkey + struct.pack('>L', index)

        I = hmac.new(c_par, data, hashlib.sha512).digest()
        Il, Ir = I[:32], I[32:]
        child_key_int = (string_to_number(Il) + string_to_number(k_par)) % SECP256k1.order
        child_key = child_key_int.to_bytes(32, 'big')
        return child_key, Ir

    elements = path.split('/')[1:]
    for e in elements:
        hardened = e.endswith("'")
        index = int(e[:-1]) if hardened else int(e)
        index += 0x80000000 if hardened else 0
        priv_key, chain_code = CKD_priv(priv_key, chain_code, index)

    return priv_key

def unique_ordered(seq):
    result = []

    seen = set()
    
    for item in seq:
        if item not in seen:
            result.append(item)
            seen.add(item)

    return result


def is_alnum_underscore(s):
    return re.fullmatch(r'\w+', s) is not None


def to_custom_base(num):
    if num == 0:
        return CBASE_CHARS[0]

    chars = []
    base = len(CBASE_CHARS)

    while num > 0:
        num, rem = divmod(num, base)
        chars.append(CBASE_CHARS[rem])

    return ''.join(reversed(chars))


def from_custom_base(s):
    base = len(CBASE_CHARS)
    value = 0

    for c in s:
        value = value * base + CBASE_CHARS.index(c)
    
    return value


def get_enc_mask(rows):
    mask = ''

    for i in range(16):
        row_mask = ''.join((
            '1' if px else '0'
            for px
            in rows[i]
        ))

        mask += row_mask
    
    return to_custom_base(int(mask, 2))


def apply_theme(root):
    default_font = ('Trebuchet MS', 12)

    style = ttk.Style(root)
    root.configure(bg=UI_BGCOLOR)
    style.theme_use('default')

    style.configure('.', 
                    background=UI_BGCOLOR,
                    foreground=UI_TEXTCOLOR,
                    font=default_font)

    style.configure('TFrame',
                    background=UI_BGCOLOR)

    style.configure('TLabel',
                    background=UI_BGCOLOR,
                    foreground=UI_TEXTCOLOR,
                    font=default_font)

    style.configure('TButton',
                    background=UI_HIGHLIGHT,
                    foreground='#000000',
                    padding=6,
                    borderwidth=0,
                    font=('Segoe UI', 11, 'bold'))
    style.map('TButton',
              background=[('active', UI_DARK_HIGHLIGHT)],
              foreground=[('active', '#000000')])
    
    style.configure('TCheckbutton',
                    background=UI_BGCOLOR,
                    foreground=UI_TEXTCOLOR,
                    font=default_font,
                    focuscolor=UI_BGCOLOR,
                    indicatorcolor=UI_BGCOLOR,
                    borderwidth=1)

    style.map('TCheckbutton',
              background=[('active', UI_BGCOLOR)],
              foreground=[('active', UI_HIGHLIGHT)],
              indicatorcolor=[('selected', UI_HIGHLIGHT)],
              indicatorbackground=[('selected', UI_HIGHLIGHT)],
              relief=[('pressed', 'sunken'), ('!pressed', 'flat')])

    style.configure('TEntry',
                    fieldbackground=UI_BGCOLOR,
                    foreground=UI_TEXTCOLOR,
                    insertcolor=UI_TEXTCOLOR,
                    borderwidth=0,
                    relief='flat',
                    padding=6)
    style.map('TEntry',
              foreground=[('focus', UI_TEXTCOLOR)],
              fieldbackground=[('focus', '#111')])

    style.configure('TCombobox',
                    fieldbackground=UI_BGCOLOR,
                    background=UI_BGCOLOR,
                    foreground=UI_TEXTCOLOR,
                    arrowcolor=UI_HIGHLIGHT)
    style.map('TCombobox',
              fieldbackground=[('readonly', UI_BGCOLOR)],
              foreground=[('readonly', UI_TEXTCOLOR)])
    
    style.configure('TProgressbar',
                    troughcolor=UI_TEXTCOLOR,
                    background=UI_LIGHT_HEADER_BG,
                    thickness=10)

    style.configure('TNotebook',
                    background=UI_BGCOLOR,
                    borderwidth=0)
    style.configure('TNotebook.Tab',
                    background=UI_HEADER_BG,
                    foreground=UI_TEXTCOLOR,
                    padding=10)
    style.map('TNotebook.Tab',
              background=[('selected', UI_HIGHLIGHT)],
              foreground=[('selected', '#000000')])

    style.configure('Treeview',
                    background=UI_BGCOLOR,
                    foreground=UI_TEXTCOLOR,
                    fieldbackground=UI_BGCOLOR,
                    bordercolor=UI_BORDER_COLOR)
    style.map('Treeview',
              background=[('selected', UI_HIGHLIGHT)],
              foreground=[('selected', '#000000')])

    style.configure('Vertical.TScrollbar',
                    troughcolor=UI_BGCOLOR,
                    background=UI_HIGHLIGHT,
                    bordercolor=UI_BGCOLOR)
    style.map('Vertical.TScrollbar',
              background=[('active', UI_DARK_HIGHLIGHT)])

    root.option_add('*Font', default_font)
    root.option_add('*Background', UI_BGCOLOR)
    root.option_add('*Foreground', UI_TEXTCOLOR)


class ThemedDialogBase:
    def __init__(self, parent, title, prompt, is_int=False):
        self.result = None
        self.is_int = is_int

        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.configure(bg="#0b0b0b")
        self.window.grab_set()
        self.window.resizable(False, False)

        self.create_widgets(prompt)
        self.window.protocol("WM_DELETE_WINDOW", self.cancel)
        self.entry.focus()
        self.window.wait_window()

    def create_widgets(self, prompt):
        label = ttk.Label(self.window, text=prompt)
        label.pack(padx=16, pady=(16, 4), anchor="w")

        self.entry = ttk.Entry(self.window)
        self.entry.pack(padx=16, pady=(0, 16), fill="x")

        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(padx=16, pady=(0, 16), fill="x")

        ok_btn = ttk.Button(btn_frame, text="OK", command=self.ok)
        ok_btn.pack(side="left", expand=True, fill="x", padx=(0, 8))

        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=self.cancel)
        cancel_btn.pack(side="left", expand=True, fill="x")

    def ok(self):
        value = self.entry.get()
        if self.is_int:
            try:
                self.result = int(value)
            except ValueError:
                self.result = None
        else:
            self.result = value
        self.window.destroy()

    def cancel(self):
        self.result = None
        self.window.destroy()


class ThemedStrDialog(ThemedDialogBase):
    def __init__(self, parent, title, prompt):
        super().__init__(parent, title, prompt, is_int=False)


class ThemedIntDialog(ThemedDialogBase):
    def __init__(self, parent, title, prompt):
        super().__init__(parent, title, prompt, is_int=True)
