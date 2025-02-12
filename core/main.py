"""
core/main.py

Entry point for the HakInfinit framework. Provides CLI argument parsing,
initial setup, and calls the executor to run scans/enumerations.
"""

import sys
import argparse
from core import config_manager
from core import db_manager
from core.executor import Executor
from core.log_manager import logger  # (Newly referenced logging module)
from scripts.nmap.run_nmap import run_nmap_scan
from scripts.nmap.parse_results import parse_nmap_output

def main():
    parser = argparse.ArgumentParser(description="HakInfinit - Automated Enumeration and Vulnerability Framework")
    parser.add_argument('-t', '--targets', nargs='+', help='One or more target IP addresses or hostnames', required=False)
    parser.add_argument('-f', '--file', help='File containing list of targets', required=False)
    parser.add_argument('-s', '--scan', action='store_true', help='Run an Nmap scan on the provided targets')
    parser.add_argument('-p', '--parse', action='store_true', help='Parse existing Nmap output file')
    parser.add_argument('-e', '--enumerate', action='store_true', help='Run enumeration modules on discovered services')
    parser.add_argument('-r', '--report', action='store_true', help='Generate an HTML or Markdown report')
    parser.add_argument('--masscan', action='store_true', help='Use Masscan for large-scale port discovery (new)')

    args = parser.parse_args()

    # Initialize configuration and DB
    config_manager.load_config()
    db_manager.init_db()

    # Construct an Executor instance
    executor = Executor()

    if args.targets or args.file:
        if args.scan:
            # Optionally run Masscan, then Nmap
            if args.masscan:
                logger.info("Running Masscan before Nmap (feature not yet implemented in run_nmap.py).")
                # Future: Implement masscan logic here or in run_nmap.py

            logger.info("Running Nmap scan on provided targets...")
            run_nmap_scan(args.targets, args.file)
        if args.parse:
            logger.info("Parsing existing Nmap output file(s)...")
            # Possibly parse results from a default or user-specified file
            parse_nmap_output("nmap_output.xml")  # Example path
    else:
        logger.info("No targets provided. Skipping scan and parse steps.")

    if args.enumerate:
        logger.info("Running enumeration modules...")
        executor.run_enumeration()

    if args.report:
        logger.info("Generating report (not implemented in detail yet).")
        # Future: Implement reporting logic

if __name__ == "__main__":
    main()
