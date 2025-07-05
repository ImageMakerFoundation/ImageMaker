#!/usr/bin/env python3
import os
import sys
import copy
import threading
import itertools
import string

import hashlib
from pathlib import Path

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image

import imutils


class imNFTMiner:
    
    def __init__(self):
        self.img_path = None
        self.mining = False
        self.stop_event = threading.Event()

        self.secret_len = 1
        self.iter_count = 0

    def open_image(self):
        if self.mining:
            return
        
        self.img_path = filedialog.askopenfilename(
            title='Select an image',
            filetypes=[('PNG Images', '*.png')]
        )
    
    def mine_row(self, row, img_name, y, secrets):
        print(f'{y}:')
        print(''.join((hex(r)[2:] for r in row)).replace('0', '_'))

        self.secret_len = 1

        while True:
            for c in itertools.islice(
                itertools.product(
                    string.ascii_letters + string.digits,
                    repeat=self.secret_len,
                ),
                self.iter_count,
                None
            ):
                secret = ''.join(c)

                hash = hashlib.sha3_512(
                    bytes(''.join((
                        f"{img_name} {'_'.join(secrets) if secrets else ''}",
                        hex(y)[2:],
                        secret,
                    )), 'ascii')
                ).hexdigest()

                found = True
                for i in range(16):
                    if not row[i]:
                        continue
                    
                    if hash[i] != hex(row[i])[2:]:
                        found = False
                        break
                
                if found:
                    if secret in secrets:
                        continue

                    print(f'{hash[:16]} - {secret}')
                    print(f'{round((y+1)*100/16)}%\n')

                    secrets.append(secret)
                    self.iter_count = 0

                    return

                self.iter_count += 1

            self.secret_len += 1
            self.iter_count = 0

    def mine(self):
        if self.mining:
            return
        else:
            self.mining = True
        
        img_path = copy.deepcopy(self.img_path) if self.img_path else None

        self.root.after(0, lambda: self.progress_bar.config(value=0))

        if not img_path:
            self.root.after(
                0,
                lambda: messagebox.showerror('Error', 'Select an image first.'),
            )
            self.mining = False
            return

        img_name = Path(img_path).stem

        if not imutils.is_alnum_underscore(img_name):
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    'Error',
                    'Image name can contain only English letters, digits and underscores.',
                )
            )
            self.mining = False
            return
        
        with Image.open(img_path) as img:
            if img.width != 16 or img.height != 16:
                self.root.after(0, lambda: messagebox.showerror('Error', 'Image must be 16x16.'))
                self.mining = False
                return
            
            img_data = list(img.getdata())
            rows = []

            existing_proof_text = self.proof_text.get('1.0', 'end').strip()
            secrets = existing_proof_text.split('_') if existing_proof_text else []
            start_row = len(secrets)

            iteration = imutils.ThemedStrDialog(
                self.root,
                'Set Counter', 'Set counter to (leave empty to start new): ',
            ).result

            if iteration is None:
                self.mining = False
                return
            
            if iteration == '':
                self.secret_len = 1
                self.iter_count = 0
            
            else:
                try:
                    secret_len = int(iteration.split(':')[0])
                    if secret_len is None or secret_len < 1:
                        secret_len = 1

                    iter_count = int(iteration.split(':')[1].replace(',', ''))
                    if iter_count is None or iter_count < 0:
                        iter_count = 0
                    
                    self.secret_len = secret_len
                    self.iter_count = iter_count
                
                except:
                    self.root.after(
                        0,
                        lambda: messagebox.showerror('Error', "Bad counter format, must be 'Number:Number'."),
                    )

                    self.mining = False
                    return

            for y in range(start_row):
                row = []
                img_row = img_data[y * 16:(y + 1) * 16]
                for px in img_row:
                    row.append(
                        next((i for i, v in enumerate(imutils.PALETTE) if v == px[:3]), 0)
                    )
                rows.append(row)
            
            if start_row > 0:
                self.root.after(
                    0,
                    lambda v=round(start_row * 100 / img.height): self.progress_bar.config(value=v)
                )

            for y in range(start_row, 16):
                if self.stop_event.is_set():
                    self.mining = False
                    return

                row = []
                img_row = img_data[y * 16:(y + 1) * 16]
                for px in img_row:
                    row.append(
                        next((i for i, v in enumerate(imutils.PALETTE) if v == px[:3]), 0)
                    )
                
                active = sum(1 for color_index in row if imutils.PALETTE[color_index] != (0, 0, 0))
                complexity = (16 ** active) if active > 0 else 1

                self.root.after(0, lambda y=y: self.label_row.config(text=f'Current Row: {y+1}'))
                self.root.after(0, lambda c=complexity: self.label_complexity.config(text=f'Current Mining Complexity: {c:,}'))

                self.mine_row(row, img_name, y, secrets)
                rows.append(row)

                self.root.after(
                    0,
                    lambda v=round((y + 1) * 100 / img.height): self.progress_bar.config(value=v)
                )
                self.root.after(0, lambda: self.proof_text.delete('1.0', 'end'))
                self.root.after(0, lambda: self.proof_text.insert('1.0', '_'.join(secrets)))
            
            enc_mask = imutils.get_enc_mask(rows)
            proof_of_work = '_'.join(secrets)

            full_imid = '.'.join((img_name, enc_mask, proof_of_work))
            token_id = hashlib.sha3_256(bytes(full_imid, 'ascii')).hexdigest()

            imid = '.'.join((img_name, token_id[:8]))

            print(f'imID: {imid}')
            print(f'PoW: {proof_of_work}')

            with open(f'{img_name}.imnft', 'w') as f:
                f.write(f'{enc_mask}.{proof_of_work}\n')
            
            self.root.after(0, lambda: messagebox.showinfo('Info', 'Mining success.'))
            self.root.after(0, lambda: self.progress_bar.config(value=0))

            self.root.after(0, lambda: self.label_row.config(text=f'Current Row: N/A'))
            self.root.after(0, lambda: self.label_complexity.config(text=f'Current Mining Complexity: N/A'))

            self.proof_text.delete('1.0', tk.END)
            
            self.mining = False
    
    def show_counter(self):
        messagebox.showinfo('Iteration Counter', f'{self.secret_len}:{self.iter_count:,}')

    def main(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)

        def on_close():
            self.stop_event.set()
            self.root.destroy()

        self.root.protocol('WM_DELETE_WINDOW', on_close)

        cwd = os.getcwd()
        if getattr(sys, 'frozen', False):
            os.chdir(sys._MEIPASS)

        icon = tk.PhotoImage(file=imutils.ICON)
        self.root.iconphoto(True, icon)

        os.chdir(cwd)

        self.root.title('imNFT Miner')

        imutils.apply_theme(self.root)

        open_button = ttk.Button(
            self.root,
            text='Open',
            command=self.open_image,
        )
        open_button.grid(row=0, column=0, padx=125, pady=10)

        mine_button = ttk.Button(
            self.root,
            text='Mine',
            command=lambda: threading.Thread(target=self.mine, daemon=True).start(),
        )
        mine_button.grid(row=1, column=0, padx=125, pady=10)

        show_button = ttk.Button(
            self.root,
            text='Show Counter',
            command=self.show_counter,
        )
        show_button.grid(row=2, column=0, padx=125, pady=10)

        self.progress_bar = ttk.Progressbar(
            self.root,
            orient='horizontal',
            length=250,
            mode='determinate',
        )
        self.progress_bar.grid(row=3, column=0, pady=10)

        self.label_row = ttk.Label(self.root, text='Current Row: N/A')
        self.label_row.grid(row=4, column=0)

        self.label_complexity = ttk.Label(self.root, text='Current Mining Complexity: N/A')
        self.label_complexity.grid(row=5, column=0)

        self.proof_text = tk.Text(
            self.root,
            width=40,
            height=6,
            bg=imutils.UI_LIGHT_HEADER_BG,
            fg=imutils.UI_TEXTCOLOR,
            insertbackground=imutils.UI_TEXTCOLOR,
            font=imutils.UI_MONOSPACE_FONT,
            wrap='word',
            relief='flat',
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=imutils.UI_HIGHLIGHT,
        )

        self.proof_text.grid(row=6, column=0, padx=10, pady=10)

        self.root.mainloop()


def main():
    imNFTMiner().main()


if __name__ == '__main__':
    main()
