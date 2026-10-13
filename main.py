# -*- coding: utf-8 -*-
"""
力同 A6 平台 DMR 模组 AT 指令测试工具（教学版）
主入口：组装 顶部串口栏 + 中间指令面板 + 底部日志
"""
import tkinter as tk
from tkinter import ttk

from serial_comm import SerialComm
from ui.serial_bar import SerialBar
from ui.cmd_panel import CmdPanel
from ui.log_panel import LogPanel


def main():
    root = tk.Tk()
    root.title("DMR 模组 AT 指令测试工具 (力同 A6 平台) - 教学版")
    root.geometry("1100x720")

    # 串口通信对象（接收回调导向日志）
    log = LogPanel(root)

    def on_receive(line):
        log.log(line)

    comm = SerialComm(on_receive=on_receive)

    # 顶部串口栏
    serial_bar = SerialBar(root, comm, on_model_change=lambda m: cmd_panel.set_model(m))
    serial_bar.pack(side=tk.TOP, fill=tk.X)

    # 中间指令面板
    cmd_panel = CmdPanel(root, comm, log_fn=log.log)
    cmd_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=4, pady=4)

    # 底部日志
    log.pack(side=tk.BOTTOM, fill=tk.X)

    log.log("就绪。请选择串口与模组型号后点击【连接】。")
    log.log("提示：连接后会自动发送 AT+DMOCONNECT 握手；模块上电会主动上报 +DMOGETSTARTUP。")

    root.mainloop()


if __name__ == "__main__":
    main()
