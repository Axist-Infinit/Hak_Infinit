"""
core/config_manager.py

Reads configuration files (like database.ini, framework.ini) 
and provides access to configuration details.
"""

import configparser
import os
from core.log_manager import logger

_config = None
_db_config = {}

def load_config():
    global _config
    if _config is not None:
        return  # Already loaded
    
    # Assume config/database.ini for DB and config/framework.ini for general
    db_ini_path = os.path.join('config', 'database.ini')
    framework_ini_path = os.path.join('config', 'framework.ini')
    
    _config = configparser.ConfigParser()

    # Load DB config
    if os.path.exists(db_ini_path):
        db_parser = configparser.ConfigParser()
        db_parser.read(db_ini_path)
        _db_config['dbname'] = db_parser.get('postgresql', 'dbname')
        _db_config['user'] = db_parser.get('postgresql', 'user')
        _db_config['password'] = db_parser.get('postgresql', 'password')
        _db_config['host'] = db_parser.get('postgresql', 'host')
        _db_config['port'] = db_parser.get('postgresql', 'port')
        logger.info("Database config loaded.")
    else:
        logger.warning(f"Database config not found at {db_ini_path}")

    # Load framework config
    if os.path.exists(framework_ini_path):
        _config.read(framework_ini_path)
        logger.info("Framework config loaded.")
    else:
        logger.warning(f"Framework config not found at {framework_ini_path}")

def get_db_config():
    return _db_config

def get_config_value(section, key):
    if _config and _config.has_option(section, key):
        return _config.get(section, key)
    return None
