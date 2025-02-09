# scripts/enumeration/vnc_enum.py
import subprocess
from core.db_manager import DBManager

NEEDS_USER_APPROVAL = True  # Brute forcing VNC is intrusive

def enumerate_service(ip, port):
    print(f"[+] Starting VNC enumeration on {ip}:{port}")
    db = DBManager()

    # Nmap scripts
    nmap_cmd = ["nmap", "-p", str(port), "--script", "vnc-info,vnc-title", ip]
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"[!] VNC Nmap enumeration failed: {result.stderr}")
        return

    print(result.stdout)

    # Example Hydra brute force
    hydra_cmd = ["hydra", "-P", "vnc_passlist.txt", f"vnc://{ip}:{port}"]
    try:
        hydra_result = subprocess.run(hydra_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "host:" in hydra_result.stdout.lower():
            db.insert_note(host_ip=ip, service_port=port, note=f"VNC brute force success:\n{hydra_result.stdout}")
    except FileNotFoundError:
        print("[!] Hydra not installed or not in PATH.")
