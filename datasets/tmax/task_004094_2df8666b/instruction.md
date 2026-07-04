You are a database administrator tasked with cleaning up a relational database that stores a Knowledge Graph. Due to a recent bulk update where foreign key constraints were temporarily disabled, the database now contains "stale" rows—specifically, edge relationships pointing to nodes that no longer exist.

The database is located at `/home/user/graph.db`. It contains two tables:
- `nodes` with columns: `id` (TEXT), `label` (TEXT), `properties` (TEXT)
- `edges` with columns: `source` (TEXT), `target` (TEXT), `rel_type` (TEXT)

Your objective is to use Python (with the built-in `sqlite3` module) to analyze the schema, identify the stale graph relationships, and clean the database. 

Please perform the following steps:
1. Identify all "stale" edges. A stale edge is any row in the `edges` table where either the `source` or the `target` `id` does not exist in the `nodes` table.
2. We are particularly interested in finding people who have been orphaned by the deletion of their company. Find all nodes with the label `'Person'` that are the `source` of a `'WORKS_FOR'` edge where the `target` node is missing from the `nodes` table.
3. Extract the `id`s of these orphaned Person nodes. Sort them in **descending alphabetical order**, and paginate the results to return only the **first 5** IDs.
4. Save these 5 IDs to a text file at `/home/user/stale_persons.txt`, with one ID per line.
5. Finally, clean the database by deleting *all* stale edges (not just the 'WORKS_FOR' ones) from the `edges` table.

Do not use external libraries like `pandas` or `sqlalchemy`—rely entirely on the standard Python `sqlite3` library. Run your script to ensure the outputs are generated and the database is cleaned.