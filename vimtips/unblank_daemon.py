#!/usr/bin/env python3

import itertools
import subprocess
import time
from datetime import date
from .config import config
from . import unblank_check


def main() -> None:
    gui_last_start_by_daemon_date = date.fromtimestamp(config.gui_last_start_by_daemon)
    for _ in itertools.chain(["unblank"], unblank_check.run_unblank_check()):
        if date.today() != gui_last_start_by_daemon_date:
            subprocess.call(config.gui_command)
            config.gui_last_start_by_daemon = time.time()
            gui_last_start_by_daemon_date = date.fromtimestamp(config.gui_last_start_by_daemon)


if __name__ == "__main__":
    main()
