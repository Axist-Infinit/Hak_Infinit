# scripts/utils/output_parser.py

import re

def extract_ips(text):
    """
    Extracts all IP addresses from the given text.

    :param text: The input text.
    :return: A list of extracted IP addresses.
    """
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    return ip_pattern.findall(text)

def extract_urls(text):
    """
    Extracts all URLs from the given text.

    :param text: The input text.
    :return: A list of extracted URLs.
    """
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return url_pattern.findall(text)

def extract_emails(text):
    """
    Extracts all email addresses from the given text.

    :param text: The input text.
    :return: A list of extracted email addresses.
    """
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return email_pattern.findall(text)

def parse_nmap_services(nmap_output):
    """
    Parses Nmap output to extract open ports and associated services.

    :param nmap_output: The raw output from an Nmap scan.
    :return: A dictionary with ports as keys and services as values.
    """
    service_pattern = re.compile(r'(\d{1,5})/tcp\s+open\s+(\S+)')
    services = {}
    for match in service_pattern.findall(nmap_output):
        port, service = match
        services[int(port)] = service
    return services
