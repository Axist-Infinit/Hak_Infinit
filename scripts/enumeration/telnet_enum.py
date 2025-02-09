# scripts/enumeration/telnet_enum.py
import subprocess
from core.db_manager import DBManager

NEEDS_USER_APPROVAL = True  # Brute forcing telnet can be intrusive

def enumerate_service(ip, port):
    print(f"[+] Starting Telnet enumeration on {ip}:{port}")
    db = DBManager()

    # Nmap scripts for Telnet
    nmap_cmd = ["nmap", "-p", str(port), "--script", "telnet-encryption,telnet-ntlm-info", ip]
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"[!] Nmap Telnet enumeration failed: {result.stderr}")
        return

    print(result.stdout)

    # Hydra brute force
    hydra_cmd = ["hydra", "-L", "common_users.txt", "-P", "common_passwords.txt", f"telnet://{ip}"]
    try:
        hydra_result = subprocess.run(hydra_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "login:" in hydra_result.stdout.lower():
            db.insert_note(host_ip=ip, service_port=port, note=f"Telnet brute forced:\n{hydra_result.stdout}")
    except FileNotFoundError:
        print("[!] Hydra not installed or not in PATH.")
