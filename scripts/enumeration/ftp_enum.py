# scripts/enumeration/ftp_enum.py
import subprocess
from core.db_manager import DBManager

# Suppose this script *can* do brute forcing, so we set approval flag
NEEDS_USER_APPROVAL = True

def enumerate_service(ip, port):
    print(f"[+] Starting FTP enumeration on {ip}:{port}")
    db = DBManager()

    # Passive enumeration with Nmap scripts
    nmap_cmd = [
        "nmap", "-p", str(port),
        "--script", "ftp-anon,ftp-banner,ftp-syst",
        str(ip)
    ]
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"[!] FTP Nmap enumeration failed: {result.stderr}")
        return

    output = result.stdout
    print(output)

    # Check for anonymous login
    if "Anonymous FTP login allowed" in output:
        db.insert_note(host_ip=ip, service_port=port, note="Anonymous FTP login possible.")

    # Potential brute force attempt (user must approve first, because NEEDS_USER_APPROVAL=True)
    hydra_cmd = [
        "hydra", "-L", "userlist.txt", "-P", "passlist.txt",
        f"ftp://{ip}"
    ]
    try:
        hydra_result = subprocess.run(hydra_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "login:" in hydra_result.stdout.lower():
            # Simple parse of found credentials
            creds_found = []
            for line in hydra_result.stdout.splitlines():
                if "[21][ftp]" in line.lower() and "login:" in line.lower():
                    creds_found.append(line)
            if creds_found:
                note_text = "Hydra FTP brute force success:\n" + "\n".join(creds_found)
                db.insert_note(host_ip=ip, service_port=port, note=note_text)
    except FileNotFoundError:
        print("[!] Hydra not installed or not in PATH.")
