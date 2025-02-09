# scripts/enumeration/oracle_enum.py
import subprocess
from core.db_manager import DBManager

NEEDS_USER_APPROVAL = True  # Oracle brute forcing can be intensive

def enumerate_service(ip, port):
    print(f"[+] Starting Oracle DB enumeration on {ip}:{port}")
    db = DBManager()

    # Nmap scripts
    nmap_cmd = ["nmap", "-p", str(port), "--script", "oracle-sid-brute,oracle-tns-version,oracle-brute", ip]
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"[!] Oracle Nmap scripts failed: {result.stderr}")
        return

    output = result.stdout
    print(output)
    
    # Potential TNSCMD or additional brute force can be done here
