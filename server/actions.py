import psutil
import platform
import sys
import os
import subprocess
import shlex
from socket import AF_INET
from ipaddress import IPv4Network


def reboot():
    if sys.platform == "win32":
        os.system("shutdown /r /t 0")
    else:
        os.system("reboot -h now")


def shutdown():
    if sys.platform == "win32":
        os.system("shutdown /t 0")
    else:
        os.system("shutdown -h now")


def get_cpu_usage():
    return psutil.cpu_percent()


def get_memory_usage():
    dict = psutil.virtual_memory()._asdict()

    return {
        "total": round(dict["total"] / 1_073_741_824, 2),
        "used": round(dict["used"] / 1_073_741_824, 2),
        # TODO: Il en manque tjs un peu... faire total - used?
        "free": round((dict["available"] + dict["free"]) / 1_073_741_824, 2),
        "percent": dict["percent"],
    }


def get_disk_usage():
    dict = psutil.disk_usage("/")._asdict()

    return {
        "total": round(dict["total"] / 1_073_741_824, 2),
        "used": round(dict["used"] / 1_073_741_824, 2),
        "free": round(dict["free"] / 1_073_741_824, 2),
        "percent": dict["percent"],
    }


def get_os_info():
    if sys.platform == "linux":
        freedesktop = platform.freedesktop_os_release()
        return {
            "node": platform.node(),
            "system": f"{freedesktop['PRETTY_NAME']} (Linux)",
            "release": platform.release(),
        }
    else:
        return {
            "node": platform.node(),
            "system": platform.system(),
            "release": platform.release(),
        }


def get_ip():
    ipaddresses = []
    for nic, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            address = addr.address
            # Ingore garbage addresses on Windows
            if addr.family == AF_INET and not address.startswith("169.254"):
                ipaddresses.append(
                    f"{address}/{IPv4Network('0.0.0.0/' +  addr.netmask).prefixlen}"
                )
    return ipaddresses


def get_all():
    return {
        "os": get_os_info(),
        "cpu": get_cpu_usage(),
        "mem": get_memory_usage(),
        "disk": get_disk_usage(),
        "ip": get_ip(),
    }


# TODO: append the response to a success string so the client knows when a no output command is successful
def send_command(command: str, shell: str = "default"):
    # this is kind of dangerous
    ret = ""
    if (shell == "default" and sys.platform == "win32") or shell == "dos":
        p = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="cp850",
            )
        out= p.stdout.read().rstrip()
        err= p.stderr.read().rstrip()
        ret = f"{out}{err}"
    elif shell == "default" and sys.platform in ("linux", "darwin"):
        p = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
            )
        out= p.stdout.read().rstrip()
        err= p.stderr.read().rstrip()
        ret = f"{out}{err}"
    elif shell == "bash":
        p = subprocess.Popen(
                f"/bin/bash -c '{command}'",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8"
            )
        out= p.stdout.read().rstrip()
        err= p.stderr.read().rstrip()
        ret = f"{out}{err}"
    #FIXME: powershell just returns the command
    elif shell == "powershell":
        p = subprocess.Popen(
                f'powershell.exe "{command}"',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8"
            )
        out= p.stdout.read().rstrip()
        err= p.stderr.read().rstrip()
        ret = f"{out}{err}"

    # we add some text at the end to let the user know the command has been executed
    return ret + f"\nCommand {command} executed."

if __name__ == "__main__":
    print(get_all())
