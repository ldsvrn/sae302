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


# check shlex.split() for security https://docs.python.org/3/library/shlex.html#shlex.split
# FIXME: stderr is not returned WHY im giving up at this point
# TODO: return smth for mkdir???
def send_command(command: str, shell: str = "default"):
    # this is kind of dangerous
    if (shell == "default" and sys.platform == "win32") or shell == "dos":
        p = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                encoding="cp850",
            )
        # here it is a subprocess.CompletedProcess
        out, err = "", ""
        out= p.stdout.read().decode().rstrip() if p.stdout != None else ""
        err= p.stderr.read().decode().rstrip() if p.stderr != None else ""
        return f"{out}{err}"
    elif shell == "default" and sys.platform in ("linux", "darwin"):
        p = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
            )
        # here it is a subprocess.CompletedProcess
        out, err = "", ""
        out= p.stdout.read().decode().rstrip() if p.stdout != None else ""
        err= p.stderr.read().decode().rstrip() if p.stderr != None else ""
        return f"{out}{err}"
    elif shell == "bash":
        p = subprocess.Popen(
                f"/bin/bash -c '{command}'",
                shell=True,
                stdout=subprocess.PIPE,
            )
        # here it is a subprocess.CompletedProcess
        out, err = "", ""
        out= p.stdout.read().decode().rstrip() if p.stdout != None else ""
        err= p.stderr.read().decode().rstrip() if p.stderr != None else ""
        return f"{out}{err}"
    #FIXME: powershell just returns the command
    elif shell == "powershell":
        p = subprocess.Popen(
                f"powershell.exe '{command}'",
                shell=True,
                stdout=subprocess.PIPE,
            )
        out, err = "", ""
        out= p.stdout.read().decode().rstrip() if p.stdout != None else ""
        err= p.stderr.read().decode().rstrip() if p.stderr != None else ""
        return f"{out}{err}"


if __name__ == "__main__":
    print(get_all())
