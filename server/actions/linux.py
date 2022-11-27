import subprocess
import os
import platform
import psutil

def reboot():
    os.system("reboot now")

def shutdown():
    os.system("shutdown -h now")