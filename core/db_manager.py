"""
core/db_manager.py

Handles database connections and queries for the HakInfinit framework.
"""

import psycopg2
import psycopg2.extras
from core.config_manager import get_db_config
from core.log_manager import logger

connection = None

def init_db():
    """
    Initializes a connection to the PostgreSQL database. 
    Creates necessary tables if they don't exist (by running migrations).
    """
    global connection
    db_config = get_db_config()
    try:
        connection = psycopg2.connect(
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
        connection.autocommit = True
        logger.info("Database connection established.")
        # Optional: call run_migrations() here if you want automatic migrations
    except Exception as e:
        logger.error(f"Failed to connect to DB: {e}")

def run_query(query, params=None):
    """
    Runs a query (SELECT, INSERT, UPDATE, DELETE) against the database.
    Returns a cursor.fetchall() for SELECT queries, or None otherwise.
    """
    if not connection:
        logger.error("No DB connection established. Call init_db() first.")
        return None
    try:
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params if params else ())
            if cur.description:  # It's a SELECT query
                return cur.fetchall()
            else:
                return None
    except Exception as e:
        logger.error(f"Database query error: {e}")
        return None

def store_host(ip, hostname=None):
    """
    Insert or update a host record in the database. Returns the host_id.
    """
    select_q = "SELECT id FROM hosts WHERE ip = %s;"
    result = run_query(select_q, (ip,))
    if result:
        host_id = result[0]['id']
        update_q = "UPDATE hosts SET hostname = %s WHERE id = %s;"
        run_query(update_q, (hostname, host_id))
        return host_id
    else:
        insert_q = "INSERT INTO hosts (ip, hostname) VALUES (%s, %s) RETURNING id;"
        result = run_query(insert_q, (ip, hostname))
        if result:
            return result[0]['id']
    return None

def store_service(host_id, port, protocol, service_name, version=None):
    """
    Insert or update a service for a given host. Returns the service_id.
    """
    select_q = """SELECT id FROM services 
                  WHERE host_id = %s AND port = %s AND protocol = %s;"""
    result = run_query(select_q, (host_id, port, protocol))
    if result:
        service_id = result[0]['id']
        update_q = """UPDATE services 
                      SET service_name = %s, version = %s 
                      WHERE id = %s;"""
        run_query(update_q, (service_name, version, service_id))
        return service_id
    else:
        insert_q = """INSERT INTO services (host_id, port, protocol, service_name, version) 
                      VALUES (%s, %s, %s, %s, %s)
                      RETURNING id;"""
        result = run_query(insert_q, (host_id, port, protocol, service_name, version))
        if result:
            return result[0]['id']
    return None

def store_vulnerability(service_id, vuln_name, description, references=None, severity=None):
    """
    Insert a new vulnerability record for a given service.
    """
    insert_q = """INSERT INTO vulnerabilities
                  (service_id, vuln_name, description, references, severity)
                  VALUES (%s, %s, %s, %s, %s);"""
    run_query(insert_q, (service_id, vuln_name, description, references, severity))

def get_services_for_host(host_id):
    """
    Retrieve all services for the given host_id.
    """
    q = "SELECT * FROM services WHERE host_id = %s;"
    return run_query(q, (host_id,))

def get_all_hosts():
    """
    Returns all hosts from the DB.
    """
    q = "SELECT * FROM hosts;"
    return run_query(q)

def close_db():
    """
    Closes the database connection.
    """
    global connection
    if connection:
        connection.close()
        connection = None
        logger.info("Database connection closed.")
