import subprocess
import os
from core.config_manager import ConfigManager

def run_nmap_scan(target, output_xml_path, additional_args=None):
    """
    Run an Nmap scan on the target and store XML output.
    Includes checks to ensure we capture all ports, handle errors,
    and optionally runs a second pass for thoroughness.
    """
    config = ConfigManager()

    # Provide a robust default set of Nmap args if none supplied
    if additional_args is None:
        additional_args = [
            "-sC",               # default scripts
            "-sV",               # version detection
            "-O",                # OS detection
            "-p-",               # scan all TCP ports
            "-T4",               # faster timing
            "--max-retries", "2",
            "-oX", output_xml_path
        ]

    nmap_cmd = ["nmap"] + additional_args + [target]
    print(f"[+] Running Nmap command: {' '.join(nmap_cmd)}")

    try:
        result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"[!] Nmap scan failed with error:\n{result.stderr}")
            return None

        # Optional second pass: If user wants to do a UDP scan or deeper script scan
        udp_scan = config.get("Nmap", "udp_scan", fallback="false")
        if udp_scan.lower() == "true":
            # Example additional UDP scan
            udp_output_xml = output_xml_path.replace(".xml", "_udp.xml")
            udp_cmd = ["nmap", "-sU", "-p-", "-T4", "--max-retries", "2", "-oX", udp_output_xml, target]
            print(f"[+] Running additional UDP scan: {' '.join(udp_cmd)}")
            subprocess.run(udp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # We'll parse this second output in parse_results if it exists

        print(f"[+] Nmap scan completed successfully. Results saved to {output_xml_path}")
        return output_xml_path

    except FileNotFoundError:
        print("[!] Nmap not found. Please ensure it is installed and in your PATH.")
        return None
    except Exception as e:
        print(f"[!] Exception occurred while running Nmap: {str(e)}")
        return None
