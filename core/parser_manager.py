import xml.etree.ElementTree as ET

def parse_nmap_xml(xml_output):
    tree = ET.parse(xml_output)
    root = tree.getroot()
    hosts = []
    for host in root.findall('host'):
        ip = host.find('address').get('addr')
        ports = []
        for port in host.find('ports').findall('port'):
            port_id = port.get('portid')
            service = port.find('service').get('name')
            ports.append((port_id, service))
        hosts.append({'ip': ip, 'ports': ports})
    return hosts
