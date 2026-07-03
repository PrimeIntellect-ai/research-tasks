You are a database administrator tasked with optimizing a graph-processing query for our server network. We store our server hierarchy and configurations in an SQLite database, utilizing its JSON extension to simulate NoSQL document storage for flexible hardware configurations.

Database location: `/home/user/network.db`
Table schema:
- `nodes`
  - `id` (INTEGER PRIMARY KEY)
  - `parent_id` (INTEGER, Foreign Key to `nodes.id` representing the graph hierarchy)
  - `config` (TEXT, storing a JSON document like `{"cpu": 8, "ram": 32}`)

Your objective is to write a C program that connects to this SQLite database and executes a single query to calculate the aggregate resource usage of a specific server cluster.

Requirements:
1. Write a C program at `/home/user/query.c`.
2. The C program must execute a query using a Recursive Common Table Expression (CTE) to find node `id=1` and all of its descendants (children, grandchildren, etc.) in the graph.
3. Using SQLite's JSON extraction functions (NoSQL-like aggregation), sum the total `cpu` and `ram` values embedded within the `config` JSON documents of all nodes in this specific subtree.
4. The C program must write the aggregated result to `/home/user/output.txt` in exactly this format:
   `CPU: <total_cpu>, RAM: <total_ram>`
   (Replace `<total_cpu>` and `<total_ram>` with the computed integer totals).
5. Compile and run the C program to produce the output file. 

You may need to install the SQLite C development libraries to compile your code. You can use `sudo apt-get update && sudo apt-get install -y libsqlite3-dev` if necessary. Compile your C code with `-lsqlite3`.