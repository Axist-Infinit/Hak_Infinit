"""
scripts/nmap/run_nmap.py

Runs an Nmap scan on a target (or targets) and stores XML output.
- Preserves robust default arguments from the old script.
- Integrates second-pass UDP scan if enabled in config.
- Uses structured logging from core.log_manager.
"""

import subprocess
import os
from core.log_manager import logger
from core.config_manager import get_config_value  # or use any updated config approach

def run_nmap_scan(
    target: str,
    output_xml_path: str = "nmap_output.xml",
    additional_args: list = None
) -> str:
    """
    Run an Nmap scan on the target, store XML output, and (optionally) run a second pass for UDP.
    
    :param target: Single target (IP/hostname). 
    :param output_xml_path: Path to save the primary XML output.
    :param additional_args: Optional list of additional Nmap arguments.
    :return: The path to the XML file if successful, or None on error.
    """

    # Provide robust defaults if none supplied
    if additional_args is None:
        additional_args = [
            "-sC",  # default scripts
            "-sV",  # version detection
            "-O",   # OS detection
            "-p-",  # scan all TCP ports
            "-T4",  # faster timing
            "--max-retries", "2",
            "-oX", output_xml_path
        ]

    # Build the final Nmap command
    nmap_cmd = ["nmap"] + additional_args + [target]
    logger.info(f"Running Nmap command: {' '.join(nmap_cmd)}")

    try:
        # Run the Nmap scan
        result = subprocess.run(
            nmap_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check for errors
        if result.returncode != 0:
            logger.error(f"Nmap scan failed with error:\n{result.stderr}")
            return None

        logger.info(f"Nmap scan (TCP) completed successfully. Results saved to {output_xml_path}")

        # Optional second pass for UDP
        # Assuming you have a config.ini or similar with:
        # [Nmap]
        # udp_scan = true
        udp_scan = get_config_value("Nmap", "udp_scan")
        if udp_scan and udp_scan.lower() == "true":
            # Run an additional UDP scan
            udp_output_xml = output_xml_path.replace(".xml", "_udp.xml")
            udp_cmd = [
                "nmap",
                "-sU",
                "-p-",
                "-T4",
                "--max-retries", "2",
                "-oX", udp_output_xml,
                target
            ]
            logger.info(f"Running additional UDP scan: {' '.join(udp_cmd)}")

            udp_result = subprocess.run(
                udp_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if udp_result.returncode != 0:
                logger.warning(f"UDP scan failed:\n{udp_result.stderr}")
            else:
                logger.info(f"UDP scan completed successfully. Results saved to {udp_output_xml}")

        return output_xml_path

    except FileNotFoundError:
        logger.error("Nmap not found. Please ensure it is installed and in your PATH.")
        return None
    except Exception as e:
        logger.error(f"Exception occurred while running Nmap: {str(e)}")
        return None
