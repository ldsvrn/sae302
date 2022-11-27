import psutil
import platform

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
    if platform.system() == 'Linux':
        freedesktop = platform.freedesktop_os_release()
        return {
            'system': freedesktop['PRETTY_NAME'],
            'node': platform.node(),
            'release': platform.release(),
        }
    else:
        return {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
        }