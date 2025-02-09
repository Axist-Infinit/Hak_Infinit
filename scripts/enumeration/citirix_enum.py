# scripts/enumeration/citrix_enum.py
import subprocess
from core.db_manager import DBManager

NEEDS_USER_APPROVAL = False  # Basic enumeration

def enumerate_service(ip, port):
    print(f"[+] Starting Citrix enumeration on {ip}:{port}")
    db = DBManager()

    # Potential Nmap scripts or custom checks for Citrix Gateway
    nmap_cmd = ["nmap", "-p", str(port), "--script", "http-citrix-enumapps", ip]
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"[!] Citrix Nmap enumeration failed: {result.stderr}")
        return

    output = result.stdout
    print(output)

    if "CITRIX" in output.upper():
        db.insert_note(host_ip=ip, service_port=port, note="Citrix environment discovered.")
