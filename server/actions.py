import psutil
import platform
import sys
import os

def reboot():
    if sys.platform == "windows":
        os.system("shutdown /r /t 0")
    else:
        os.system("reboot -h now")

def shutdown():
    if sys.platform == "windows":
        os.system("shutdown /t 0")
    else:
        os.system("shutdown -h now")


def get_cpu_usage():
    return psutil.cpu_percent()


def get_memory_usage():
    dict = psutil.virtual_memory()._asdict()

    return {
        'total': dict['total'],
        'used': dict['used'],
        'free': dict['free'],
        'percent': dict['percent']
    }


def get_disk_usage():
    dict = psutil.disk_usage('/')._asdict()

    return {
        'total': dict['total'],
        'used': dict['used'],
        'free': dict['free'],
        'percent': dict['percent']
    }


def get_os_info():
    if sys.platform == 'linux':
        freedesktop = platform.freedesktop_os_release()
        return {
            'node': platform.node(),
            'system': f"{freedesktop['PRETTY_NAME']} (Linux)",
            'release': platform.release(),
        }
    else:
        return {
            'node': platform.node(),
            'system': platform.system(),
            'release': platform.release(),
        }
