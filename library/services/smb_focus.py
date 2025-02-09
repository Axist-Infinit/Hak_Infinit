import subprocess
import sys
import os
import logging
import ipaddress
import shlex

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_results_directory(ip):
    results_dir = os.path.join(os.getcwd(), "Results", ip)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    return results_dir

def scan_smb_shares(ip, results_dir):
    try:
        logging.info(f"Scanning for SMB shares on {ip}...")
        command = ['smbclient', '-L', ip, '-N']
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output_file = os.path.join(results_dir, f"smb_shares_{ip}.txt")
        with open(output_file, 'w') as f:
            f.write(result.stdout)
        logging.info(f"SMB shares scan results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to scan SMB shares on {ip}: {e}")

def verify_smb_connection(ip, share_name):
    try:
        logging.info(f"Verifying connection to SMB share {share_name} on {ip}...")
        command = ['smbclient', f"//{ip}/{share_name}", '-N']
        subprocess.run(command, check=True)
        logging.info(f"Successfully connected to SMB share {share_name} on {ip}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to connect to SMB share {share_name} on {ip}: {e}")

def list_smb_exploits():
    logging.info("Listing potential exploits for SMB service.")
    command = ['searchsploit', '--www', 'smb']
    subprocess.run(command)

def run_nmap_smb_enum(ip, results_dir):
    try:
        logging.info(f"Running Nmap SMB enumeration on {ip}...")
        output_file = os.path.join(results_dir, f"nmap_smb_enum_{ip}.txt")
        command = [
            'nmap', '-p', '445',
            '--script', 'smb-enum-shares,smb-enum-users,smb-os-discovery',
            '-oN', output_file, ip
        ]
        subprocess.run(command, check=True)
        logging.info(f"Nmap SMB enumeration results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run Nmap SMB enumeration on {ip}: {e}")

def search_exploits(service):
    logging.info(f"Searching for exploits related to {service} using searchsploit...")
    command = ['searchsploit', '--www', service]
    subprocess.run(command)

def detect_smb_version(ip, results_dir):
    try:
        logging.info(f"Detecting SMB version on {ip}...")
        output_file = os.path.join(results_dir, f"smb_version_{ip}.txt")
        command = [
            'nmap', '-p', '445',
            '--script', 'smb-protocols',
            '-oN', output_file, ip
        ]
        subprocess.run(command, check=True)
        logging.info(f"SMB version detection results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to detect SMB version on {ip}: {e}")

def check_for_eternalblue(ip, results_dir):
    try:
        logging.info(f"Checking for EternalBlue vulnerability on {ip}...")
        output_file = os.path.join(results_dir, f"eternalblue_check_{ip}.txt")
        command = [
            'nmap', '-p', '445',
            '--script', 'smb-vuln-ms17-010',
            '-oN', output_file, ip
        ]
        subprocess.run(command, check=True)
        logging.info(f"EternalBlue vulnerability check results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to check for EternalBlue on {ip}: {e}")

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def main():
    if len(sys.argv) < 2:
        logging.error("No IP addresses provided. Exiting.")
        return

    smb_ips = sys.argv[1].split(',')

    for ip in smb_ips:
        if not ip.strip():
            continue
        ip = ip.strip()
        if not is_valid_ip(ip):
            logging.error(f"Invalid IP address: {ip}")
            continue

        logging.info(f"SMB service detected on {ip}")
        results_dir = ensure_results_directory(ip)
        
        while True:
            print(f"\nSelect an action for {ip}:")
            print("1. Scan for open SMB shares")
            print("2. Verify connection to an SMB share")
            print("3. List potential SMB exploits")
            print("4. Perform Nmap SMB enumeration")
            print("5. Detect SMB version")
            print("6. Check for EternalBlue vulnerability")
            print("7. Search for related exploits with searchsploit")
            print("8. Move to next IP")
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == '1':
                scan_smb_shares(ip, results_dir)
            elif choice == '2':
                share_name = input("Enter the SMB share name to verify: ").strip()
                share_name = shlex.quote(share_name)
                verify_smb_connection(ip, share_name)
            elif choice == '3':
                list_smb_exploits()
            elif choice == '4':
                run_nmap_smb_enum(ip, results_dir)
            elif choice == '5':
                detect_smb_version(ip, results_dir)
            elif choice == '6':
                check_for_eternalblue(ip, results_dir)
            elif choice == '7':
                service = input("Enter the service or keyword to search exploits for: ").strip()
                if service:
                    search_exploits(service)
                else:
                    logging.error("No service provided for exploit search.")
            elif choice == '8':
                logging.info(f"Moving to next IP.")
                break
            else:
                logging.error("Invalid choice, please select a valid option.")

if __name__ == "__main__":
    main()
