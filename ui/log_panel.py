# -*- coding: utf-8 -*-
"""底部收发日志面板。"""
import tkinter as tk
from tkinter import ttk


class LogPanel(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.var = tk.StringVar(value="")
        tk.Label(self, text="收发日志", font=("Microsoft YaHei", 10, "bold")).pack(anchor=tk.W, padx=6, pady=2)
        self.txt = tk.Text(self, wrap=tk.WORD, height=8, bg="black", fg="#00ff00", font=("Consolas", 9))
        self.txt.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)
        self.txt.config(state=tk.DISABLED)
        # 选项
        opt = tk.Frame(self)
        opt.pack(anchor=tk.W, padx=6)
        self.ts_var = tk.BooleanVar(value=True)
        tk.Checkbutton(opt, text="显示时间戳", variable=self.ts_var, command=self._dummy).pack(side=tk.LEFT)
        tk.Button(opt, text="清空", command=self.clear).pack(side=tk.LEFT, padx=8)

    def _dummy(self):
        pass

    def log(self, msg):
        import datetime
        prefix = ""
        if self.ts_var.get():
            prefix = datetime.datetime.now().strftime("%H:%M:%S ") 
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, prefix + msg + "\n")
        self.txt.config(state=tk.DISABLED)
        self.txt.see(tk.END)

    def clear(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.delete("1.0", tk.END)
        self.txt.config(state=tk.DISABLED)
