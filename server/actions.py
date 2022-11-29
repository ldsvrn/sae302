import psutil
import platform
import sys
import os
import subprocess
import shlex


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
        "total": dict["total"],
        "used": dict["used"],
        "free": dict["free"],
        "percent": dict["percent"],
    }


def get_disk_usage():
    dict = psutil.disk_usage("/")._asdict()

    return {
        "total": dict["total"],
        "used": dict["used"],
        "free": dict["free"],
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
    if sys.platform == "linux":
        return (
            subprocess.Popen(
                "ip a | grep inet | grep global | awk '{print $2}'",
                shell=True,
                stdout=subprocess.PIPE,
            )
            .stdout.read()
            .decode()
            .rstrip()
            .split("\n")
        )
    elif sys.platform == "darwin":
        # IPs with broadcast address = local IPs i guess??
        return (
            subprocess.Popen(
                "ifconfig | grep inet | grep broadcast | awk '{print $2}'",
                shell=True,
                stdout=subprocess.PIPE,
            )
            .stdout.read()
            .decode()
            .rstrip()
            .split("\n")
        )
    elif sys.platform == "win32":
        # TODO: parse ipconfig output
        return (
            subprocess.Popen(
                "ipconfig",
                shell=True,
                stdout=subprocess.PIPE,
            )
            .stdout.read()
            .decode()
            .rstrip()
        )

# check shlex.split() for security https://docs.python.org/3/library/shlex.html#shlex.split
# TODO: stderr is not returned, this is a problem when the command is not found
def send_command(command: str, shell: str = "default"):
    # this is kind of dangerous
    if shell == "default" or shell == "dos":
        return (
            subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
            )
            # here it is a subprocess.CompletedProcess
            .stdout.read()
            .decode()
            .rstrip()
        )
        # TODO:check if i need to use a list of args
    elif shell == "bash":
        return (
            subprocess.Popen(
                f"/bin/bash -c '{command}'",
                shell=True,
                stdout=subprocess.PIPE,
            )
            # here it is a subprocess.CompletedProcess
            .stdout.read()
            .decode()
            .rstrip()
        )
    elif shell == "powershell":
        return (
            subprocess.Popen(
                f"powershell.exe '{command}'",
                shell=True,
                stdout=subprocess.PIPE,
            )
            # here it is a subprocess.CompletedProcess
            .stdout.read()
            .decode()
            .rstrip()
        )