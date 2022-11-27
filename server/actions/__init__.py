import sys

match sys.platform:
    case "linux":
        from .linux import *
    case "windows":
        from .windows import *
    case "darwin":
        from .osx import *
    case _:
        raise Exception("OS not supported.")

from .common import *