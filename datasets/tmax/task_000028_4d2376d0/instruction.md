You are a Database Reliability Engineer managing backups for a complex microservice architecture. 

Our backup metadata is stored in an SQLite database, but our service dependency graph is modeled as RDF. We need a unified report identifying which services are impacted by currently failing datastore backups.

**Phase 1: Graph Database Setup**
1. Download Apache Jena Fuseki (version 4.9.0 is recommended: `wget https://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-4.9.0.tar.gz`).
2. Extract it and start the Fuseki server in the background on port 3030 with an in-memory dataset named `/ds` that allows updates (e.g., `./fuseki-server --update --mem /ds &`).
3. We have provided an RDF file at `/home/user/architecture.ttl`. Upload this file to your running Fuseki instance's `/ds` dataset using `curl` or Fuseki's `s-put` script.

**Phase 2: Relational Database**
You have an SQLite database at `/home/user/backups.db` with two tables:
* `datastores` (`id` INTEGER, `name` TEXT, `uri` TEXT)
* `backups` (`id` INTEGER, `datastore_id` INTEGER, `timestamp` DATETIME, `status` TEXT, `size_bytes` INTEGER)
*Note: The `uri` in the `datastores` table matches the RDF resource URI.*

**Phase 3: Cross-Query Python Script**
Write a Python script at `/home/user/analyze.py` that does the following:
1. Connects to `/home/user/backups.db`.
2. Uses a complex SQL query (e.g., with window functions or subqueries) to identify `datastores` where the **most recent** backup job (by `timestamp`) has a `status` of `'FAILED'`.
3. For each of these failing datastores, calculate the **average `size_bytes`** of all historically `'SUCCESS'` backups for that specific datastore (to estimate the un-backed-up data size). If there are no successful backups, the average should be 0.
4. Uses parameterized SPARQL queries via the `SPARQLWrapper` library to query the Fuseki server. For each failing datastore, find the URIs of all microservices that depend on it **transitively** (i.e., service -> dependsOn -> ... -> dependsOn -> datastore). The predicate used in the RDF is `<http://example.org/dependsOn>`.
5. Outputs a JSON file to `/home/user/critical_failures.json`.

**Output Format requirement for `/home/user/critical_failures.json`**:
```json
{
  "datastore_name_1": {
    "avg_successful_size": 1024.5,
    "impacted_services": ["http://example.org/ServiceA", "http://example.org/ServiceB"]
  }
}
```
*Note: `impacted_services` must be sorted alphabetically.*

Ensure you install any necessary Python packages (like `SPARQLWrapper`) using pip. Execute your script so the JSON file is created.