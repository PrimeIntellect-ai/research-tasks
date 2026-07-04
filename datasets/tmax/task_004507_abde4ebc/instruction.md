You are a Database Reliability Engineer. We maintain our cluster's backup metadata (full backups, incremental backups, and storage locations) as an RDF knowledge graph in Turtle (.ttl) format. We query this graph to plan restoration jobs and calculate storage requirements.

Our Python environment is restricted, so we use a vendored version of the `rdflib` library located at `/app/rdflib-source`. However, a junior engineer recently made an unauthorized edit to the `rdflib` source code to "disable expensive queries" during an incident, and now our SPARQL engine is broken.

Your objectives:
1. **Fix the Vendored Package**: Locate and fix the intentional breakage in the vendored `rdflib` package at `/app/rdflib-source`. (Hint: look in the SPARQL evaluation module for an injected `Exception` or `NotImplementedError`). Ensure that `/app/rdflib-source` is added to your `PYTHONPATH` when running scripts.
2. **Build the Backup Analyzer**: Write a Python script at `/home/user/backup_analyzer.py` that takes two command-line arguments:
   `python3 /home/user/backup_analyzer.py <path_to_ttl_file> <target_backup_uri>`
3. **Graph Analytics & Windowing**: Your script must load the provided `.ttl` file using the fixed `rdflib`.
   - Use a **parameterized SPARQL query** to find the given `<target_backup_uri>` and all of its ancestor backups. (An incremental backup `ns:dependsOn` its parent backup, forming a chain back to a root full backup).
   - For each backup in this restoration path, retrieve its `ns:backupSize` (integer) and `ns:creationTime` (integer timestamp).
   - In Python, process this result set to calculate the running total of the backup sizes, ordered by `creationTime` ascending (simulating a window function).
   - Calculate the total number of backups in the chain and the final total size (the max of the running sum).
4. **Output Format**: Print exactly one line to standard output:
   `Restoration chain for [TARGET]: Length=[N], TotalSize=[SUM]`
   (Replace `[TARGET]` with the provided URI string, `[N]` with the count of backups in the chain, and `[SUM]` with the final accumulated size).

The automated verifier will test your script against thousands of random backup URIs from dynamically generated backup graphs to ensure it perfectly matches the output of our internal oracle program.