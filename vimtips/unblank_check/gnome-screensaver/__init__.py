import os
import psutil


def priority():
    return 1


def is_suitable_check():
    return any(proc.info["name"] == "gnome-screensaver" for proc in psutil.process_iter(attrs=["name"]))


def check_executable():
    return os.path.join(os.path.dirname(__file__), "unblank_check.sh")
