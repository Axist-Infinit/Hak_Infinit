import subprocess

def enumerate_smb(ip):
    """
    Enumerates SMB service on the target IP.

    :param ip: The target IP address.
    """
    print(f"Enumerating SMB on {ip}")

    # Run enum4linux
    enum4linux_command = ['enum4linux', '-a', ip]
    subprocess.run(enum4linux_command)

    # List SMB shares using smbclient
    smbclient_command = ['smbclient', '-L', f"//{ip}/", '-N']
    subprocess.run(smbclient_command)
