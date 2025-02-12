"""
core/executor.py

Logic to orchestrate which enumeration scripts to run based on DB data or configuration.
"""

import os
from core import db_manager
from core.log_manager import logger
from core.config_manager import get_config_value
from scripts.utils.common import load_tool_mapping
from core.plugin_loader import load_plugins  # (New file referenced)

class Executor:
    def __init__(self):
        self.tool_mapping = load_tool_mapping(os.path.join('config', 'tool_mapping.yml'))
        # Load all enumeration plugins
        self.plugins = load_plugins()

    def run_enumeration(self):
        """
        Orchestrate enumeration by reading discovered services from the DB 
        and matching them with known enumeration scripts or plugins.
        """
        hosts = db_manager.get_all_hosts()
        if not hosts:
            logger.info("No hosts found in DB. Make sure you have parsed Nmap results.")
            return

        for host in hosts:
            host_id = host['id']
            logger.info(f"Running enumeration for Host: {host['ip']} (id={host_id})")
            services = db_manager.get_services_for_host(host_id)
            
            for svc in services:
                service_name = svc['service_name'].lower()
                port = svc['port']
                protocol = svc['protocol']
                
                # Check the tool_mapping to see if we have a recommended script
                # e.g., HTTP => http_enum.py
                script_name = self.tool_mapping.get(service_name)
                if script_name:
                    logger.info(f"Enumerating {service_name} on port {port}")
                    self._execute_enumeration_script(script_name, host, svc)

                # Additionally, check plugin-based enumeration
                for plugin in self.plugins:
                    if plugin.SERVICE_NAME == service_name:
                        logger.info(f"Running plugin '{plugin.__name__}' for service {service_name}")
                        plugin.run(host, svc)

    def _execute_enumeration_script(self, script_name, host, svc):
        """
        Dynamically import and run a specific enumeration script by name.
        """
        try:
            mod_path = f"scripts.enumeration.{script_name.replace('.py','')}"
            mod = __import__(mod_path, fromlist=[None])
            if hasattr(mod, 'run'):
                mod.run(host, svc)
            else:
                logger.warning(f"No 'run' function found in {script_name}.")
        except Exception as e:
            logger.error(f"Failed to run script {script_name}: {e}")
