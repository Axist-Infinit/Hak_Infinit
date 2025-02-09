# scripts/enumeration/mssql_enum.py
import subprocess
from core.db_manager import DBManager

NEEDS_USER_APPROVAL = True

def enumerate_service(ip, port):
    print(f"[+] Starting MSSQL enumeration on {ip}:{port}")
    db = DBManager()

    # Nmap MSSQL scripts
    nmap_cmd = ["nmap", "-p", str(port), "--script", "ms-sql-info,ms-sql-config,ms-sql-tables", ip]
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"[!] MSSQL Nmap enumeration failed: {result.stderr}")
        return

    output = result.stdout
    print(output)

    # Hydra brute force for 'sa' or other known users
    hydra_cmd = ["hydra", "-l", "sa", "-P", "common_passwords.txt", f"mssql://{ip}:{port}"]
    try:
        hydra_result = subprocess.run(hydra_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "login:" in hydra_result.stdout.lower():
            db.insert_note(host_ip=ip, service_port=port, note="Possible SA credentials found via Hydra brute force.")
    except FileNotFoundError:
        print("[!] Hydra not installed or not in PATH.")
