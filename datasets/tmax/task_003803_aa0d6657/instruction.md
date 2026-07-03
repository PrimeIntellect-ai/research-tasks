You are a data analyst tasked with processing a network graph stored in an SQLite database. 

You have been provided with an SQLite database at `/home/user/network.db` containing two tables:
1. `nodes`: Contains node information.
   - `id` (TEXT)
   - `department` (TEXT)
2. `edges`: Contains directed edge information representing communication between nodes.
   - `src` (TEXT)
   - `dst` (TEXT)
   - `timestamp` (INTEGER)

**The Problem:**
Due to a faulty logging system, the `edges` table contains "stale" duplicate rows. There are multiple records for the same `(src, dst)` pair. 

Your task is to write a Go program at `/home/user/analyze.go` that connects to this SQLite database and performs the following analytical workflow:
1. **Deduplicate Edges:** For any given `(src, dst)` pair, only the edge with the highest `timestamp` is considered valid. Ignore all older edges for that pair.
2. **Calculate Total Degree:** Compute the "total degree" for each node based on the deduplicated edges. The total degree is the sum of a node's in-degree (times it appears as `dst`) and out-degree (times it appears as `src`).
3. **Rank Nodes:** For each `department`, rank the nodes based on their total degree in descending order. Use dense ranking (e.g., 1, 2, 2, 3). If there is a tie in total degree, break the tie by ordering the node `id` in ascending alphabetical order.
4. **Extract Top Nodes:** Filter the results to include only the top 3 ranked nodes for each department.

Your Go program must output the final results to a CSV file at `/home/user/top_nodes.csv`.
The CSV file must have exactly this header: `department,node_id,total_degree,rank`
The rows must be sorted alphabetically by `department` (ascending), and then by `rank` (ascending), and finally by `node_id` (ascending).

Requirements:
- You must use Go to execute the queries and generate the CSV.
- The `github.com/mattn/go-sqlite3` driver is recommended.
- You may use complex SQL queries (CTEs, Window Functions, etc.) to do the heavy lifting in SQLite before exporting the results.
- Do not modify the original `/home/user/network.db` database. Read from it only.