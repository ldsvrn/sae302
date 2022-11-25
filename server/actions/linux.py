import subprocess
import os
import platform

def reboot():
    os.system("reboot now")

def get_version() -> dict:
    ver = platform.freedesktop_os_release()