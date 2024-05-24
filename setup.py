import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"  

options = {
    "build_exe": {
        "packages": ["tkinter", "keyboard", "pyautogui"],
        "include_files": [],
    }
}

executables = [
    Executable("Desstop.py", base=base)
]

setup(
    name="Desstop",
    version="0.2",
    description="An ASCII faced desktop assistant",
    options=options,
    executables=executables
)
