import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {'packages': [], 'excludes' : []}
base = 'Win32GUI'
exe = Executable(
    script = 'Battery Scan.py',
    initScript = None,
    base = 'Win32GUI',
    targetName = 'Battery Scan.exe',
    #icon = True
)

setup( name = 'Battery Scan', 
        version = '1.0',
        description = 'Battery Scan',
        options = {'build_exe': build_exe_options},
        executables = [Executable('Battery Scan.py', base = base)])
