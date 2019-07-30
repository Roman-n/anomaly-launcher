import sys
from cx_Freeze import setup, Executable

setup(
    name = "Anomaly Launcher",
    version = "1",
    description = "Anomaly's quick launcher.",
    executables = [Executable("main.py", base = "Win32GUI")])