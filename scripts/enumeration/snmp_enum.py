# scripts/enumeration/snmp_enum.py
import subprocess
from core.db_manager import DBManager

NEEDS_USER_APPROVAL = False  # Typically just reading with common strings, not truly 'brute forcing'

def enumerate_service(ip, port):
    print(f"[+] Starting SNMP enumeration on {ip}:{port}")
    db = DBManager()

    # Example using onesixtyone to check common community strings
    onesixtyone_cmd = ["onesixtyone", "-c", "community_strings.txt", ip]
    try:
        result = subprocess.run(onesixtyone_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"[!] onesixtyone error: {result.stderr}")
            return

        output = result.stdout
        print(output)
        for line in output.splitlines():
            if "community" in line.lower():
                comm_string = line.split()[-1]
                db.insert_note(host_ip=ip, service_port=port, note=f"Found SNMP community string: {comm_string}")

        # Additional detail with snmpwalk, snmp-check, etc.
        # ...
    except FileNotFoundError:
        print("[!] onesixtyone not installed or not in PATH.")
