# scripts/enumeration/es_enum.py
import requests
from core.db_manager import DBManager

NEEDS_USER_APPROVAL = False  # Typically just GET requests

def enumerate_service(ip, port):
    print(f"[+] Starting Elasticsearch enumeration on {ip}:{port}")
    db = DBManager()

    base_url = f"http://{ip}:{port}"
    try:
        r = requests.get(base_url, timeout=5)
        if r.status_code == 200:
            db.insert_note(host_ip=ip, service_port=port, note="Elasticsearch open. Basic info:\n" + r.text)
        else:
            print(f"[!] Received non-200 status: {r.status_code}")
    except Exception as e:
        print(f"[!] Could not connect to Elasticsearch: {e}")
