"""
core/plugin_loader.py

Dynamic plugin loading mechanism.
Scans a directory (e.g. scripts/enumeration/plugins) for Python modules 
that implement a 'SERVICE_NAME' attribute and a 'run(host, service)' function.
"""

import importlib
import pkgutil
import os

def load_plugins():
    plugin_folder = 'scripts.enumeration.plugins'
    plugins = []
    
    try:
        package = importlib.import_module(plugin_folder)
    except ImportError:
        # If the plugin folder doesn't exist or is empty
        return plugins
    
    for loader, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{plugin_folder}.{module_name}"
        mod = importlib.import_module(full_module_name)
        # We assume each plugin has at least: SERVICE_NAME, run(host, service)
        if hasattr(mod, 'SERVICE_NAME') and hasattr(mod, 'run'):
            plugins.append(mod)
    return plugins
