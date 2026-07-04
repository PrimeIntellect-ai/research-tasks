You are a data analyst working with an organizational graph. You've been provided with a raw data dump and a vendored C application that is supposed to serve hierarchy queries over the network.

Your objectives:

1. **Data Reverse Engineering & Projection**
   You have a raw CSV file at `/home/user/data.csv` without headers. It contains employee records. One column is the unique employee ID, and another column is the manager's employee ID. 
   Analyze the data to determine which columns represent the `employee_id` and `manager_id` (the manager ID column will exclusively contain values that exist in the employee ID column, except for the top-level executive who has a value of `0`).
   Write a script to project this data into a new file at `/home/user/hierarchy.csv` containing only `manager_id,employee_id` for every valid edge (exclude the top-level executive's `0` manager).

2. **Fix the Vendored Application**
   In `/app/org-server/`, there is a vendored C package designed to read `hierarchy.csv` on startup and serve recursive graph queries. However, it has bit-rotted:
   - The `Makefile` has an error preventing it from compiling.
   - The graph traversal logic in `graph.c` has a bug: it currently only returns direct subordinates instead of the full hierarchical tree of descendants.

3. **Deploy the Service**
   Fix the C code so that it correctly computes all transitive subordinates. Compile the server and start it. It must:
   - Read `/home/user/hierarchy.csv`.
   - Listen on TCP port `8888`.
   - Implement the custom protocol: when it receives a string like `REPORTS 15\n`, it must return a comma-separated list of all descendant employee IDs (e.g., `23,45,99\n`).

Leave the server running in the background listening on `127.0.0.1:8888` when you are finished.