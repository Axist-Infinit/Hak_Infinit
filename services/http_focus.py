import subprocess
import sys
import os
import requests
import logging
import ipaddress
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_results_directory(ip):
    results_dir = os.path.join(os.getcwd(), "Results", ip)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    return results_dir

def take_screenshot(ip, results_dir):
    try:
        url = f"http://{ip}/"
        options = Options()
        options.headless = True
        with webdriver.Chrome(ChromeDriverManager().install(), options=options) as driver:
            driver.get(url)
            screenshot_name = os.path.join(results_dir, f"screenshot_{ip}.png")
            driver.save_screenshot(screenshot_name)
        logging.info(f"Screenshot of {url} saved as {screenshot_name}")
    except WebDriverException as e:
        logging.error(f"Failed to take screenshot of {ip}: {e}")

def get_robots_txt(ip, results_dir):
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; CustomScript/1.0)'}
    for protocol in ['http', 'https']:
        try:
            url = f"{protocol}://{ip}/robots.txt"
            response = requests.get(url, headers=headers, verify=False, timeout=5)
            if response.status_code == 200:
                robots_file = os.path.join(results_dir, f"robots_{ip}.txt")
                with open(robots_file, 'w') as f:
                    f.write(response.text)
                logging.info(f"robots.txt saved to {robots_file}")
                break
            else:
                logging.info(f"No robots.txt found on {ip} using {protocol.upper()}")
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve robots.txt from {ip} using {protocol.upper()}: {e}")

def list_http_exploits():
    logging.info(f"Listing potential exploits for HTTP/HTTPS service.")
    searchsploit_command = f"searchsploit --www http"
    subprocess.run(searchsploit_command, shell=True)

def search_exploits(service):
    logging.info(f"Searching for exploits related to {service} using searchsploit...")
    searchsploit_command = f"searchsploit --www {service}"
    subprocess.run(searchsploit_command, shell=True)

def main():
    if len(sys.argv) < 2:
        logging.error("No IP addresses provided. Exiting.")
        return

    http_ips = sys.argv[1].split(',')

    for ip in http_ips:
        if not ip.strip():
            continue
        ip = ip.strip()
        if not is_valid_ip(ip):
            logging.error(f"Invalid IP address: {ip}")
            continue

        logging.info(f"HTTP/HTTPS service detected on {ip}")
        results_dir = ensure_results_directory(ip)
        
        while True:
            print(f"\nSelect an action for {ip}:")
            print("1. Take a screenshot of the index page")
            print("2. Retrieve and save /robots.txt")
            print("3. List potential HTTP/HTTPS exploits")
            print("4. Search for related exploits with searchsploit")
            print("5. Move to next IP")
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                take_screenshot(ip, results_dir)
            elif choice == '2':
                get_robots_txt(ip, results_dir)
            elif choice == '3':
                list_http_exploits()
            elif choice == '4':
                service = input("Enter the service or keyword to search exploits for: ").strip()
                if service:
                    search_exploits(service)
                else:
                    logging.error("No service provided for exploit search.")
            elif choice == '5':
                logging.info(f"Moving to next IP.")
                break
            else:
                logging.error("Invalid choice, please select a valid option.")

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    main()
