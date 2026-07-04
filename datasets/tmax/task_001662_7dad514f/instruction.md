You are a Database Reliability Engineer managing an on-demand partial backup system. Our internal users can request partial data dumps by specifying a list of tables and filters via JSON. However, a severe issue has been causing database outages: users are submitting requests for tables that have no relationship, causing our backup extraction tool to generate SQL queries with implicit cross joins (Cartesian products), which overwhelm the database.

We have a multi-service setup in `/app/`:
1. PostgreSQL (listening on port 5432) containing the production schema.
2. Redis (listening on port 6379) used for tracking backup job states.
3. A Go-based backup extraction service located in `/app/backup-service`.

Your task is to write a Go CLI tool (`/app/backup-service/validator.go`) that acts as a schema-aware query validator. It must prevent cross-join outages by ensuring that any requested subset of tables forms a **single connected component** based on the database's Foreign Key constraints.

Requirements:
1. **Service Configuration**: Ensure Postgres and Redis are running. A startup script `/app/start_services.sh` is provided, but you may need to configure the database credentials in `/app/backup-service/config.env` so the Go tool can connect (DB: `backup_db`, User: `postgres`, Pass: `postgres`).
2. **Schema Analysis**: Your Go tool must connect to PostgreSQL, analyze `pg_constraint` or `information_schema`, and build an undirected graph of table relationships based on Foreign Keys.
3. **Validation Logic**: The tool must accept a JSON file path via a command-line argument (e.g., `go run validator.go /path/to/request.json`). 
   - The JSON contains a list of tables: `{"tables": ["table1", "table2"]}`.
   - If the requested tables are fully connected (i.e., there is a path between every pair of tables in the request using only the tables present in the request and their FK relationships), print `ACCEPT` to standard output and exit with code 0.
   - If the tables are disconnected (which would result in an implicit cross join), print `REJECT` to standard output and exit with code 1.

We have provided two corpora of backup requests to test your implementation:
- `/app/corpus/clean/`: Contains valid JSON requests where tables are properly connected. Your tool must ACCEPT 100% of these.
- `/app/corpus/evil/`: Contains malicious or poorly formed JSON requests that cause implicit cross joins (disconnected tables). Your tool must REJECT 100% of these.

Write your solution in `/app/backup-service/validator.go`. You may use standard Go libraries or the `lib/pq` driver which is already initialized in the Go module.