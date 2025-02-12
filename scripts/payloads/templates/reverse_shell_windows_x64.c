"""
scripts/utils/common.py

Common helper functions for the HakInfinit framework.

Changelog:
- Removed any references to msfvenom-based payload generation.
- Added a new 'generate_payload' method that leverages our custom PayloadGenerator
  from scripts/payloads/payload_generator.py.

Functions:
    - setup_logging
    - ensure_directory_exists
    - is_valid_ip
    - run_subprocess
    - generate_payload (NEW custom generator, NOT using msfvenom!)
"""

import os
import logging
import ipaddress
import subprocess

from scripts.payloads.payload_generator import PayloadGenerator

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
    Executes a subprocess command and returns the standard output.

    :param command: The command to execute as a list of arguments.
    :return: The standard output from the command, or None if there's an error.
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{' '.join(command)}' failed with error: {e}")
        return None

def generate_payload(
    payload_type="reverse_shell",
    target_os="linux",
    arch="x64",
    lhost="127.0.0.1",
    lport=4444,
    output_format=None,
    outfile=None
):
    """
    Generates a custom payload using our internal C-compiler-based approach.
    
    Example usage:
        generate_payload(
            payload_type="reverse_shell",
            target_os="windows",
            arch="x64",
            lhost="192.168.1.10",
            lport=4444,
            output_format="exe",
            outfile="payloads/my_rev_shell.exe"
        )

    :param payload_type: e.g., "reverse_shell", "bind_shell"
    :param target_os: "linux" or "windows" (extendable)
    :param arch: "x64" or "x86"
    :param lhost: IP for reverse shell callbacks
    :param lport: Port for reverse shell callbacks
    :param output_format: "exe" for Windows, "elf" for Linux, etc. If None, defaults automatically.
    :param outfile: Where to save the final compiled payload. If None, we auto-generate a name.
    :return: The path to the generated payload or None if it fails.
    """

    # Default the output format if not specified
    if not output_format:
        output_format = "exe" if target_os == "windows" else "elf"

    generator = PayloadGenerator(
        lhost=lhost,
        lport=lport,
        target_os=target_os,
        output_format=output_format,
        arch=arch
    )

    # Return the path to the compiled payload
    return generator.generate(payload_type=payload_type, outfile=outfile)
