
Script Framework structure:
===========================
hakinfinit-framework/
├── core/
│   ├── __init__.py
│   ├── main.py               # Main entry point for the framework
│   ├── db_manager.py         # Handles database connections/queries
│   ├── config_manager.py     # Reads config (like DB creds, file paths)
│   ├── parser_manager.py     # Utility functions for parsing Nmap output
│   └── executor.py           # Logic to orchestrate which enumeration scripts to run, etc.
│
├── scripts/
│   ├── __init__.py
│   ├── nmap/
│   │   ├── run_nmap.py       # Functions to run Nmap scans
│   │   └── parse_results.py  # Functions to parse the XML/greppable output of Nmap
│   │
│   ├── enumeration/
│   │   ├── ftp_enum.py       
│   │   ├── ssh_enum.py       
│   │   ├── http_enum.py     
│   │   ├── smb_enum.py      
│   │   ├── rdp_enum.py       
│   │   ├── mysql_enum.py      
│   │   ├── mssql_enum.py      
│   │   ├── winrm_enum.py
│   │   ├── telnet_enum.py
│   │   ├── oracle_enum.py     
│   │   ├── postgres_enum.py
│   │   ├── vnc_enum.py
│   │   ├── redis_enum.py    
│   │   ├── citrix_enum.py
│   │   ├── es_enum.py
│   │   └── ... 
│   │
│   ├── vulnerability/
│   │   ├── searchsploit_integration.py  # Logic to query searchsploit
│   │   └── vulndb_integration.py        # Logic to query VulnDB or related APIs
│   │
│   └── utils/
│       ├── __init__.py
│       ├── common.py         # Common helper functions
│       └── output_parser.py  # Additional parser helpers (regex, text extraction, etc.)
│
├── database/
│   ├── migrations/
│   │   └── V1__initial_schema.sql  # Example migration file
│   ├── schema.sql                  # Core DB schema for hosts, services, vulnerabilities
│   └── seed_data.sql               # If you have any seed data or test data
│
├── config/
│   ├── database.ini      # Example: DB config file with credentials, host, port
│   ├── framework.ini     # Example: general framework settings
│   └── tool_mapping.yml  # Mappings from service/port to enumeration scripts
│
├── tests/
│   ├── __init__.py
│   ├── test_nmap_parsing.py    # Unit tests for Nmap parsing
│   ├── test_db_integration.py  # Tests for database connectivity
│   ├── test_enumeration.py     # Tests for enumeration scripts
│   └── test_vuln_lookup.py     # Tests for searchsploit/vulndb integration
│
├── logs/
│   └── .gitkeep   # Or keep empty for real-time logs from your scripts
│
├── .gitignore
├── requirements.txt   # Python dependencies (e.g., psycopg2, lxml, etc.)
├── README.md          # Project documentation
└── LICENSE            # License of your choice
