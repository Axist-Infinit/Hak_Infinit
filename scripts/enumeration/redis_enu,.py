# scripts/enumeration/redis_enum.py
import subprocess
from core.db_manager import DBManager

NEEDS_USER_APPROVAL = False  # Usually checking for open Redis doesn't need brute force

def enumerate_service(ip, port):
    print(f"[+] Starting Redis enumeration on {ip}:{port}")
    db = DBManager()

    # Nmap script
    nmap_cmd = ["nmap", "-p", str(port), "--script", "redis-info", ip]
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"[!] Redis Nmap enumeration failed: {result.stderr}")
        return

    output = result.stdout
    print(output)

    # If "redis-version:" found, store it
    if "redis-version:" in output.lower():
        db.insert_note(host_ip=ip, service_port=port, note=f"Redis version detected:\n{output}")
