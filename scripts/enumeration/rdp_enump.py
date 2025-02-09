# scripts/enumeration/rdp_enum.py

import subprocess
from core.db_manager import DBManager

def enumerate_service(ip, port):
    """
    Use Nmap RDP scripts and other tools to gather info about RDP services.
    """
    print(f"[+] Starting RDP enumeration on {ip}:{port}")
    db = DBManager()

    # 1. Nmap scripts for RDP
    # Note: Nmap has some rdp-* scripts
    cmd = [
        "nmap", 
        "-p", str(port), 
        "--script", "rdp-enum-encryption,rdp-ntlm-info",  # or "rdp-*"
        ip
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"[!] Nmap RDP enumeration failed: {result.stderr}")
        return

    output = result.stdout
    print(output)

    # Store or parse output for interesting details
    if "RDP Protocol Version" in output:
        db.insert_note(host_ip=ip, service_port=port, note="Detected RDP protocol version info")

    # 2. Additional checks: We could attempt a Hydra brute force if credentials are known or guessed
    # For example:
    # hydra_cmd = ["hydra", "-l", "Administrator", "-P", "passwords.txt", f"rdp://{ip}:{port}"]
    # result = subprocess.run(hydra_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # ...
