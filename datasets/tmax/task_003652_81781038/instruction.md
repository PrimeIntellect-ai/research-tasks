You are a database administrator tasked with optimizing a hierarchical query and implementing a data retrieval tool in C.

A company stores its organizational structure in an SQLite database located at `/home/user/company.db`. The database contains a single table:
`employees (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER)`

Your task consists of three parts:

1. **Database Optimization**: Analyze the `employees` table and create the appropriate index on the `manager_id` column in `/home/user/company.db` to optimize hierarchical graph traversals (finding direct reports).

2. **C Program Implementation**: Write a C program at `/home/user/hierarchy.c` that connects to the SQLite database. The program must:
   - Accept three command-line arguments (in order): `manager_id`, `limit`, and `offset`.
   - Use a parameterized recursive Common Table Expression (CTE) to traverse the management graph and find all descendants of the given `manager_id` (including the manager themselves at depth 0).
   - Sort the results first by `depth` (ascending), then by `name` (ascending).
   - Apply the provided `limit` and `offset` for pagination.
   - Perform cross-representation mapping by writing the paginated relational results as a JSON array of objects to `/home/user/output.json`.

3. **Execution**: 
   - Compile your program: `gcc /home/user/hierarchy.c -lsqlite3 -o /home/user/hierarchy`
   - Run your program to find the descendants of employee ID `1`, with a limit of `4` and an offset of `2`:
     `/home/user/hierarchy 1 4 2`

**Output Format Requirement:**
The file `/home/user/output.json` must contain a valid JSON array of objects, exactly matching this structure (whitespace is flexible as long as it is valid JSON):
```json
[
  {"id": 3, "name": "Charlie", "depth": 1},
  {"id": 4, "name": "David", "depth": 2},
  {"id": 5, "name": "Eve", "depth": 2},
  {"id": 6, "name": "Frank", "depth": 2}
]
```

Ensure you handle the SQLite API correctly (`sqlite3_prepare_v2`, `sqlite3_bind_int`, `sqlite3_step`, etc.). Do not forget to install any necessary development packages for SQLite if they are missing (e.g., `libsqlite3-dev`).