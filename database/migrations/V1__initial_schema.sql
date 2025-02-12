-- database/migrations/V1__initial_schema.sql
-- Basic schema for hosts, services, vulnerabilities

CREATE TABLE IF NOT EXISTS hosts (
    id SERIAL PRIMARY KEY,
    ip VARCHAR(255) NOT NULL UNIQUE,
    hostname VARCHAR(255),
    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    host_id INT REFERENCES hosts(id) ON DELETE CASCADE,
    port INT NOT NULL,
    protocol VARCHAR(50),
    service_name VARCHAR(255),
    version VARCHAR(255),
    UNIQUE (host_id, port, protocol)
);

CREATE TABLE IF NOT EXISTS vulnerabilities (
    id SERIAL PRIMARY KEY,
    service_id INT REFERENCES services(id) ON DELETE CASCADE,
    vuln_name VARCHAR(255) NOT NULL,
    description TEXT,
    references TEXT,
    severity VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Potential credential table:
CREATE TABLE IF NOT EXISTS credentials (
    id SERIAL PRIMARY KEY,
    service_id INT REFERENCES services(id) ON DELETE CASCADE,
    username VARCHAR(255),
    password VARCHAR(255),
    hash_type VARCHAR(50),
    discovered_at TIMESTAMP DEFAULT NOW()
);
