You are tasked with a forensic investigation and system recovery for a telemetry ingestion pipeline. 

The system is a multi-service application located in `/home/user/app/repo`. It consists of:
1. An API endpoint (`api_server.sh`) running on port 8080 using `socat` to accept incoming telemetry payloads.
2. A background worker (`worker.sh`) that tails a spool file and inserts records into an SQLite database (`/home/user/app/data.db`).

Recently, a severe regression was merged into the `main` branch. Symptoms include:
- The worker daemon sporadically hangs and stops processing data, leaving the SQLite database in an uncheckpointed state with a massive Write-Ahead Log (WAL) file (`data.db-wal`).
- Telemetry processing throughput has collapsed.
- The pipeline drops data during these hangs.

Your objectives:
1. **Bisect the Regression**: The repository in `/home/user/app/repo` has 200 commits. Use `git bisect` (or another method) to identify the exact commit that introduced the bug in `worker.sh`. The bug involves an infinite loop/recursion trigger and causes the script to hang when it encounters a specific statistical anomaly in the sensor data.
2. **Fix the Code**: Once identified, fix the bug in `worker.sh` on the `main` branch so that the worker gracefully handles the anomaly without hanging or dropping records.
3. **Service Integration**: Restart the services using `/home/user/app/repo/start_services.sh`. Verify that data flows end-to-end (from port 8080 to the SQLite DB).
4. **Data Recovery (Forensics)**: A corrupted production snapshot is located at `/home/user/corrupted_env/`. The main database file is truncated, but the `data.db-wal` file contains thousands of stranded inserts. Recover these records by extracting the stranded telemetry data from the WAL file. Reconstruct the database and save the recovered database to `/home/user/recovered.db` with the table schema: `CREATE TABLE telemetry (id INTEGER PRIMARY KEY, sensor TEXT, value REAL);`. 

Ensure `/home/user/recovered.db` contains as many recovered rows as possible. An automated verifier will check the row count of this database.