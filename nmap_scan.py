import subprocess
import os
import re
import sys

# Get the absolute path of the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_quick_scan(network_range):
    results_dir = os.path.join(SCRIPT_DIR, "Results")
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Sanitize the network_range for use in filenames
    sanitized_network_range = network_range.replace('/', '_').replace('.', '_').replace(':', '_')

    quick_scan_output = os.path.join(results_dir, f"nmap_quick_scan_{sanitized_network_range}.txt")

    # Run a quick Nmap scan to check for live hosts
    print(f"Running quick Nmap scan on {network_range} to identify live hosts...")
    nmap_quick_command = f"nmap -sn {network_range} -oG -"
    try:
        result = subprocess.run(nmap_quick_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        live_hosts = parse_live_hosts(result.stdout)
        print(f"Quick scan completed. Live hosts found: {len(live_hosts)}")
    except subprocess.CalledProcessError as e:
        print(f"Error running quick Nmap scan:\n{e.stderr}")
        sys.exit(1)

    return live_hosts

def parse_live_hosts(nmap_output):
    live_hosts = []
    for line in nmap_output.splitlines():
        if 'Up' in line:
            match = re.search(r'Host: (\S+)', line)
            if match:
                live_hosts.append(match.group(1))
    return live_hosts

def run_comprehensive_scan(hosts):
    results_dir = os.path.join(SCRIPT_DIR, "Results")

    comprehensive_output_file = os.path.join(results_dir, "nmap_comprehensive_scan.txt")

    # Run comprehensive Nmap scan on live hosts
    print(f"Running comprehensive Nmap scan on live hosts...")
    hosts_str = ' '.join(hosts)
    nmap_comprehensive_command = f"nmap -sS -sV -O -A -T4 -p- -vv {hosts_str} -oN \"{comprehensive_output_file}\""
    try:
        subprocess.run(nmap_comprehensive_command, shell=True, check=True)
        print(f"Comprehensive scan completed. Results saved in {comprehensive_output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running comprehensive Nmap scan:\n{e.stderr}")
        sys.exit(1)

    return comprehensive_output_file

def extract_service_ips(nmap_output_file, service_ports):
    service_ips = set()
    with open(nmap_output_file, 'r') as file:
        ip = None
        for line in file:
            ip_match = re.match(r"Nmap scan report for (\S+)", line)
            if ip_match:
                ip = ip_match.group(1)
            for port in service_ports:
                if f"{port}/tcp open" in line and ip:
                    service_ips.add(ip)
    return list(service_ips)

def run_service_scripts(services_ips_dict):
    for service, ips in services_ips_dict.items():
        if ips:
            print(f"\nThe following IP addresses have {service.upper()} services running:")
            for ip in ips:
                print(f" - {ip}")

            proceed = input(f"\nWould you like to perform {service.upper()}-specific actions on these IP addresses? (y/n): ").strip().lower()

            if proceed == 'y':
                ips_str = ','.join(ips)
                script_path = os.path.join("services", f"{service}_focus.py")
                if os.path.exists(script_path):
                    subprocess.run(f"python3 {script_path} {ips_str}", shell=True)
                else:
                    print(f"Service script for {service} not found at {script_path}")
        else:
            print(f"\nNo IP addresses with {service.upper()} services detected.")

def run_output_results():
    print("Running output_results.py to consolidate findings...")
    output_results_path = os.path.join(SCRIPT_DIR, 'general', 'output_results.py')
    if not os.path.exists(output_results_path):
        print(f"Error: {output_results_path} does not exist.")
        return
    subprocess.run(f"python3 \"{output_results_path}\"", shell=True)
    print("Results have been consolidated and saved.")

def main():
    print(f"Script is running from: {SCRIPT_DIR}")
    print(f"Current working directory: {os.getcwd()}")

    network_range = input("Enter the network range to scan (e.g., 192.168.1.0/24): ").strip()

    # Run quick scan to identify live hosts
    live_hosts = run_quick_scan(network_range)
    if not live_hosts:
        print("No live hosts found. Exiting.")
        sys.exit(0)

    # Run comprehensive scan on live hosts
    comprehensive_output_file = run_comprehensive_scan(live_hosts)

    # Define service ports to look for
    services = {
        'smb': ['445'],
        'http': ['80', '443'],
        'smtp': ['25', '465', '587'],
        'mssql': ['1433']
    }

    # Extract IPs for each service
    services_ips_dict = {}
    for service, ports in services.items():
        ips = extract_service_ips(comprehensive_output_file, ports)
        services_ips_dict[service] = ips

    # Run service-specific scripts based on the detected services
    run_service_scripts(services_ips_dict)

    # Run output_results.py to consolidate results
    run_output_results()

if __name__ == "__main__":
    main()
