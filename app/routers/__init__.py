from pkgutil import walk_packages
from importlib import import_module

all_router = [
    import_module(f"{__name__}.{module.name}").router
    for module in walk_packages(__path__)
]
