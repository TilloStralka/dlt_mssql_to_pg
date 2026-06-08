# DLT MSSQL to PostgreSQL

## Reference Architecture for On-Prem Healthcare Data Integration

This repository contains a proof of concept (PoC) for transferring data from a source database into PostgreSQL using **dlt (Data Load Tool)** and **Docker**.

The current implementation uses:

```text
Microsoft SQL Server (AdventureWorks)
            ↓
            dlt
            ↓
PostgreSQL
```

The long-term goal is to use this project as a reference architecture for an on-premises healthcare environment where sensitive data is transferred from an operational source system (e.g. Oracle) into a PostgreSQL-based analytics or integration platform.

---

## Project Goals

### Current Proof of Concept

Validate the following concepts in a local development environment:

* Database-to-database extraction using dlt
* Automated schema discovery
* Table creation in PostgreSQL
* Containerized execution using Docker
* Logging and monitoring
* Secure credential management

### Target Architecture

Future production scenario:

```text
Oracle Database
       ↓
       ↓ dlt Pipeline
       ↓
PostgreSQL
       ↓
Analytics / Reporting / Integration Layer
```

The PostgreSQL database is expected to run on the same on-prem server as the ETL process, while the source database may reside on a separate internal database server.

---

## Repository Structure

```text
DLT_MSSQL_TO_PG/
│
├── .dlt/
│   ├── config.toml
│   └── secrets.toml
│
├── logs/
│
├── pg_dlt/
│   └── Local Python virtual environment
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
│
├── requirements.txt
├── mssql_to_postgres.py
│
└── README.md
```

---

## Technology Stack

* Python 3.12
* dlt
* SQLAlchemy
* pyodbc
* PostgreSQL
* Microsoft SQL Server
* Docker
* Docker Compose

---

## Architecture Overview

```text
+---------------------+
| Microsoft SQL Server|
| AdventureWorks      |
+----------+----------+
           |
           |
           v
+---------------------+
| dlt Pipeline        |
| Docker Container    |
+----------+----------+
           |
           |
           v
+---------------------+
| PostgreSQL          |
| dlt_data            |
+---------------------+
```

---

## Prerequisites

### Software

* Docker Desktop
* PostgreSQL
* Microsoft SQL Server
* Python 3.12 (optional for local execution)

### Database Access

The source and target systems must be reachable from the machine executing the container.

Required:

* Database host
* Port
* Service account
* Password
* Appropriate read/write permissions

---

## Configuration

### dlt Secrets

Configuration is stored in:

```text
.dlt/secrets.toml
```

Example:

```toml
[sources.sql_database.credentials]
drivername = "mssql+pyodbc"
database = "AdventureWorks"
host = "host.docker.internal"
port = 1433
username = "dlt_loader"
password = "********"

query = { driver = "ODBC Driver 17 for SQL Server", TrustServerCertificate = "yes" }

[destination.postgres.credentials]
drivername = "postgresql+psycopg2"
database = "dlt_data"
host = "host.docker.internal"
port = 5432
username = "postgres"
password = "********"
```

### Important

Do not commit production credentials to Git.

Recommended approaches:

* Environment variables
* Docker secrets
* Vault solutions
* Encrypted configuration management

---

## Build Docker Image

From the repository root:

```bash
docker compose build
```

---

## Run the Pipeline

Execute a single load run:

```bash
docker compose run --rm dlt_mssql_to_pg
```

Expected output:

```text
Pipeline mssql_to_postgres load step completed
1 load package(s) were loaded
```

---

## Local Execution (Optional)

Activate the virtual environment:

```bash
pg_dlt\Scripts\activate
```

Run the pipeline directly:

```bash
python mssql_to_postgres.py
```

---

## Logging

The pipeline generates structured logs.

Example:

```text
logs/
├── mssql_to_postgres_20260608_135616.log
├── mssql_to_postgres_20260608_140102.log
└── ...
```

Information logged:

* Pipeline name
* Source table
* Destination dataset
* Load package IDs
* Execution status
* Errors and stack traces

---

## Current Test Scenario

Current implementation:

```text
Source:
    MSSQL AdventureWorks

Table:
    dbo.AWBuildVersion

Destination:
    PostgreSQL

Schema:
    adventureworks

Table:
    aw_build_version
```

---

## Scaling to Additional Tables

Current code loads a single table:

```python
source = sql_database(
    schema="dbo"
).with_resources("AWBuildVersion")
```

Additional tables can be added by changing:

```python
schema="Person"
```

and

```python
.with_resources("Address")
```

or by extending the pipeline to process multiple resources.

---

## Data Loading Strategies

dlt supports multiple loading modes:

### Replace

Recreate destination table contents:

```python
write_disposition="replace"
```

### Append

Insert new rows only:

```python
write_disposition="append"
```

### Merge

Update existing rows based on primary keys:

```python
write_disposition="merge"
```

---

## Healthcare Considerations

This repository is intended as a foundation for healthcare data integration projects.

Recommended production practices:

* Service accounts only
* Principle of least privilege
* No patient data in logs
* TLS encrypted database connections
* Centralized log management
* Secrets management
* Auditing and monitoring

All deployments should remain inside the organization's protected network.

---

## Future Enhancements

Planned next steps:

* Oracle source integration
* Incremental loading
* CDC (Change Data Capture)
* SCD Type 2 historization
* Scheduling (cron / Windows Task Scheduler / Kubernetes Jobs)
* Monitoring and alerting
* CI/CD pipeline integration

---

## Status

Current status:

```text
Proof of Concept Completed

MSSQL → PostgreSQL
Dockerized
Logging enabled
Ready for Oracle migration prototype
```
