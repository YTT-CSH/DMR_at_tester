# -*- coding: utf-8 -*-
"""串口通信封装：连接/断开/发送AT指令/读取响应(超时1s)/处理主动上报。"""
import serial
import serial.tools.list_ports
import threading
import time

# 协议规定：AT指令以 \r (0x0D) 结束；回复超时建议 1s
CR = b"\r"
DEFAULT_TIMEOUT = 1.0
DEFAULT_BAUDRATE = 9600


class SerialComm:
    def __init__(self, on_receive=None, on_status=None):
        """
        on_receive(line): 收到一行数据(已strip)时回调，用于日志/主动上报
        on_status(connected: bool, msg: str): 连接状态变化回调
        """
        self.ser = None
        self.on_receive = on_receive
        self.on_status = on_status
        self._reader = None
        self._running = False
        self.lock = threading.Lock()

    # ---------- 端口枚举 ----------
    @staticmethod
    def list_ports():
        ports = []
        for p in serial.tools.list_ports.comports():
            ports.append(p.device)
        return ports

    # ---------- 连接/断开 ----------
    def connect(self, port, baudrate=DEFAULT_BAUDRATE, timeout=DEFAULT_TIMEOUT):
        if self.ser and self.ser.is_open:
            self.disconnect()
        try:
            self.ser = serial.Serial(
                port=port, baudrate=baudrate, bytesize=8,
                stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE,
                xonxoff=False, rtscts=False, dsrdtr=False, timeout=timeout,
            )
        except Exception as e:
            if self.on_status:
                self.on_status(False, f"打开串口失败: {e}")
            return False
        self._running = True
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()
        if self.on_status:
            self.on_status(True, f"已连接 {port} @ {baudrate}")
        # 连接后自动握手
        self.send("AT+DMOCONNECT", expect_resp=False)
        return True

    def disconnect(self):
        self._running = False
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
            except Exception:
                pass
        self.ser = None
        if self.on_status:
            self.on_status(False, "已断开")

    @property
    def is_open(self):
        return self.ser is not None and self.ser.is_open

    # ---------- 发送 ----------
    def send(self, cmd, expect_resp=True, timeout=DEFAULT_TIMEOUT):
        """
        发送一条 AT 指令（自动补 \r）。
        若 expect_resp 为 True，则等待并返回模块应答行（以 + 开头的首行）。
        模块主动上报(无请求)也通过 on_receive 实时输出，不会在此阻塞。
        """
        if not self.is_open:
            if self.on_status:
                self.on_status(False, "未连接串口")
            return None
        with self.lock:
            # 清空输入缓冲，避免旧数据干扰
            try:
                self.ser.reset_input_buffer()
            except Exception:
                pass
            line = cmd if cmd.endswith("\r") else cmd + "\r"
            self.ser.write(line.encode("ascii", errors="replace"))
            if self.on_receive:
                self.on_receive(">> " + cmd)
            if not expect_resp:
                return None
            # 读取直到出现以 '+' 开头的应答行，或超时
            start = time.time()
            buf = ""
            while time.time() - start < timeout:
                try:
                    if self.ser.in_waiting:
                        raw = self.ser.read(self.ser.in_waiting)
                        text = raw.decode("ascii", errors="ignore")
                        buf += text
                        for part in text.split("\r\n"):
                            part = part.strip()
                            if part.startswith("+"):
                                return part
                        # 有些应答直接以 \r 分隔
                        if "+" in buf:
                            for part in buf.replace("\r", "\n").split("\n"):
                                part = part.strip()
                                if part.startswith("+"):
                                    return part
                except Exception:
                    pass
                time.sleep(0.02)
            return buf.strip() if buf.strip() else None

    # ---------- 后台读取（主动上报） ----------
    def _read_loop(self):
        while self._running and self.ser and self.ser.is_open:
            try:
                if self.ser.in_waiting:
                    raw = self.ser.read(self.ser.in_waiting)
                    text = raw.decode("ascii", errors="ignore")
                    for line in text.replace("\r", "\n").split("\n"):
                        line = line.strip()
                        if line:
                            if self.on_receive:
                                self.on_receive("<< " + line)
                else:
                    time.sleep(0.02)
            except Exception:
                break
