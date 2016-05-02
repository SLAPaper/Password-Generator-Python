from TkUtil import *

import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import tix

import hashlib
import base64

import typing as tg


class PasswordConverter(ttk.Frame):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.pack(fill=tix.BOTH, expand=True)
        self.__createWidgets()

    def __createWidgets(self) -> None:
        # <pane>
        self.pane = ttk.PanedWindow(self, orient=tix.HORIZONTAL)
        self.pane.rowconfigure(0, weight=1)
        self.pane.rowconfigure(1, weight=1)
        self.pane.columnconfigure(1, weight=1)
        self.pane.grid(column=0, row=0, sticky=tuple(STICK_HORIZONTAL))

        self.key_label = ttk.Label(self.pane)
        self.key_label["text"] = "Key:"
        self.key_label.grid(column=0, row=0, sticky=tuple(STICK_W))

        self.key_value = tk.StringVar()
        self.key = ttk.Entry(self.pane, textvariable=self.key_value)
        self.key.grid(column=1,
                      row=0,
                      sticky=tuple(STICK_ALL),
                      padx=(5, 2),
                      pady=(1, 2))
        self.key.focus_set()

        self.salt_label = ttk.Label(self.pane)
        self.salt_label["text"] = "Salt:"
        self.salt_label.grid(column=0, row=1, sticky=tuple(STICK_W))

        self.salt_value = tk.StringVar()
        self.salt = ttk.Entry(self.pane, textvariable=self.salt_value)
        self.salt.grid(column=1,
                       row=1,
                       sticky=tuple(STICK_ALL),
                       padx=(5, 2),
                       pady=(2, 1))

        self.button = ttk.Button(self.pane)
        self.button["text"] = "计算！"
        self.button["command"] = self.generate_password
        self.button.grid(column=2,
                         rowspan=2,
                         row=0,
                         sticky=tuple(STICK_VERTICAL),
                         padx=(2, 0))
        # </pane>

        # <scrollpane>
        self.scrollpane = ttk.PanedWindow(self, orient=tix.HORIZONTAL)
        self.scrollpane.grid(column=0, row=1, sticky=tuple(STICK_ALL), padx=5)
        self.scrollpane.columnconfigure(0, weight=1)
        self.scrollpane.rowconfigure(0, weight=1)

        self.text = tix.Text(self.scrollpane, autosep=1)
        self.text.grid(column=0, row=0, sticky=tuple(STICK_ALL))
        self.text['state'] = 'disabled'

        self.scrollbar = ttk.Scrollbar(self.scrollpane, orient=tix.VERTICAL, command=self.text.yview)
        self.scrollbar.grid(column=1, row=0, sticky=tuple(STICK_ALL))

        self.text['yscrollcommand'] = self.scrollbar.set
        # </scrollpane>

    def generate_password(self) -> None:
        self.text['state'] = 'normal'
        self.text.delete('1.0', 'end')
        raw_input = self.key_value.get() + self.salt_value.get() # type: str
        hashers = (hashlib.md5, hashlib.sha1, hashlib.sha224, hashlib.sha256,
                   hashlib.sha384, hashlib.sha512)
        output_strings = [] # type: tg.List[str]
        for hasher_init in hashers:
            hasher = hasher_init()
            name = hasher.name # type: str
            hasher.update(raw_input.encode())
            digest = hasher.digest()
            hexdigest = hasher.hexdigest()
            b64_output = base64.standard_b64encode(digest).decode()
            a85_output = base64.a85encode(digest).decode()
            b85_output = base64.b85encode(digest).decode()
            output_strings.append("hash: %s\nresult: %s\nbase64: %s\nascii85: %s\nbase85: %s\n" % (name, hexdigest, b64_output, a85_output, b85_output))

        for output_string in output_strings:
            self.text.insert('end', output_string + '\n')

        self.text['state'] = 'disabled'


if __name__ == "__main__":
    root = tix.Tk()
    root.title("纸睡的密码生成器")
    root.geometry('600x400')
    root.minsize(300, 200)

    tkFont.nametofont("TkDefaultFont").config(family="Dengxian", size=11)

    style = ttk.Style()
    style.configure("basic.TFrame", foreground="black")
    style.configure("red.TButton", foreground="red")

    mainframe = PasswordConverter(master=root, style="basic.TFrame")

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.bind('<Return>', lambda _: mainframe.generate_password())
    root.bind('<Escape>', lambda _: root.destroy())

    root.mainloop()
