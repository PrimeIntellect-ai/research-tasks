You are a Database Reliability Engineer investigating a suspect backup of an internal microservice's edge registry. The backup is an SQLite database located at `/home/user/service_backup.db`. 

We have received reports that secondary indexes in these backups occasionally suffer from silent corruption, causing standard queries to return stale or missing rows. Before restoring this data, we need to extract the raw entity relationships and materialize them into a clean graph structure.

Your task is to write and execute a Python script that accomplishes the following:

1. **Schema Analysis**: Reverse-engineer the schema of `/home/user/service_backup.db` to identify the table storing the assets/nodes (containing their string names) and the table storing the parent-child relationships (edges) between them. Note: the table and column names are not documented, so you will need to inspect the database schema (`sqlite_master`) to figure out the exact structure.
2. **Index Remediation**: Before extracting the data, your script must programmatically drop all secondary (non-primary key) indexes in the database to ensure subsequent queries perform full table scans on the raw heap, bypassing any potentially corrupted indexes.
3. **Graph Projection**: Query the raw tables to extract the full dependency graph. 
4. **Materialization**: Process the relationships into an adjacency list mapping each parent asset's **name** to a list of its direct children's **names**. 
5. **Output**: Save this materialized graph as a formatted JSON file at `/home/user/graph_materialized.json`. 

**Output Requirements for `/home/user/graph_materialized.json`:**
- It must be a single JSON object where keys are parent asset names (strings), and values are arrays of child asset names (strings).
- Assets with no children should not be included as keys in the JSON object.
- The arrays of child names must be sorted alphabetically.
- The JSON file must be nicely formatted (indent=4).

You may use any standard Python libraries (e.g., `sqlite3`, `json`).