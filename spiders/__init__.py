import pkgutil
import inspect
from typing import Dict

from spiders.base import SpiderBase


def load_spiders():
    spiders = {}
    for loader, name, _ in pkgutil.walk_packages(__path__):
        module = loader.find_module(name).load_module(name)

        for key, value in inspect.getmembers(module):
            globals()[key] = value
            if (
                    inspect.isclass(value)
                    and issubclass(value, SpiderBase)
                    and value is not SpiderBase
            ):
                spiders[value.NAME] = value()

    return spiders


spiders: Dict[str, SpiderBase] = load_spiders()
