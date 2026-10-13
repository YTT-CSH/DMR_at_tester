@echo off
REM DMR 模组 AT 测试工具启动脚本
REM 优先使用已装好 pyserial 的 Python 3.14 解释器；如需分发请改用 PyInstaller 打包成 exe
set PY="C:\Users\csh-8\AppData\Local\Python\pythoncore-3.14-64\python.exe"
if not exist %PY% set PY=python
%PY% "%~dp0main.py"
if errorlevel 1 pause
