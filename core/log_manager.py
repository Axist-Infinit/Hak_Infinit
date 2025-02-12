"""
core/log_manager.py

Sets up a structured JSON logger for the framework.
"""

import logging
import os
import sys
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("hakinfinit")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

file_handler = logging.FileHandler(os.path.join(LOG_DIR, "hakinfinit.log"))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
