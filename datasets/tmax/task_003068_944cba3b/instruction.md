You are a data engineer working on optimizing data replication routes across a global network of data centers. You have been provided with network latency data and need to build an ETL pipeline in Bash that loads this data into a database and computes the shortest latency paths between specific data centers.

Assume `sqlite3` is already installed on the system. All your work should be done in the `/home/user/` directory.

You need to build a modular pipeline consisting of three Bash scripts:

**1. Database Initialization Script (`/home/user/init_db.sh`)**
Write a script that:
- Creates an SQLite database named `/home/user/network.db`.
- Creates a table named `edges` with columns `source` (TEXT), `target` (TEXT), and `latency` (INTEGER).
- Imports the raw CSV data located at `/home/user/network_edges.csv` into the `edges` table. 
- (Note: The CSV has a header row: `source,target,latency`).

**2. Path Computation Script (`/home/user/find_shortest_path.sh`)**
Write a Bash script that takes two arguments: a `start_node` and an `end_node` (in that order).
- The script must dynamically construct an SQLite query using a Recursive Common Table Expression (CTE) to traverse the graph and find the path with the minimum total latency from the `start_node` to the `end_node`.
- The graph is directed (paths go from `source` to `target`).
- Your script must execute the query against `/home/user/network.db`.
- The output to `stdout` should be strictly in this format: `TOTAL_LATENCY|PATH`
- Example output: `35|DC1-DC2-DC5`

**3. Master ETL Pipeline (`/home/user/pipeline.sh`)**
Write a Bash script that chains the workflow together:
- First, it should execute `init_db.sh`.
- Next, it should read a provided file `/home/user/routes_to_calc.csv` (which contains pairs of data centers in the format `start_node,end_node` without a header).
- For each pair in the file, it should call `find_shortest_path.sh`, capture the result, and append a line to `/home/user/optimized_routes.log` in the format:
  `START_NODE,END_NODE,TOTAL_LATENCY,PATH`
- Example line in log: `DC1,DC5,35,DC1-DC2-DC5`

Ensure all three scripts are executable (`chmod +x`). Once you have written all scripts, run `/home/user/pipeline.sh` so the final `/home/user/optimized_routes.log` file is generated.