# scripts/enumeration/postgres_enum.py
import subprocess
from core.db_manager import DBManager

NEEDS_USER_APPROVAL = True

def enumerate_service(ip, port):
    print(f"[+] Starting PostgreSQL enumeration on {ip}:{port}")
    db = DBManager()

    # Nmap scripts
    nmap_cmd = ["nmap", "-p", str(port), "--script", "pgsql-*", ip]
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"[!] PostgreSQL Nmap enumeration failed: {result.stderr}")
        return

    output = result.stdout
    print(output)

    # Hydra approach
    hydra_cmd = ["hydra", "-L", "pg_userlist.txt", "-P", "pg_passlist.txt", f"postgres://{ip}"]
    try:
        hydra_result = subprocess.run(hydra_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "login:" in hydra_result.stdout.lower():
            db.insert_note(host_ip=ip, service_port=port, note=f"PostgreSQL brute force success:\n{hydra_result.stdout}")
    except FileNotFoundError:
        print("[!] Hydra not installed or not in PATH.")
