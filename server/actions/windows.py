import subprocess
import os

def reboot():
    os.system("shutdown /r /t 0")

def shutdown():
    os.system("shutdown /t 0")