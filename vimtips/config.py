import os
from configparser import ConfigParser
from typing import Any, Dict, Optional, TextIO, Union  # noqa: F401  # pylint: disable=unused-import

DEFAULT_CONFIG_FILENAME = os.path.expanduser('~/.vimtips.conf')


class Config:
    _default_config = {
        'gui': {
            'command': 'vimtips-gui',
            'last_start_by_daemon': 0.0
        }
    }  # type: Dict[str, Dict[str, Any]]

    def __init__(self, config_filename: str = DEFAULT_CONFIG_FILENAME) -> None:
        self._config_filename = config_filename
        self._config = ConfigParser()
        self._config.read_dict(self._default_config)
        self.read_config()

    def read_config(self, config_filename: Optional[str] = None) -> None:
        if config_filename is None:
            config_filename = self._config_filename
        self._config.read(config_filename)

    def write_config(self, config_filename: Optional[str] = None) -> None:
        if config_filename is None:
            config_filename = self._config_filename
        with open(config_filename, 'w') as f:
            self._config.write(f)

    @property
    def gui_command(self) -> str:
        return self._config['gui']['command']

    @property
    def gui_last_start_by_daemon(self) -> float:
        return float(self._config['gui']['last_start_by_daemon'])

    @gui_last_start_by_daemon.setter
    def gui_last_start_by_daemon(self, value: float) -> None:
        self._config['gui']['last_start_by_daemon'] = str(value)
        self.write_config()


config = Config()
