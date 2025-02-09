import os
import importlib
import yaml

from core.db_manager import DBManager
from core.config_manager import ConfigManager

class Executor:
    def __init__(self):
        self.config = ConfigManager()
        self.db = DBManager()

    def run_enumeration_for_host(self, host_id, interactive=True):
        """
        Retrieves services for a given host from the DB,
        then runs matching enumeration scripts from tool_mapping.yml.
        If interactive=True, prompt user before running scripts that require user approval.
        """
        host_info = self.db.get_host_by_id(host_id)
        if not host_info:
            print(f"[!] No host found with ID {host_id}")
            return

        # Load the service-to-script mapping
        tool_mapping_file = os.path.join(self.config.get_config_dir(), "tool_mapping.yml")
        if not os.path.isfile(tool_mapping_file):
            print(f"[!] tool_mapping.yml not found at {tool_mapping_file}")
            return

        with open(tool_mapping_file, 'r') as f:
            service_mappings = yaml.safe_load(f) or {}

        # Retrieve all services for this host from DB
        services = self.db.get_services_by_host_id(host_id)
        if not services:
            print(f"[!] No services found for host ID {host_id}.")
            return

        ip_address = host_info['ip_address']
        for service_record in services:
            service_name = service_record['service_name']
            port = service_record['port']
            matched = False

            # Try to match the service name or the port in the tool_mapping
            for mapping_key, mapping_value in service_mappings.items():
                mapped_ports = mapping_value.get('ports', [])
                if (
                    (service_name and service_name == mapping_key)
                    or (port in mapped_ports)
                ):
                    scripts = mapping_value.get('scripts', [])
                    for script in scripts:
                        self.run_script(script, ip_address, port, interactive=interactive)
                    matched = True

            # If not matched by name or port, you might do a fallback or default approach here
            if not matched:
                print(f"[~] No direct mapping found for service={service_name}, port={port}")

    def run_script(self, script_filename, ip_address, port, interactive=True):
        """
        Dynamically imports and runs the enumeration script.
        If the script sets NEEDS_USER_APPROVAL=True, prompt user to proceed if interactive is True.
        """
        script_module_path = f"scripts.enumeration.{script_filename.replace('.py', '')}"
        try:
            module = importlib.import_module(script_module_path)
            if hasattr(module, 'enumerate_service'):
                needs_approval = getattr(module, 'NEEDS_USER_APPROVAL', False)
                if needs_approval and interactive:
                    user_input = input(f"[?] {script_filename} may perform brute force or exploit. Proceed? (y/n): ")
                    if user_input.lower() != 'y':
                        print(f"[!] Skipping {script_filename} due to user choice.")
                        return

                print(f"[+] Running {script_filename} for {ip_address}:{port}")
                module.enumerate_service(ip_address, port)
            else:
                print(f"[!] {script_filename} does not have 'enumerate_service' function.")
        except FileNotFoundError:
            print(f"[!] Script {script_filename} not found.")
        except Exception as e:
            print(f"[!] Failed to run script {script_filename} for {ip_address}:{port} - Error: {e}")
