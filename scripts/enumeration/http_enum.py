import subprocess

def enumerate_http(ip, port=80):
    """
    Enumerates HTTP service on the target IP and port.

    :param ip: The target IP address.
    :param port: The target port number (default is 80).
    """
    url = f"http://{ip}:{port}"
    print(f"Enumerating HTTP on {url}")

    # Run Nikto
    nikto_command = ['nikto', '-h', url]
    subprocess.run(nikto_command)

    # Run Gobuster
    gobuster_command = ['gobuster', 'dir', '-u', url, '-w', '/usr/share/wordlists/dirb/common.txt']
    subprocess.run(gobuster_command)
