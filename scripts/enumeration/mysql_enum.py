# scripts/enumeration/mysql_enum.py
import subprocess
from core.db_manager import DBManager

NEEDS_USER_APPROVAL = True  # We'll attempt brute forcing

def enumerate_service(ip, port):
    print(f"[+] Starting MySQL enumeration on {ip}:{port}")
    db = DBManager()

    # 1. Run Nmap scripts for MySQL
    nmap_cmd = ["nmap", "-p", str(port), "--script", "mysql-*", str(ip)]
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"[!] MySQL Nmap enumeration failed: {result.stderr}")
        return

    print(result.stdout)

    # 2. Brute force with Hydra or other tool
    hydra_cmd = ["hydra", "-L", "userlist.txt", "-P", "passlist.txt", f"mysql://{ip}"]
    try:
        hydra_result = subprocess.run(hydra_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if hydra_result.returncode == 0 and "login:" in hydra_result.stdout.lower():
            lines = hydra_result.stdout.splitlines()
            success_lines = [l for l in lines if "[mysql]" in l.lower() and "login:" in l.lower()]
            for line in success_lines:
                db.insert_note(host_ip=ip, service_port=port, note=f"MySQL creds found: {line}")
    except FileNotFoundError:
        print("[!] Hydra not installed or not in PATH.")
