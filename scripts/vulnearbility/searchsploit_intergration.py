"""
scripts/vulnerability/searchsploit_integration.py

Enhanced logic to query searchsploit with service name + version,
parse results, and store potential exploit references
that match discovered services/ports.

We don't launch any exploit automatically;
we only record suggestions for further manual review.
"""

import subprocess
import re
from core.log_manager import logger
from core import db_manager

def searchsploit_lookup(term):
    """
    Runs 'searchsploit <term>' and returns the raw results as a string.
    """
    logger.info(f"Running searchsploit for term: {term}")
    cmd = ["searchsploit", term, "--exclude", "papers,shellcodes"]  
    # 'exclude' example: skip papers or shellcodes if you want less noise
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"searchsploit failed: {e}")
        return None

def parse_searchsploit_results(raw_results, version=None):
    """
    Parse the raw searchsploit output into a structured list of exploit references.
    If 'version' is provided, attempt to filter or highlight exploits referencing that version.
    Returns a list of dictionaries, e.g.:
    [
      {
        "title": "PHP 8.1.0 - 'xyz' Remote Code Execution",
        "path": "/usr/share/exploitdb/exploits/php/webapps/12345.txt",
        "verified_version_match": True / False
      },
      ...
    ]
    """
    if not raw_results:
        return []

    lines = raw_results.splitlines()
    # Typical searchsploit format has lines like:
    #   ------------------------------------------------------------------------------- ---------------------------------
    #   Exploit Title                                                                  |  Path
    #   ------------------------------------------------------------------------------- ---------------------------------
    #   ...
    # We'll do a simple parse ignoring the header lines.

    exploit_data = []
    columns_pattern = re.compile(r'\s*\|\s*')  # pattern to split at ' | ' if there's consistent formatting
    for line in lines:
        if not line.strip() or "-----" in line or "Exploit Title" in line:
            continue

        # Attempt to split the line by " | "
        parts = columns_pattern.split(line.strip())
        if len(parts) == 2:
            title, path = parts
            # Heuristic check if the version is mentioned in the title
            verified_version_match = False
            if version and re.search(re.escape(version), title, re.IGNORECASE):
                verified_version_match = True

            exploit_data.append({
                "title": title.strip(),
                "path": path.strip(),
                "verified_version_match": verified_version_match
            })
        else:
            # If the format is inconsistent, you could do a simpler parse
            # or skip the line
            pass

    return exploit_data

def suggest_exploits_for_service(service_id, service_name, version=None, host_os=None):
    """
    High-level function that:
    1) Queries searchsploit with 'service_name version' (if version is known)
    2) Parses results
    3) (Optional) Filters out results that don't match the host OS, if known
    4) Stores suggested exploits in DB (or returns them)
    """

    # 1) Build the search term
    if version:
        term = f"{service_name} {version}"
    else:
        # fallback
        term = service_name

    raw_results = searchsploit_lookup(term)
    exploit_suggestions = parse_searchsploit_results(raw_results, version=version)

    # 2) Optionally refine suggestions by host OS
    refined_suggestions = []
    if host_os:
        # Example: skip "Linux" exploits if host OS is "Windows"
        # This is naive—some exploits might be cross-platform
        for item in exploit_suggestions:
            title_lower = item["title"].lower()
            # Quick heuristic filters
            if "windows" in host_os.lower():
                if "linux" in title_lower:
                    # skip it
                    continue
            elif "linux" in host_os.lower():
                if "windows" in title_lower:
                    # skip it
                    continue
            refined_suggestions.append(item)
    else:
        refined_suggestions = exploit_suggestions

    # 3) Store them in DB (or do something else)
    for suggestion in refined_suggestions:
        db_manager.store_suggested_exploit(
            service_id=service_id,
            exploit_title=suggestion["title"],
            exploit_path=suggestion["path"],
            verified_version_match=suggestion["verified_version_match"]
        )

    logger.info(f"Found {len(refined_suggestions)} potential exploits for {service_name} (id={service_id}).")

    return refined_suggestions
