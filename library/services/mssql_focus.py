import subprocess
import sys
import os

def run_nmap_mssql_enum(ip):
    print(f"Running Nmap MSSQL enumeration on {ip}...")
    nmap_command = (
        f"nmap -p 1433 --script ms-sql-info,ms-sql-config,"
        f"ms-sql-ntlm-info,ms-sql-empty-password -oN Results/nmap_mssql_enum_{ip}.txt {ip}"
    )
    subprocess.run(nmap_command, shell=True)
    print(f"Nmap MSSQL enumeration results saved to Results/nmap_mssql_enum_{ip}.txt")

def run_sqlrecon(ip):
    print(f"Running SQLRecon on {ip}...")
    sqlrecon_command = f"SQLRecon -t {ip} -o Results/sqlrecon_{ip}.txt"
    subprocess.run(sqlrecon_command, shell=True)
    print(f"SQLRecon results saved to Results/sqlrecon_{ip}.txt")

def run_sqlmap(ip, username, password, db_name):
    print(f"Running sqlmap on {ip}...")
    sqlmap_command = (
        f"sqlmap -d \"mssql://{username}:{password}@{ip}:1433/{db_name}\" --dbs --risk=3 --level=5 "
        f"-o Results/sqlmap_{ip}.txt"
    )
    subprocess.run(sqlmap_command, shell=True)
    print(f"sqlmap results saved to Results/sqlmap_{ip}.txt")

def run_enumdb(ip):
    print(f"Running EnumDB on {ip}...")
    enumdb_command = f"EnumDB -t {ip} -o Results/enumdb_{ip}.txt"
    subprocess.run(enumdb_command, shell=True)
    print(f"EnumDB results saved to Results/enumdb_{ip}.txt")

def search_exploits(ip, service):
    print(f"Searching for exploits related to {service} on {ip} using searchsploit...")
    searchsploit_command = f"searchsploit {service}"
    subprocess.run(searchsploit_command, shell=True)

def main():
    if len(sys.argv) < 2:
        print("No IP addresses provided. Exiting.")
        return

    mssql_ips = sys.argv[1].split(',')

    for ip in mssql_ips:
        print(f"\nMSSQL service detected on {ip}")
        
        print("What would you like to do?")
        print("1. Perform Nmap MSSQL enumeration")
        print("2. Run SQLRecon")
        print("3. Run sqlmap")
        print("4. Run EnumDB")
        print("5. Search for related exploits with searchsploit")
        print("6. Skip this IP")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            run_nmap_mssql_enum(ip)
        elif choice == '2':
            run_sqlrecon(ip)
        elif choice == '3':
            username = input("Enter the MSSQL username: ").strip()
            password = input("Enter the MSSQL password: ").strip()
            db_name = input("Enter the database name (or leave blank for all): ").strip()
            run_sqlmap(ip, username, password, db_name)
        elif choice == '4':
            run_enumdb(ip)
        elif choice == '5':
            search_exploits(ip, "mssql")
        elif choice == '6':
            print(f"Skipping IP: {ip}")
        else:
            print("Invalid choice, skipping this IP.")

if __name__ == "__main__":
    main()
