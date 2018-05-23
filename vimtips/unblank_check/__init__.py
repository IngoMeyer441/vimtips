import os
import pkgutil
import subprocess
from types import ModuleType
from typing import Iterator, List, Optional  # noqa: F401  # pylint: disable=unused-import

__all__ = ['run_unblank_check']

_suitable_plugin = None  # type: Optional[ModuleType]


def _find_suitable_plugin() -> None:
    global _suitable_plugin

    def find_all_plugins() -> List[ModuleType]:
        plugins = []  # type: List[ModuleType]
        for importer, module_name, is_package in pkgutil.iter_modules([os.path.dirname(__file__)]):
            if not module_name.startswith('_'):
                module = importer.find_module(module_name).load_module(module_name)
                if all(
                    hasattr(module, attr) and callable(getattr(module, attr))
                    for attr in ('priority', 'is_suitable_check', 'check_executable')
                ):
                    plugins.append(module)
        return plugins

    def filter_plugins(plugins: List[ModuleType]) -> ModuleType:
        return max(
            (plugin for plugin in plugins if plugin.is_suitable_check()),  # type: ignore
            key=lambda x: x.priority()  # type: ignore
        )

    plugins = find_all_plugins()
    _suitable_plugin = filter_plugins(plugins)


def run_unblank_check() -> Iterator[str]:
    valid_words = ['on', 'unblank', 'wakeup']
    if _suitable_plugin is None:
        _find_suitable_plugin()
    if _suitable_plugin is not None:
        process = subprocess.Popen(
            [_suitable_plugin.check_executable()],  # type: ignore
            stdout=subprocess.PIPE,
            universal_newlines=True
        )
        for stdout_line in iter(process.stdout.readline, ''):
            if stdout_line.strip().lower() in valid_words:
                yield 'unblank'
        return_code = process.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, _suitable_plugin.check_executable())  # type: ignore
