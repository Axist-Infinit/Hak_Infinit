import xml.etree.ElementTree as ET
import os

from core.db_manager import DBManager

def parse_nmap_xml(xml_file_path):
    """
    Parses the Nmap XML output file and returns a structured list of discovered hosts.
    Each element in the list is a dict with keys: ip_address, os_info, ports (list of port dicts).
    """
    parsed_data = []
    
    # Handle missing file or parse errors
    if not os.path.isfile(xml_file_path):
        print(f"[!] Nmap XML output not found: {xml_file_path}")
        return parsed_data

    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"[!] Error parsing Nmap XML: {e}")
        return parsed_data

    for host in root.findall('host'):
        status = host.find('status')
        if status is not None and status.get('state') != 'up':
            continue

        # Grab IPv4 address
        ip_address = None
        for address in host.findall('address'):
            if address.get('addrtype') == 'ipv4':
                ip_address = address.get('addr')

        if not ip_address:
            continue

        # OS detection
        os_info = None
        os_el = host.find('os')
        if os_el is not None:
            os_matches = os_el.findall('osmatch')
            if os_matches:
                # highest accuracy match
                os_info = os_matches[0].get('name')

        # Ports
        ports_data = []
        ports_el = host.find('ports')
        if ports_el is not None:
            for port_el in ports_el.findall('port'):
                port_id = port_el.get('portid')
                protocol = port_el.get('protocol')
                state_el = port_el.find('state')
                state = state_el.get('state') if state_el is not None else 'unknown'

                service_el = port_el.find('service')
                service_name = service_el.get('name') if service_el is not None else None
                service_version = service_el.get('version') if service_el is not None else None

                if state.lower() == 'open':
                    ports_data.append({
                        'port': int(port_id),
                        'protocol': protocol,
                        'service': service_name.lower() if service_name else None,
                        'version': service_version
                    })

        parsed_data.append({
            'ip_address': ip_address,
            'os_info': os_info,
            'ports': ports_data
        })

    return parsed_data

def store_scan_results_in_db(parsed_data):
    """
    Stores the parsed Nmap results into the database (hosts/services).
    """
    db = DBManager()
    for host in parsed_data:
        host_id = db.insert_host(host['ip_address'], host['os_info'])
        for port_info in host['ports']:
            db.insert_service(
                host_id=host_id,
                port=port_info['port'],
                protocol=port_info['protocol'],
                service_name=port_info['service'],
                version=port_info['version']
            )

def parse_and_store(xml_file_path):
    """
    Helper function that combines parse + store logic.
    """
    data = parse_nmap_xml(xml_file_path)
    if data:
        store_scan_results_in_db(data)
        print(f"[+] Parsed and stored data from {xml_file_path}")
    else:
        print("[!] No valid data found or file was not parseable.")
