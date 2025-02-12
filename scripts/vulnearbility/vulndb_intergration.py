"""
scripts/vulnerability/vulndb_integration.py

Enhanced logic to query an external vulnerability database (e.g., VulnDB, NVD)
to confirm if a discovered CVE is relevant to a specific version or product.
"""

import requests
import re
from core.log_manager import logger
from core import db_manager

def query_vulndb(cve_id):
    """
    Query a vulnerability database API for CVE details.
    This example uses a placeholder "https://vuldb.com/?id.<cve>" 
    but in practice, you'd have a real API to parse JSON or XML.
    """
    url = f"https://vuldb.com/?id.{cve_id}"
    logger.info(f"Querying VulnDB for {cve_id} at {url}")
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.text  # Or parse JSON if the API returns JSON
        else:
            logger.error(f"Failed to fetch data for {cve_id}, status code {resp.status_code}")
    except Exception as e:
        logger.error(f"Error connecting to VulnDB: {e}")
    return None

def is_cve_applicable(cve_text, product_name, product_version):
    """
    Heuristic function that attempts to see if 'cve_text' references
    the 'product_name' and possibly the 'product_version' range.

    Return True if it likely applies, False otherwise.
    """
    # Very naive approach: check if product name appears in CVE text
    # and if version range is suggested to include our version.
    # In a real system, you'd parse official JSON fields from NVD:
    # cpe_uri, version_start, version_end, etc.
    if product_name.lower() not in cve_text.lower():
        return False

    if product_version:
        # For example, if the CVE text says "Apache 2.4.x < 2.4.48" 
        # and we have 2.4.29, we can see if it's included.
        version_pattern = re.compile(product_version, re.IGNORECASE)
        if version_pattern.search(cve_text):
            return True
        # Possibly parse ranges like "affected versions < 1.3.5"
        # This requires more advanced logic. 
        # We'll keep it simple for demonstration:
    else:
        # If no product version is known, at least check product name
        return True

    return False

def confirm_cve_relevance(service_id, cve_id, product_name, product_version):
    """
    1) Query the VulnDB (or NVD) for the CVE content
    2) Check if it likely applies to the discovered product & version
    3) Store a 'potential_vulnerability' record if relevant
    """
    cve_text = query_vulndb(cve_id)
    if not cve_text:
        return False

    applies = is_cve_applicable(cve_text, product_name, product_version)
    if applies:
        logger.info(f"CVE {cve_id} likely applies to {product_name} {product_version}")
        # store in DB as a new potential vulnerability
        db_manager.store_vulnerability(
            service_id=service_id,
            vuln_name=f"CVE {cve_id}",
            description=f"Likely relevant to {product_name} {product_version}",
            references=url_for(cve_id=cve_id),
            severity=None
        )
    else:
        logger.info(f"CVE {cve_id} does NOT appear relevant to {product_name} {product_version}")

    return applies

def url_for(cve_id):
    # Helper function to construct a link to the CVE
    return f"https://vuldb.com/?id.{cve_id}"
