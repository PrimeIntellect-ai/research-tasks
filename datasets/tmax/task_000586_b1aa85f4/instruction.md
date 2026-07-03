You are a Database Reliability Engineer managing backups for a complex microservices architecture. The infrastructure dependencies are regularly backed up as an RDF graph in N-Triples format.

Your task is to create a robust Bash tooling system to query this backup, verify dependencies for specific servers, and maintain a fast-lookup index of your queries.

We have provided two files in your home directory (`/home/user`):
1. `graph_backup.nt`: An N-Triples file containing the graph database backup.
2. `run_sparql.py`: A Python utility that executes SPARQL queries against an RDF file. It accepts `--data` and `--query` arguments and outputs standard SPARQL JSON results. (Note: you must install the `rdflib` Python package first to use it).

**Your Objectives:**

1. **Environment Setup:** Ensure the `rdflib` package is installed for the Python environment so the provided `run_sparql.py` works. Also, ensure `jq` is installed.

2. **Create the Verification Script:** Write a Bash script at `/home/user/check_deps.sh` that takes a single server name as an argument (e.g., `AppServer`). The script must:
   - **Construct a Parameterized Query:** Dynamically generate a valid SPARQL `SELECT` query to find all nodes the given server depends on. 
     - The subject URI format is `<http://example.org/server/{SERVER_NAME}>`.
     - The predicate URI is `<http://example.org/vocab/dependsOn>`.
     - Select a single variable `?dep` representing the object URIs.
     - Save this query to a temporary file.
   - **Execute the Query:** Use `python3 /home/user/run_sparql.py` to run the generated query against `/home/user/graph_backup.nt`.
   - **Format Conversion:** Use `jq` to parse the standard SPARQL JSON output from the Python script. Extract just the server names from the returned `?dep` URIs (i.e., extract `DB_Primary` from `http://example.org/server/DB_Primary`). 
   - **Export Result:** Output a clean JSON file to `/home/user/deps_{SERVER_NAME}.json`. The format must be exactly:
     `{"server": "AppServer", "dependsOn": ["DB_Primary", "Redis_Cache"]}` (Array elements should be sorted alphabetically).
   - **Index Strategy:** To speed up future audits, the script must append a record of the query to a flat-file index at `/home/user/query_index.csv`. The format should be `ServerName,Dependency1|Dependency2` (dependencies sorted alphabetically, joined by a pipe). If the server has no dependencies, leave the right side of the comma empty.

3. **Execution:** Run your script for two specific servers to verify functionality:
   - `./check_deps.sh AppServer`
   - `./check_deps.sh DB_Primary`

**Constraints & Notes:**
- You must use Bash for the main script. You may use standard Linux utilities (`jq`, `awk`, `sed`, `grep`, etc.).
- Ensure your script correctly handles the extraction of the base server name from the full URIs.