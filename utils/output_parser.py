"""
scripts/utils/output_parser.py

Merged version that retains old IP/URL/Email extraction,
adds version extraction, and can optionally parse 
Nmap TCP/UDP services with version info.
"""

import re

def extract_ips(text):
    """
    Extracts all IPv4 addresses from the given text.
    (Optionally, we can expand to IPv6 if desired.)
    """
    # For strict IPv4. 
    # If you want to handle IPv6, consider an additional pattern or a combined approach.
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    return ip_pattern.findall(text)

def extract_urls(text):
    """
    Extracts all URLs from the given text.
    """
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z0-9]|[$-_@.&+]|[!*\(\),]|'
        r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return url_pattern.findall(text)

def extract_emails(text):
    """
    Extracts all email addresses from the given text.
    """
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Z|a-z]{2,}\b')
    return email_pattern.findall(text)

def extract_version(banner):
    """
    Extracts a version number from a string/banner (e.g. 1.2.3).
    You can expand this regex or logic if you need more complex patterns.
    """
    version_pattern = re.compile(r'([0-9]+\.[0-9]+(\.[0-9]+)?)')
    match = version_pattern.search(banner)
    if match:
        return match.group(1)
    return None

def parse_nmap_services(nmap_output, include_udp=False):
    """
    Parses text-based Nmap output to extract open ports and associated services.

    :param nmap_output: The raw output from an Nmap scan (grepable or normal).
    :param include_udp: If True, also parse UDP lines: '(\d+)/udp open ...'
    :return: A dictionary with ports as keys and (service, protocol, version?) as values.
             e.g. {80: ('http', 'tcp', None), 443: ('https', 'tcp', None)}
    """
    # Original pattern for TCP: (\d{1,5})/tcp\s+open\s+(\S+)
    # Add an optional group for capturing version if present,
    # e.g. "80/tcp open  http syn-ack ttl 64 Apache httpd 2.4.18"
    # This requires a more flexible regex or partial parse.

    # Basic pattern for open service lines, capturing port & service:
    tcp_pattern = re.compile(r'(\d{1,5})/tcp\s+open\s+(\S+)')
    udp_pattern = re.compile(r'(\d{1,5})/udp\s+open\s+(\S+)')

    services = {}

    # Parse TCP lines
    for match in tcp_pattern.findall(nmap_output):
        port, svc = match
        port = int(port)
        # Optionally parse version from the trailing text if you'd like:
        # e.g., sometimes Nmap prints "http syn-ack ttl 64 Apache httpd 2.4.18"
        # but we'd need an additional approach or capture group for version info.
        # For now, we just store the raw service name.
        services[port] = (svc, 'tcp', None)

    # Parse UDP lines if requested
    if include_udp:
        for match in udp_pattern.findall(nmap_output):
            port, svc = match
            port = int(port)
            # Same logic for version capturing could apply here if needed.
            services[port] = (svc, 'udp', None)

    return services
