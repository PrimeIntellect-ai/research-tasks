You are acting as a Database Administrator and Python Developer. We use a proprietary in-memory graph querying engine called `sql-graph-emulator` to perform recursive hierarchical queries and cross-query aggregations on our tree-like JSON datasets. 

Recently, our aggregations have been returning astronomically incorrect results. We suspect that there is a bug in the engine causing an implicit cross join (Cartesian product) during the execution of hierarchical relationships, which leads to massive duplication of nodes during recursive traversal.

Your task consists of two parts:

**Part 1: Fix the Vendored Package**
1. The source code for `sql-graph-emulator` version `1.2.0` is vendored at `/app/sql-graph-emulator`.
2. Inspect the engine's source code, specifically looking for where node relationships (parent-child joins) are evaluated. Find the bug causing the implicit cross join and fix it. 
3. Ensure the package is properly installed or accessible to your Python environment.

**Part 2: Create the Query Script**
1. Write a Python script at `/home/user/solve.py`.
2. The script must accept a single command-line argument: the path to a JSON dataset.
   The JSON format is:
   `{"nodes": [{"id": 1, "value": 10}, {"id": 2, "value": 20}], "edges": [{"parent": 1, "child": 2}]}`
3. Using the fixed `sql-graph-emulator` package, the script must parse the JSON, and for *every* node in the graph, calculate the total recursive sum of its value plus the values of all its transitive descendants.
4. Export the summarization to standard output (stdout) in standard CSV format with a header, strictly formatted as:
   ```csv
   id,total_value
   1,30
   2,20
   ```
5. The CSV rows must be sorted by `id` in ascending numerical order.

Requirements:
- Your solution must be bit-exact reproducible. An automated testing system will run your script against multiple random, deeply nested graph JSON files and compare your script's stdout against a reference implementation.
- Only output the final CSV data to stdout. Do not print debug logs to stdout (use stderr if you must).