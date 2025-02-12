"""
core/console.py

Provides an interactive CLI for listing hosts, services, running modules, etc.
Similar to Metasploit's msfconsole (very simplified).
"""

import cmd
from core import db_manager
from core.executor import Executor

class HakInfinitConsole(cmd.Cmd):
    intro = "Welcome to the HakInfinit console. Type help or ? to list commands.\n"
    prompt = "(hakinfinit) "

    def __init__(self):
        super().__init__()
        self.executor = Executor()

    def do_hosts(self, arg):
        "List all discovered hosts: hosts"
        hosts = db_manager.get_all_hosts()
        if not hosts:
            print("No hosts in DB.")
            return
        for h in hosts:
            print(f"ID={h['id']}, IP={h['ip']}, Hostname={h['hostname']}")

    def do_services(self, arg):
        "List services for a given host ID: services <host_id>"
        args = arg.split()
        if not args:
            print("Usage: services <host_id>")
            return
        host_id = args[0]
        services = db_manager.get_services_for_host(host_id)
        if not services:
            print("No services found for that host.")
            return
        for s in services:
            print(f"Port={s['port']}, Protocol={s['protocol']}, Service={s['service_name']}, Version={s['version']}")

    def do_enumerate(self, arg):
        "Run enumeration across all hosts in DB: enumerate"
        self.executor.run_enumeration()

    def do_quit(self, arg):
        "Exit the console"
        return True

def main():
    console = HakInfinitConsole()
    console.cmdloop()

if __name__ == "__main__":
    main()
