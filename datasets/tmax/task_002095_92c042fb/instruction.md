You are a Database Reliability Engineer managing a complex backup validation pipeline. Our backup metadata spans across multiple systems:
1. **PostgreSQL** (stores backup schedules and relational metadata)
2. **MongoDB** (stores raw backup logs and document metadata)
3. **Redis** (caches validated backup manifest lineages)

You have been given access to `/app/`, which contains a multi-service orchestration script (`/app/start_services.sh`) that brings up these three services. 

There are two main issues you must resolve in this multi-stage workflow:

**Part 1: Fix the Cross-Representation Query Pipeline**
Inside `/app/query_lineage.py`, there is a data retrieval pipeline that fetches schedule metadata from PostgreSQL and joins it with backup logs in MongoDB to generate a Graph representation (a JSON lineage manifest). 
However, the SQL query inside this file is poorly written. It contains an implicit cross join that causes a massive explosion in returned rows, mapping every schedule to every backup log regardless of the `schedule_id`. 
1. Fix the SQL query in `/app/query_lineage.py` to perform a proper `JOIN` between `schedules` and `backup_runs` on `schedule_id`.
2. Add a NoSQL aggregation pipeline in the script that correctly groups the MongoDB logs by `run_id`.
3. To ensure performance, connect to MongoDB and create an ascending index on the `run_id` field in the `backup_logs` collection.
4. Modify `/app/.env` to include the correct connection strings to allow the script to connect to all three local services (PostgreSQL on 5432, MongoDB on 27017, Redis on 6379).

**Part 2: Build the Manifest Verifier (Adversarial Corpus)**
Our pipeline has been processing corrupted and malicious backup manifests. You must write a Python script at `/app/verify_manifest.py` that acts as a gatekeeper.
The script must take a single command-line argument (the path to a JSON manifest file) and print exactly `VALID` or `INVALID` to standard output. 

A manifest is considered `INVALID` (evil) if it meets ANY of the following criteria:
- The graph structure contains a cycle (e.g., Backup A depends on B, which depends on A).
- It contains unmatched cross-representation IDs (a Postgres `schedule_id` that does not match the regex pattern `SCH-\d{4}`).
- The document metadata contains injected NoSQL operators in the keys (any key starting with `$`).

A manifest is considered `VALID` (clean) if it is a proper Directed Acyclic Graph (DAG) with valid IDs and no NoSQL injection attempts.

Test your script thoroughly. Automated grading will evaluate `/app/verify_manifest.py` against a hidden corpus of clean and evil JSON manifests.

Your final goal is a working multi-service pipeline where `python /app/query_lineage.py` completes successfully without memory exhaustion, and your `/app/verify_manifest.py` flawlessly classifies the adversarial corpus.