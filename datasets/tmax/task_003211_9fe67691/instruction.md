You are a Database Reliability Engineer (DBRE) tasked with managing a legacy backup system. We have lost the source code that interprets the metadata for our incremental backup chains. The metadata is currently exported as a raw NoSQL JSON Lines (JSONL) dump, but the field names are obfuscated.

Fortunately, we recovered an old architectural diagram that maps these obfuscated NoSQL fields to their canonical relational data model. This diagram is available as an image at `/app/schema_clue.png`. 

Your task is to reverse-engineer the data model using the image, and build a Python-based query and result processing tool that can project this metadata into a backup dependency graph and calculate critical restoration metrics.

Write a Python script at `/home/user/restore_planner.py` that takes exactly one argument (the path to a JSONL file containing the raw NoSQL dump) and prints a processed JSONL output to standard output. 

The script must perform the following:
1. **Data Model Reverse Engineering**: Parse the obfuscated JSONL using the mapping found in `/app/schema_clue.png`.
2. **Graph Materialization**: Treat the backups as a directed tree where each node represents a backup, and edges represent the parent-child dependency (incremental backups depend on a parent).
3. **Analytical Aggregation (Total Restore Size)**: For each backup node, calculate the `total_restore_size`. This is the sum of its own size AND the sizes of all its ancestors back to the root backup.
4. **Window Function Analysis (Sibling Rank)**: For each backup node, calculate its `sibling_rank`. Partition the nodes by their parent ID. Order the nodes within each partition by their timestamp in **descending** order (newest first). Assign a rank starting at 1. Root nodes (no parent) are in a single partition where parent is null/None.
5. **Output**: Print to stdout a JSONL stream where each line represents a node, containing exactly these keys: `{"node_id": "<str>", "total_restore_size": <int>, "sibling_rank": <int>}`. The output lines MUST be sorted alphabetically by `node_id`.

Example input line (obfuscated keys are placeholders, see image for actual keys):
`{"K1": "nodeA", "K2": null, "K3": 1000, "K4": 1600000000}`

Your script should be executable via `python3 /home/user/restore_planner.py <input_file.jsonl>`. Use standard Python libraries.