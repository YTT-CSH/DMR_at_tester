# -*- coding: utf-8 -*-
"""顶部串口/型号/连接控件。"""
import tkinter as tk
from tkinter import ttk
from serial_comm import SerialComm, DEFAULT_BAUDRATE
from at_db import MODELS


class SerialBar(tk.Frame):
    def __init__(self, master, comm: SerialComm, on_model_change=None, **kw):
        super().__init__(master, **kw)
        self.comm = comm
        self.on_model_change = on_model_change
        self._build()

    def _build(self):
        pad = {"padx": 4, "pady": 3}

        tk.Label(self, text="串口:").pack(side=tk.LEFT, **pad)
        self.port_var = tk.StringVar()
        self.port_cb = ttk.Combobox(self, textvariable=self.port_var, width=10, state="readonly")
        self.port_cb.pack(side=tk.LEFT, **pad)
        self._refresh_ports()

        tk.Button(self, text="刷新", command=self._refresh_ports).pack(side=tk.LEFT, **pad)

        tk.Label(self, text="波特率:").pack(side=tk.LEFT, **pad)
        self.baud_var = tk.StringVar(value=str(DEFAULT_BAUDRATE))
        self.baud_cb = ttk.Combobox(
            self, textvariable=self.baud_var, width=9, state="readonly",
            values=["2400", "4800", "9600", "19200", "38400", "57600", "115200"],
        )
        self.baud_cb.pack(side=tk.LEFT, **pad)

        self.connect_btn = tk.Button(self, text="连接", width=8, command=self._toggle)
        self.connect_btn.pack(side=tk.LEFT, **pad)

        tk.Label(self, text="  模组型号:").pack(side=tk.LEFT, **pad)
        self.model_var = tk.StringVar(value=MODELS[0])
        self.model_cb = ttk.Combobox(self, textvariable=self.model_var, width=12, state="readonly", values=MODELS)
        self.model_cb.pack(side=tk.LEFT, **pad)
        self.model_cb.bind("<<ComboboxSelected>>", lambda e: self._emit_model())

        self.status_var = tk.StringVar(value="● 未连接")
        self.status_lbl = tk.Label(self, textvariable=self.status_var, fg="red")
        self.status_lbl.pack(side=tk.LEFT, padx=10)

        # 连接状态回调
        self.comm.on_status = self._on_status

    def _refresh_ports(self):
        ports = SerialComm.list_ports()
        self.port_cb["values"] = ports if ports else ["(无串口)"]
        if ports:
            self.port_var.set(ports[0])
        else:
            self.port_var.set("(无串口)")

    def _toggle(self):
        if self.comm.is_open:
            self.comm.disconnect()
        else:
            port = self.port_var.get()
            if not port or port == "(无串口)":
                self.status_var.set("● 请先选择串口")
                return
            try:
                baud = int(self.baud_var.get())
            except ValueError:
                baud = DEFAULT_BAUDRATE
            self.comm.connect(port, baud)

    def _on_status(self, connected, msg):
        if connected:
            self.status_var.set("● " + msg)
            self.status_lbl["fg"] = "green"
            self.connect_btn["text"] = "断开"
        else:
            self.status_var.set("● " + msg)
            self.status_lbl["fg"] = "red"
            self.connect_btn["text"] = "连接"

    def _emit_model(self):
        if self.on_model_change:
            self.on_model_change(self.model_var.get())

    def get_model(self):
        return self.model_var.get()
