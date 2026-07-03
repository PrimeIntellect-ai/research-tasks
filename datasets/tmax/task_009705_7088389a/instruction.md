You are a data analyst working for a logistics company. You have been given two CSV files representing the logistics network: `/home/user/nodes.csv` (representing cities) and `/home/user/edges.csv` (representing routes between cities). 

Due to a recent storm, some cities are marked as 'INACTIVE' in the network. You need to perform graph processing using Bash and SQLite3 (which is pre-installed) to analyze the impact and find new optimal routes.

Your task is to write a Bash script named `/home/user/process_graph.sh` that automates the following steps:

1. **Graph Materialization & Projection**:
   - Create a SQLite database at `/home/user/graph.db`.
   - Import `nodes.csv` and `edges.csv` into tables named `nodes` and `edges`.
   - Create a materialized table (or view) named `active_edges`. An edge is only active if BOTH its source and target nodes have the status 'ACTIVE'.

2. **Cross-Query Aggregation**:
   - Calculate the total network capacity by summing the `capacity` column for all `active_edges`.

3. **Graph Traversal (Shortest Path)**:
   - Using a recursive CTE in SQLite, find the lowest-cost path from the node named 'Alpha' to the node named 'Foxtrot' using ONLY `active_edges`.

4. **Output Generation**:
   - Write the results to a file named `/home/user/summary.csv`.
   - The output must have exactly this format:
     ```csv
     metric_name,value
     total_active_capacity,<your_calculated_capacity>
     shortest_path_cost,<your_calculated_cost>
     ```

5. **Output Schema Validation**:
   - Write a second Bash script named `/home/user/validate.sh`.
   - This script should read `/home/user/summary.csv` and validate that:
     a) The first line is exactly `metric_name,value`
     b) It contains exactly 3 lines.
     c) The values for `total_active_capacity` and `shortest_path_cost` are positive integers.
   - If valid, the script should print "VALID" to standard output and exit with code 0. Otherwise, print "INVALID" and exit with code 1.

Ensure `/home/user/process_graph.sh` runs autonomously without user input and creates all required files. You can use standard command-line tools (bash, awk, sed, sqlite3).