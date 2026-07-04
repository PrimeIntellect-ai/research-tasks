You are a Database Reliability Engineer managing backup systems. We have an automated pipeline that exports infrastructure metadata to determine which databases need to be backed up and according to which policies. 

Our metadata is stored as an RDF graph. There is an existing Python script at `/home/user/export_backup_metadata.py` that queries this RDF graph (`/home/user/infrastructure.ttl`) using SPARQL to generate a backup manifest.

However, the pipeline is currently failing. The SPARQL query inside the script contains a subtle flaw (equivalent to an implicit cross join in SQL) because it fails to properly connect the graph patterns. As a result, it computes a Cartesian product, assigning every single backup policy to every single database, which causes the downstream backup runners to duplicate work exponentially.

Your tasks:
1. Install any necessary Python dependencies (the script uses `rdflib`).
2. Analyze and fix the SPARQL query in `/home/user/export_backup_metadata.py`. The query should correctly traverse the graph: Databases are hosted on Hosts, and Hosts have Backup Policies. You must extract the database name and the policy name.
3. Ensure the script executes the query, interprets the results, and materializes this projection into a JSON file at `/home/user/backup_manifest.json`.
4. The JSON file must be a list of objects, each with exactly two keys: `"database"` and `"policy"`, sorted alphabetically by the database name.

Example expected format for `/home/user/backup_manifest.json`:
```json
[
  {
    "database": "customers_db",
    "policy": "daily_incremental"
  }
]
```

Fix the script and run it to produce the correct `backup_manifest.json`.