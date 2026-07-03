You are a Database Reliability Engineer managing disaster recovery for a complex microservices architecture. Our internal backup scheduling API has broken down, and you need to fix it and implement a missing feature that prioritizes backups based on graph dependencies and database metadata.

We have a vendored package located at `/app/vendor/db-backup-api` which contains the FastAPI application for this service. 

Your tasks are as follows:

1. **Fix the Vendored Package:**
   The package at `/app/vendor/db-backup-api` is broken. 
   - Its launch script (`launch.sh`) has a typo that prevents the server from starting.
   - Its configuration file (`config.py`) points to hardcoded, invalid paths instead of the actual data directory `/home/user/data/`.
   Fix these issues so the application can run.

2. **Implement the Backup Prioritization Logic:**
   Edit the main application file (`api.py`) to implement the HTTP GET endpoint `/prioritize-backups`.
   The endpoint must do the following:
   - Read the NoSQL-style document dump of database metadata located at `/home/user/data/backup_metadata.json`.
   - Read the database dependency graph located at `/home/user/data/db_dependencies.json`. The graph is an array of objects `{"source": "X", "target": "Y"}` indicating that database X depends on database Y.
   - Filter out any database from the metadata that has `"tier": 3` (these are non-critical, like logs, and shouldn't be in the priority queue).
   - Calculate the **In-Degree** (number of databases that depend on it) for each remaining database. For example, if A depends on B, and C depends on B, the in-degree of B is 2.
   - Calculate a Priority Score for each database using the formula: `Score = (In-Degree + 1) * (1000 / size_gb)` where `size_gb` is read from the metadata file.
   - Return a JSON response containing the top 5 databases sorted by `Score` in descending order. The response format must be strictly:
     `{"priority_backups": ["db_name1", "db_name2", ...]}`

3. **Deploy the Service:**
   Once fixed and implemented, run the `launch.sh` script to start the API. The API must listen continuously on `127.0.0.1:8080`. Do not shut it down; leave it running in the background or in an active terminal session so our verification system can query it.