import subprocess

def search_exploits(service):
    """
    Searches for exploits related to the specified service using SearchSploit.

    :param service: The service name to search exploits for.
    """
    print(f"Searching for exploits related to {service} using SearchSploit...")
    searchsploit_command = ['searchsploit', service]
    subprocess.run(searchsploit_command)
