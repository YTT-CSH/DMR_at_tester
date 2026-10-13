# -*- coding: utf-8 -*-
"""
无 GUI 的硬件冒烟测试脚本（命令行版）。
用法：
    python test_at.py [COM端口] [波特率]
示例：
    python test_at.py COM4 9600
"""
import sys
import serial
import time

CR = b"\r"
TIMEOUT = 1.5

# 想要测试的指令列表：(指令字串, 期望前缀)
# "expect" 用于校验应答是否以某字符串开头，空串表示只需收到非空应答即可
TESTS = [
    ("AT+DMOCONNECT",          "+DMOCONNECT"),
    ("AT+DMOGETSOFTVERSION",   "+DMOGETSOFTVERSION"),
    ("AT+DMOGETCHIPID",        "+DMOGETCHIPID"),
    ("AT+DMOGETCURRCH",        "+DMOGETCURRCH"),
    ("AT+DMORDRSSI",           "+DMORDRSSI"),
    ("AT+DMOGETRXBER",         "+DMOGETRXBER"),
    ("AT+DMOGETPWRSAVEINFO",   "+DMOGETPWRSAVEINFO"),
    ("AT+DMOGETVAFC",          "+DMOGETVAFC"),
    ("AT+DMOGETRSSIPARAM",     "+DMOGETRSSIPARAM"),
    ("AT+DMOGETLNAOFFS",       "+DMOGETLNAOFFS"),
    ("AT+DMOGETFREQBANDNUM",   "+DMOGETFREQBANDNUM"),
    ("AT+DMOGETCHFREQ=0",      "+DMOGETCHFREQ"),
]


def send_one(ser, cmd):
    ser.reset_input_buffer()
    ser.write((cmd + "\r").encode("ascii", errors="replace"))
    start = time.time()
    buf = ""
    while time.time() - start < TIMEOUT:
        if ser.in_waiting:
            raw = ser.read(ser.in_waiting)
            buf += raw.decode("ascii", errors="ignore")
            for line in buf.replace("\r", "\n").split("\n"):
                line = line.strip()
                if line.startswith("+"):
                    return line, True
        else:
            time.sleep(0.03)
    return buf.strip() if buf.strip() else None, False


def main():
    port = sys.argv[1] if len(sys.argv) > 1 else "COM4"
    baud = int(sys.argv[2]) if len(sys.argv) > 2 else 9600
    print(f"打开 {port} @ {baud} ...")
    try:
        ser = serial.Serial(port, baud, bytesize=8, stopbits=1, parity=0, timeout=TIMEOUT)
    except Exception as e:
        print(f"[失败] 无法打开串口: {e}")
        return
    print(f"已连接 {port}  固件版本待查询\n")
    ok = 0
    fail = 0
    for cmd, expect in TESTS:
        resp, got = send_one(ser, cmd)
        tag = "OK" if (got and resp.startswith(expect)) else "FAIL"
        if tag == "OK":
            ok += 1
        else:
            fail += 1
        print(f"[{tag}] {cmd}")
        print(f"       -> {resp}")
        print()
    ser.close()
    print(f"结果: {ok} 通过 / {fail} 失败 / 共 {len(TESTS)} 条")


if __name__ == "__main__":
    main()
