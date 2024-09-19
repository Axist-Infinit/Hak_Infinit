import subprocess
import sys
import os

def run_smtp_user_enum(ip, users_file):
    print(f"Running SMTP user enumeration on {ip} using smtp-user-enum...")
    smtp_user_enum_command = f"smtp-user-enum -M VRFY -U {users_file} -t {ip} -o Results/smtp_user_enum_{ip}.txt"
    subprocess.run(smtp_user_enum_command, shell=True)
    print(f"SMTP user enumeration results saved to Results/smtp_user_enum_{ip}.txt")

def run_nmap_smtp_enum(ip):
    print(f"Running Nmap SMTP enumeration on {ip}...")
    nmap_command = (
        f"nmap -p 25,465,587 --script smtp-enum-users,smtp-commands,"
        f"smtp-open-relay,smtp-vuln-cve2010-4344,smtp-vuln-cve2011-1720,"
        f"smtp-vuln-cve2011-1764 -oN Results/nmap_smtp_enum_{ip}.txt {ip}"
    )
    subprocess.run(nmap_command, shell=True)
    print(f"Nmap SMTP enumeration results saved to Results/nmap_smtp_enum_{ip}.txt")

def run_fierce_smtp_enum(domain):
    print(f"Running Fierce DNS enumeration for SMTP on domain {domain}...")
    fierce_command = f"fierce -dns {domain} -smtp -o Results/fierce_smtp_{domain}.txt"
    subprocess.run(fierce_command, shell=True)
    print(f"Fierce DNS enumeration results saved to Results/fierce_smtp_{domain}.txt")

def search_exploits(ip, service):
    print(f"Searching for exploits related to {service} on {ip} using searchsploit...")
    searchsploit_command = f"searchsploit {service}"
    subprocess.run(searchsploit_command, shell=True)

def main():
    if len(sys.argv) < 2:
        print("No IP addresses provided. Exiting.")
        return

    smtp_ips = sys.argv[1].split(',')

    users_file = input("Enter the path to the users file for SMTP enumeration (e.g., /path/to/users.txt): ").strip()
    if not os.path.exists(users_file):
        print(f"Users file {users_file} does not exist. Exiting.")
        return

    for ip in smtp_ips:
        print(f"\nSMTP service detected on {ip}")
        
        print("What would you like to do?")
        print("1. Enumerate users on the SMTP server using smtp-user-enum")
        print("2. Perform Nmap SMTP enumeration")
        print("3. Perform Fierce DNS enumeration for SMTP")
        print("4. Search for related exploits with searchsploit")
        print("5. Skip this IP")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            run_smtp_user_enum(ip, users_file)
        elif choice == '2':
            run_nmap_smtp_enum(ip)
        elif choice == '3':
            domain = input("Enter the target domain for Fierce DNS enumeration: ").strip()
            run_fierce_smtp_enum(domain)
        elif choice == '4':
            search_exploits(ip, "smtp")
        elif choice == '5':
            print(f"Skipping IP: {ip}")
        else:
            print("Invalid choice, skipping this IP.")

if __name__ == "__main__":
    main()
