import psycopg2

def init_db(db_config):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    # Initialize database schema if necessary
    cursor.execute(open("database/schema.sql", "r").read())
    conn.commit()
    cursor.close()
    conn.close()

def save_nmap_results(target, nmap_output):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    # Save Nmap results to the database
    cursor.execute("INSERT INTO nmap_results (target, output) VALUES (%s, %s)", (target, nmap_output))
    conn.commit()
    cursor.close()
    conn.close()
