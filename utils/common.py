# scripts/utils/common.py

import os
import logging
import ipaddress
import subprocess

def setup_logging(log_level=logging.INFO):
    """
    Configures the logging settings for the application.

    :param log_level: The logging level (default: logging.INFO).
    """
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def ensure_directory_exists(directory_path):
    """
    Ensures that the specified directory exists; creates it if it doesn't.

    :param directory_path: The path to the directory.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def is_valid_ip(ip):
    """
    Validates if the provided string is a valid IP address.

    :param ip: The IP address string to validate.
    :return: True if valid, False otherwise.
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def run_subprocess(command):
    """
    Executes a subprocess command and returns the output.

    :param command: The command to execute as a list of arguments.
    :return: The standard output from the command.
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{' '.join(command)}' failed with error: {e}")
        return None
