import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, tix

import hashlib, base64

STICKY_ALL = (tix.N, tix.W, tix.S, tix.E)
STICKY_HORIZONTAL = (tix.W, tix.E)
STICKY_VERTICAL = (tix.N, tix.S)

class PasswordConverter(ttk.Frame):
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.pack(fill="both", expand=True)
        self.__createWidgets()
        
    def __createWidgets(self):
        self.pane = ttk.PanedWindow(self, orient=tix.HORIZONTAL)
        self.pane.rowconfigure(0, weight=1)
        self.pane.columnconfigure(0, weight=1)
        self.pane.grid(row=0, column=0, sticky=STICKY_HORIZONTAL)

        # input box
        self.pane.entry_value = tk.StringVar()
        self.pane.entry = ttk.Entry(self.pane, textvariable=self.pane.entry_value)
        self.pane.entry.grid(row=0, column=0, sticky=STICKY_ALL, padx=5)

        # generate button
        self.pane.generate_button = ttk.Button(self.pane)
        self.pane.generate_button["text"] = "生成口令！"
        self.pane.generate_button["command"] = self.__generate_password
        self.pane.grid(row=0, column=1, sticky=STICKY_ALL, padx=5)

        # output_box

    def __generate_password(self):
        pass