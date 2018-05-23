import os
import platform


def priority():
    return 0


def is_suitable_check():
    return (platform.system() == 'Linux')


def check_executable():
    return os.path.join(os.path.dirname(__file__), 'unblank_check')
