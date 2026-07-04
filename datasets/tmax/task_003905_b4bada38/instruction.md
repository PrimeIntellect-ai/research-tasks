You are a data engineer tasked with repairing a multi-service ETL pipeline and writing a robust data transformation script in Bash.

System Environment:
In `/app/`, there is a multi-service setup defining a pipeline. 
Services running:
1. `data-api`: A Flask REST API (port 8080) that serves raw data.
2. `db`: A PostgreSQL database (port 5432).

Your tasks:
1. **Service Configuration (Multi-Service)**:
   The `data-api` service is failing to connect to the `db` service. Check the configuration files in `/app/` (e.g., `docker-compose.yml` or service env files) and correct the database connection parameters so the API can successfully query the database. The database user is `postgres` and password is `secret`. Ensure both services can communicate.

2. **ETL Transformation Script (Bash & Fuzz Equivalence)**:
   Write a Bash script at `/home/user/compute_stats.sh` that acts as the transformation step of the ETL pipeline.
   The script must read a CSV stream from `stdin` containing three columns: `id,val1,val2` (with a header row).
   
   To implement reproducible pipeline testing and sampling, your script must:
   - Discard the header row.
   - Filter the data to create a deterministic sample: ONLY keep rows where the `id` (integer) is exactly divisible by 3 (`id % 3 == 0`).
   - For this filtered sample, compute the **sample covariance** between `val1` and `val2`. 
   - You may use standard Unix tools like `awk` to perform the math.
   
   Output format:
   - Print exactly: `Covariance: <value>` where `<value>` is rounded to exactly 3 decimal places (e.g., `12.345`).
   - If the filtered sample contains fewer than 2 rows (making sample covariance undefined), output exactly: `Covariance: N/A`.

Your script `/home/user/compute_stats.sh` must be executable (`chmod +x`). It will be rigorously tested by a fuzzer that streams thousands of random CSV files to its `stdin` and compares its exact stdout byte-for-byte against a compiled reference oracle.

Ensure your Bash script handles negative numbers, floating-point inputs for val1/val2, and empty inputs gracefully according to the logic above.