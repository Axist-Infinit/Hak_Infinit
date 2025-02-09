#!/usr/bin/env python3
import sys
import os
import time

# Example imports (adjust based on your actual modules)
# from core.config_manager import ConfigManager
# from core.db_manager import DBManager
# from scripts.nmap.run_nmap import run_nmap_scan
# from scripts.nmap.parse_results import parse_nmap_output
# from core.executor import Executor
# from scripts.vulnerability.searchsploit_integration import searchsploit_query
# from scripts.vulnerability.vulndb_integration import query_vulndb

def main_menu():
    while True:
        print("\n=== Hak.Infinit Framework ===")
        print("1. Configure/Verify Database")
        print("2. Run Nmap Scan")
        print("3. Parse Nmap Results")
        print("4. Run Enumeration Scripts")
        print("5. Check for Vulnerabilities (SearchSploit/VulnDB)")
        print("6. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            configure_database()
        elif choice == "2":
            nmap_scan_menu()
        elif choice == "3":
            parse_nmap_results()
        elif choice == "4":
            run_enumerations()
        elif choice == "5":
            vulnerability_lookup_menu()
        elif choice == "6":
            print("Exiting Hak.Infinit. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select from the menu.")

def configure_database():
    print("\n[+] Configuring/Verifying Database...")
    # db = DBManager(ConfigManager().get_db_config())
    # Example logic:
    # db.test_connection()
    # db.apply_migrations()
    print("[+] Done configuring the database!")

def nmap_scan_menu():
    print("\n=== Nmap Scan Menu ===")
    target = input("Enter the target IP/domain (e.g. 192.168.1.10): ")
    scan_type = input("Enter scan type (e.g. -sV, -A, custom flags): ")
    print(f"[+] Running Nmap scan on {target} with flags: {scan_type}")
    # run_nmap_scan(target, scan_type)
    # Save results to DB
    print("[+] Nmap scan completed and results saved to the database.")

def parse_nmap_results():
    print("\n[+] Parsing Nmap results...")
    # parse_nmap_output()
    print("[+] Parsing complete. Data updated in the database.")

def run_enumerations():
    print("\n[+] Running Enumeration Scripts...")
    # Executor().run_enumerations_for_all_services()
    print("[+] Enumerations completed and saved to the database.")

def vulnerability_lookup_menu():
    print("\n=== Vulnerability Lookup Menu ===")
    print("1. SearchSploit")
    print("2. VulnDB")
    print("3. Return to Main Menu")
    choice = input("Enter your choice: ")

    if choice == "1":
        term = input("Enter search term (e.g., 'vsftpd'): ")
        print(f"[+] Running SearchSploit for {term}")
        # searchsploit_query(term)
    elif choice == "2":
        cve_id = input("Enter CVE or keyword to query (e.g., 'CVE-2012-XXXX'): ")
        print(f"[+] Querying VulnDB for {cve_id}")
        # query_vulndb(cve_id)
    else:
        return

if __name__ == "__main__":
    main_menu()
