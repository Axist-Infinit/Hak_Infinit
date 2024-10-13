import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures
import dns.resolver
import tldextract
import threading
import time
import random
import re
import os

# Suppress only the single InsecureRequestWarning from urllib3 needed.
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Lock for thread-safe operations
lock = threading.Lock()

# Default wordlist paths (Update these paths to where you've downloaded the wordlists)
SECLIST_DIR = 'SecList'  # Path to the cloned SecList repository
DISCOVERY_DIR = os.path.join(SECLIST_DIR, 'Discovery')

# General wordlists
DEFAULT_DIR_WORDLIST = os.path.join(DISCOVERY_DIR, 'Web-Content', 'directory-list-2.3-medium.txt')
LARGE_DIR_WORDLIST = os.path.join(DISCOVERY_DIR, 'Web-Content', 'directory-list-2.3-big.txt')
COMMON_FILE_WORDLIST = os.path.join(DISCOVERY_DIR, 'Web-Content', 'common.txt')
SUBDOMAIN_WORDLIST = os.path.join(DISCOVERY_DIR, 'DNS', 'names.txt')

# API wordlists
API_LOWERCASE_WORDLIST = os.path.join(DISCOVERY_DIR, 'Web-Content', 'API', 'api-endpoints.txt')

# CMS wordlists
CMS_WORDLISTS_DIR = os.path.join(DISCOVERY_DIR, 'Web-Content', 'CMS')

# Parameter wordlists
PARAMETER_WORDLIST = os.path.join(DISCOVERY_DIR, 'Web-Content', 'burp-parameter-names.txt')

# Web shell wordlists
WEBSHELLS_WORDLIST = os.path.join(DISCOVERY_DIR, 'Web-Shells', 'web-shells-reduced.txt')

# Common page extensions
COMMON_EXTENSIONS = ['.php', '.html', '.htm', '.asp', '.aspx', '.jsp']

# User-Agent list
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    'Mozilla/5.0 (X11; Linux x86_64)...',
    # Add more user agents here
]

class WebsiteEnumerator:
    def __init__(self, base_url, dir_wordlist, subdomain_wordlist, output_file):
        self.base_url = self.normalize_url(base_url)
        self.domain = self.get_domain(self.base_url)
        self.scheme = urlparse(self.base_url).scheme
        self.visited = set()
        self.to_visit = set([self.base_url])
        self.found_urls = set()
        self.dir_wordlist = dir_wordlist
        self.subdomain_wordlist = subdomain_wordlist
        self.output_file = output_file
        self.headers = {'User-Agent': random.choice(USER_AGENTS)}
        self.cms_detected = None
        self.language_detected = None

    def normalize_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return url.rstrip('/')

    def get_domain(self, url):
        ext = tldextract.extract(url)
        return ext.registered_domain

    def crawl(self):
        print("[*] Starting web crawling...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            while self.to_visit:
                current_url = self.to_visit.pop()
                if current_url in self.visited:
                    continue
                self.visited.add(current_url)
                executor.submit(self.process_page, current_url)
        print("[*] Web crawling completed.")

    def process_page(self, url):
        try:
            response = requests.get(url, headers=self.headers, verify=False, timeout=5)
            if response.status_code != 200:
                return
            self.found_urls.add(url)
            self.detect_cms(response.text)
            self.detect_language(url, response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all(['a', 'link', 'script', 'img', 'form'], href=True, src=True, action=True):
                href = link.get('href') or link.get('src') or link.get('action')
                joined_href = urljoin(url, href)
                parsed_href = urlparse(joined_href)
                href_domain = self.get_domain(joined_href)
                if href_domain == self.domain:
                    normalized_href = f"{parsed_href.scheme}://{parsed_href.netloc}{parsed_href.path}".rstrip('/')
                    with lock:
                        if normalized_href not in self.visited:
                            self.to_visit.add(normalized_href)
        except requests.RequestException:
            pass  # Ignore errors and continue

    def detect_cms(self, html_content):
        if self.cms_detected:
            return
        # Simple CMS detection logic
        if 'wp-content' in html_content or 'wordpress' in html_content:
            self.cms_detected = 'WordPress'
            print("[*] WordPress CMS detected.")
        elif 'Joomla!' in html_content:
            self.cms_detected = 'Joomla'
            print("[*] Joomla CMS detected.")
        elif 'Drupal.settings' in html_content:
            self.cms_detected = 'Drupal'
            print("[*] Drupal CMS detected.")
        # Add more CMS detection logic as needed

    def detect_language(self, url, html_content):
        if self.language_detected:
            return
        parsed_url = urlparse(url)
        path = parsed_url.path
        if path.endswith('.php') or 'PHPSESSID' in response.headers.get('Set-Cookie', ''):
            self.language_detected = 'PHP'
            print("[*] PHP application detected.")
        elif path.endswith('.asp') or path.endswith('.aspx') or 'ASPSESSIONID' in response.headers.get('Set-Cookie', ''):
            self.language_detected = 'ASP'
            print("[*] ASP application detected.")
        elif path.endswith('.jsp') or 'JSESSIONID' in response.headers.get('Set-Cookie', ''):
            self.language_detected = 'JSP'
            print("[*] JSP application detected.")
        # Add more language detection logic as needed

    def directory_brute_force(self):
        print("[*] Starting directory brute-forcing...")
        dirs = self.load_wordlist(self.dir_wordlist)

        # Include CMS-specific wordlists if CMS is detected
        if self.cms_detected:
            cms_wordlist_path = os.path.join(CMS_WORDLISTS_DIR, f"{self.cms_detected.lower()}.txt")
            if os.path.exists(cms_wordlist_path):
                print(f"[*] Including {self.cms_detected} CMS-specific wordlist.")
                cms_dirs = self.load_wordlist(cms_wordlist_path)
                dirs.extend(cms_dirs)

        # Include language-specific wordlists
        if self.language_detected:
            language_wordlist_path = os.path.join(DISCOVERY_DIR, 'Web-Content', f"{self.language_detected.lower()}.txt")
            if os.path.exists(language_wordlist_path):
                print(f"[*] Including {self.language_detected}-specific wordlist.")
                language_dirs = self.load_wordlist(language_wordlist_path)
                dirs.extend(language_dirs)

        # Include API wordlists
        api_actions = self.load_wordlist(API_LOWERCASE_WORDLIST)
        dirs.extend(api_actions)

        # Include parameter names
        parameters = self.load_wordlist(PARAMETER_WORDLIST)

        dirs_to_check = ["/" + d.strip("/") for d in dirs]
        url_list = [f"{self.base_url}{d}" for d in dirs_to_check]

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.check_url, url): url for url in url_list}
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                status_code = future.result()
                if status_code:
                    self.found_urls.add(url)
        print("[*] Directory brute-forcing completed.")

    def page_brute_force(self):
        print("[*] Starting page brute-forcing...")
        pages = self.load_wordlist(COMMON_FILE_WORDLIST)
        pages_with_ext = [p + ext for p in pages for ext in COMMON_EXTENSIONS]
        url_list = [f"{self.base_url}/{p}" for p in pages_with_ext]

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.check_url, url): url for url in url_list}
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                status_code = future.result()
                if status_code:
                    self.found_urls.add(url)
        print("[*] Page brute-forcing completed.")

    def parameter_fuzzing(self):
        print("[*] Starting parameter fuzzing...")
        parameters = self.load_wordlist(PARAMETER_WORDLIST)
        test_url = self.base_url + "?"
        url_list = [test_url + param + "=test" for param in parameters]

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.check_url, url): url for url in url_list}
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                status_code = future.result()
                if status_code and status_code != 404:
                    self.found_urls.add(url)
        print("[*] Parameter fuzzing completed.")

    def webshell_detection(self):
        print("[*] Starting web shell detection...")
        shells = self.load_wordlist(WEBSHELLS_WORDLIST)
        url_list = [f"{self.base_url}/{shell}" for shell in shells]

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.check_url, url): url for url in url_list}
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                status_code = future.result()
                if status_code:
                    self.found_urls.add(url)
        print("[*] Web shell detection completed.")

    def check_url(self, url):
        try:
            response = requests.get(url, headers=self.headers, verify=False, timeout=5)
            if response.status_code in [200, 301, 302, 403]:
                print(f"[+] {response.status_code} Found: {url}")
                return response.status_code
            time.sleep(0.1)  # Rate limiting
        except requests.RequestException:
            pass
        return None

    def subdomain_enumeration(self):
        print("[*] Starting subdomain enumeration...")
        subdomains = self.load_wordlist(self.subdomain_wordlist)
        full_subdomains = [f"{sub}.{self.domain}" for sub in subdomains]

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.resolve_subdomain, sub): sub for sub in full_subdomains}
            for future in concurrent.futures.as_completed(futures):
                sub = futures[future]
                result = future.result()
                if result:
                    sub_url = f"{self.scheme}://{result}"
                    self.found_urls.add(sub_url)
                    print(f"[+] Subdomain found: {result}")
        print("[*] Subdomain enumeration completed.")

    def resolve_subdomain(self, subdomain):
        try:
            answers = dns.resolver.resolve(subdomain, 'A')
            return subdomain
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            return None

    def load_wordlist(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(f"[!] Wordlist file not found: {filepath}")
            return []

    def save_results(self):
        print(f"[*] Saving results to {self.output_file}...")
        with open(self.output_file, 'w') as f:
            for url in sorted(self.found_urls):
                f.write(url + '\n')
        print("[*] Results saved successfully.")

    def run(self):
        self.crawl()
        self.directory_brute_force()
        self.page_brute_force()
        self.parameter_fuzzing()
        self.webshell_detection()
        self.subdomain_enumeration()
        self.save_results()

def main():
    print("=== Comprehensive Website Enumerator ===")
    base_url = input("Enter the target domain or URL (e.g., example.com or http://example.com): ").strip()

    dir_wordlist_choice = input("Choose directory wordlist size:\n1. Medium (default)\n2. Large\nEnter choice [1/2]: ").strip()
    if dir_wordlist_choice == '2':
        dir_wordlist = LARGE_DIR_WORDLIST
    else:
        dir_wordlist = DEFAULT_DIR_WORDLIST

    subdomain_wordlist = SUBDOMAIN_WORDLIST

    output_file = input("Enter output file name (e.g., burp_import.txt): ").strip()
    if not output_file:
        output_file = 'burp_import.txt'

    enumerator = WebsiteEnumerator(base_url, dir_wordlist, subdomain_wordlist, output_file)
    enumerator.run()
    print("=== Enumeration Completed ===")
    print(f"All discovered URLs have been saved to {output_file}.")
    print("You can import this file into Burp Suite's site map.")

if __name__ == "__main__":
    main()

