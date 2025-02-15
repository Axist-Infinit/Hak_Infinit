"""
core/parser_manager.py

Utility functions for parsing Nmap output or other scan outputs.
May call into scripts/nmap/parse_results.py or other specialized parsers.
"""

from scripts.nmap.parse_results import parse_nmap_xml

def parse_nmap_file(filepath):
    """
    High-level function to parse Nmap XML/greppable output.
    """
    # In this example, we simply defer to parse_nmap_xml
    return parse_nmap_xml(filepath)
