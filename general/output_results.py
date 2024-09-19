import os

def consolidate_results(ip):
    results_dir = "Results"
    output_file = os.path.join(results_dir, f"{ip}_results.txt")
    
    with open(output_file, 'a') as out_file:  # Use 'a' mode to append results if the file already exists
        out_file.write(f"Results for IP: {ip}\n")
        out_file.write("=" * 50 + "\n\n")
        
        # Nmap Scan Results
        nmap_file = os.path.join(results_dir, f"nmap_scan_{ip}.txt")
        if os.path.exists(nmap_file):
            with open(nmap_file, 'r') as nmap_result:
                out_file.write("Nmap Scan Results:\n")
                out_file.write(nmap_result.read())
                out_file.write("\n" + "=" * 50 + "\n\n")
        
        # SMB Exploits Results
        smb_file = os.path.join(results_dir, f"smb_{ip}.txt")
        if os.path.exists(smb_file):
            with open(smb_file, 'r') as smb_result:
                out_file.write("SMB Exploits:\n")
                out_file.write(smb_result.read())
                out_file.write("\n" + "=" * 50 + "\n\n")
        
        # SMB Nmap Enumeration Results
        smb_enum_file = os.path.join(results_dir, f"nmap_smb_enum_{ip}.txt")
        if os.path.exists(smb_enum_file):
            with open(smb_enum_file, 'r') as smb_enum_result:
                out_file.write("Nmap SMB Enumeration Results:\n")
                out_file.write(smb_enum_result.read())
                out_file.write("\n" + "=" * 50 + "\n\n")
        
        # HTTP Screenshot
        screenshot_file = os.path.join(results_dir, f"screenshot_{ip}.png")
        if os.path.exists(screenshot_file):
            out_file.write(f"Screenshot of {ip} index page saved as {screenshot_file}\n")
            out_file.write("\n" + "=" * 50 + "\n\n")
        
        # Robots.txt
        robots_file = os.path.join(results_dir, f"robots_{ip}.txt")
        if os.path.exists(robots_file):
            with open(robots_file, 'r') as robots_result:
                out_file.write("robots.txt Content:\n")
                out_file.write(robots_result.read())
                out_file.write("\n" + "=" * 50 + "\n\n")
        
        # SMTP User Enumeration Results
        smtp_user_enum_file = os.path.join(results_dir, f"smtp_user_enum_{ip}.txt")
        if os.path.exists(smtp_user_enum_file):
            with open(smtp_user_enum_file, 'r') as smtp_user_enum_result:
                out_file.write("SMTP User Enumeration Results:\n")
                out_file.write(smtp_user_enum_result.read())
                out_file.write("\n" + "=" * 50 + "\n\n")
        
        # SMTP Nmap Enumeration Results
        nmap_smtp_enum_file = os.path.join(results_dir, f"nmap_smtp_enum_{ip}.txt")
        if os.path.exists(nmap_smtp_enum_file):
            with open(nmap_smtp_enum_file, 'r') as nmap_smtp_enum_result:
                out_file.write("Nmap SMTP Enumeration Results:\n")
                out_file.write(nmap_smtp_enum_result.read())
                out_file.write("\n" + "=" * 50 + "\n\n")
        
        # Fierce DNS Enumeration for SMTP Results
        fierce_smtp_file = os.path.join(results_dir, f"fierce_smtp_{ip}.txt")
        if os.path.exists(fierce_smtp_file):
            with open(fierce_smtp_file, 'r') as fierce_smtp_result:
                out_file.write("Fierce DNS Enumeration for SMTP Results:\n")
                out_file.write(fierce_smtp_result.read())
                out_file.write("\n" + "=" * 50 + "\n\n")
        
        # MSSQL Nmap Enumeration Results
        nmap_mssql_enum_file = os.path.join(results_dir, f"nmap_mssql_enum_{ip}.txt")
        if os.path.exists(nmap_mssql_enum_file):
            with open(nmap_mssql_enum_file, 'r') as nmap_mssql_enum_result:
                out_file.write("Nmap MSSQL Enumeration Results:\n")
                out_file.write(nmap_mssql_enum_result.read())
                out_file.write("\n" + "=" * 50 + "\n\n")
        
        # SQLRecon Results
        sqlrecon_file = os.path.join(results_dir, f"sqlrecon_{ip}.txt")
        if os.path.exists(sqlrecon_file):
            with open(sqlrecon_file, 'r') as sqlrecon_result:
                out_file.write("SQLRecon Results:\n")
                out_file.write(sqlrecon_result.read())
                out_file.write("\n" + "=" * 50 + "\n\n")
        
        # sqlmap Results
        sqlmap_file = os.path.join(results_dir, f"sqlmap_{ip}.txt")
        if os.path.exists(sqlmap_file):
            with open(sqlmap_file, 'r') as sqlmap_result:
                out_file.write("sqlmap Results:\n")
                out_file.write(sqlmap_result.read())
                out_file.write("\n" + "=" * 50 + "\n\n")
        
        # EnumDB Results
        enumdb_file = os.path.join(results_dir, f"enumdb_{ip}.txt")
        if os.path.exists(enumdb_file):
            with open(enumdb_file, 'r') as enumdb_result:
                out_file.write("EnumDB Results:\n")
                out_file.write(enumdb_result.read())
                out_file.write("\n" + "=" * 50 + "\n\n")
        
        out_file.write("End of results.\n")

def main():
    # Find all IPs with results
    ips = []
    results_dir = "Results"
    if os.path.exists(results_dir):
        for file_name in os.listdir(results_dir):
            if "nmap_scan" in file_name:
                ip = file_name.split("_")[-1].split(".")[0]
                if ip not in ips:
                    ips.append(ip)
    
    # Generate consolidated result for each IP
    for ip in ips:
        consolidate_results(ip)
        print(f"Results consolidated for IP: {ip}")

if __name__ == "__main__":
    main()
