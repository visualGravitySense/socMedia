import platform
import config


def detect_system():
    platform_type = platform.system()
    if platform_type == 'Windows':
        return platform_type
    else:
        return 'Linux'


