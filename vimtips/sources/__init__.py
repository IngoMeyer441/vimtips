import os
import pkgutil
from types import ModuleType
from typing import List


_plugin_modules = []  # type: List[ModuleType]


def load_all_tips() -> List[str]:
    tips = []  # type: List[str]
    for module in _plugin_modules:
        tips.extend(module.tips())  # type: ignore
    return tips


def _find_plugins() -> None:
    _plugin_modules.clear()
    for importer, module_name, is_package in pkgutil.iter_modules([os.path.dirname(__file__)]):
        if not module_name.startswith('_'):
            module = importer.find_module(module_name).load_module(module_name)
            if hasattr(module, 'tips') and callable(module.tips):
                _plugin_modules.append(module)


_find_plugins()
