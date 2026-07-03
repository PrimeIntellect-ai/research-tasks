You are assisting a bioinformatics researcher in organizing a massive hierarchical dataset of biological taxonomy. 

The dataset is stored in an SQLite database at `/home/user/taxonomy.db`. 
The database contains a single table:
`taxa (id INTEGER PRIMARY KEY, name TEXT, parent_id INTEGER)`

Unfortunately, there is a known issue: the database contains a corrupted index named `idx_parent_stale`. This index was generated improperly during a bulk import. If a query uses this index, SQLite returns stale or missing rows. 

The researcher has been using a local, heavily customized Python package to interface with this database. The package is vendored at `/app/sqlite-graph-builder-0.4.5`. 
However, the package's core recursive query builder is currently broken because it explicitly forces the use of the corrupted index via an `INDEXED BY idx_parent_stale` directive in its SQL templates.

Your tasks are:
1. **Fix the vendored package**: Locate the SQL query template in the `/app/sqlite-graph-builder-0.4.5` package source and remove the `INDEXED BY idx_parent_stale` directive so it relies on SQLite's default query planner. Make sure to reinstall or link the package if necessary.
2. **Write the graph materialization script**: Create a script at `/home/user/fetch_subtree.py` that takes a single integer argument (a `node_id`). 
3. The script must use the fixed `sqlite-graph-builder` package (or raw `sqlite3` using recursive CTEs) to project the entire hierarchical subtree rooted at `node_id`.
4. **Format the output**: The script must output the materialized subtree to `stdout` as a strict, recursively nested JSON object with the following schema:
   ```json
   {
     "id": 1,
     "name": "Animalia",
     "children": [
       {
         "id": 2,
         "name": "Chordata",
         "children": []
       }
     ]
   }
   ```
   **Important Constraints**: 
   - Every node must have an `id` (integer), `name` (string), and `children` (array).
   - If a node has no children, `children` must be an empty array `[]`.
   - The `children` array must be **sorted in ascending order by `id`** at every level of the hierarchy.
   - The output must be perfectly valid JSON (no extra logging or text on standard output).

An automated testing suite will run your script multiple times with random node IDs and compare the bit-exact JSON output against a known truth oracle.