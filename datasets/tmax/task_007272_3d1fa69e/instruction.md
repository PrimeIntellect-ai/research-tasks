You are a Database Reliability Engineer investigating the backup status of a microservices architecture. The service dependency graph and recent backup metadata have been dumped into an SQLite database at `/home/user/infrastructure.db`.

Your task is to write a C++ program that analyzes this database, performs a graph projection using complex SQL queries, and exports the vulnerable sub-graph to a JSON file.

### Objectives

1. **Setup:** Install necessary dependencies (e.g., `libsqlite3-dev`, `g++`) to write and compile a C++ program that interacts with SQLite3.

2. **Schema Analysis:** The database `/home/user/infrastructure.db` has the following schema:
   - `services (service_id INTEGER PRIMARY KEY, service_name TEXT, is_active INTEGER)`
   - `dependencies (dependency_id INTEGER PRIMARY KEY, provider_id INTEGER, consumer_id INTEGER)` - Represents a directed edge where the `consumer_id` depends on the `provider_id`.
   - `backups (backup_id INTEGER PRIMARY KEY, service_id INTEGER, timestamp INTEGER, status TEXT)` - `status` can be 'SUCCESS' or 'FAILED'.

3. **Query Construction:** Write a single, efficient C++ program (e.g., `/home/user/analyze.cpp`) that connects to this database and executes queries to find:
   - **Vulnerable Services:** All `active` services (is_active = 1) that do NOT have any 'SUCCESS' backups on record.
   - **Impacted Consumers:** All `active` services that directly depend on (are consumers of) the Vulnerable Services.

4. **Graph Materialization & Export:** 
   Your C++ program must project this data into a JSON file at `/home/user/vulnerable_graph.json`.
   The JSON must follow this exact format (compact or pretty-printed, but must be valid JSON):
   ```json
   {
     "vulnerable_nodes": [
       {"service_id": 1, "service_name": "db-auth"}
     ],
     "impacted_edges": [
       {"provider_id": 1, "consumer_id": 4}
     ]
   }
   ```
   *Note: Ensure you only include active services. Order of items in arrays does not matter.*

5. **Execution:** Compile your C++ code and run it so that `/home/user/vulnerable_graph.json` is generated successfully.