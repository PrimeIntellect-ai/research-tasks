You are a data analyst working with transaction network data. You have been provided with two CSV files representing a directed graph of financial transactions.

Your objective is to write a comprehensive Bash script `/home/user/process_graph.sh` that uses `sqlite3` to process this data, find specific transaction patterns, and output the results and query optimization details.

**Data provided (Assume these already exist):**
1. `/home/user/nodes.csv` (Header: `id,name,type`)
2. `/home/user/edges.csv` (Header: `source,target,amount,timestamp`)

**Task Requirements:**
Your script `/home/user/process_graph.sh` must perform the following actions when executed:

1. **Database Setup:**
   - Create a new SQLite database at `/home/user/graph.db`.
   - Create tables `nodes` and `edges` matching the CSV schemas.
   - Import the CSV data into these tables (skip the header rows).

2. **Index Strategy:**
   - Create indexes on the `edges` table to optimize joining on source, target, and filtering by timestamp and amount.

3. **Graph Pattern Matching & Analytical Query:**
   - Write a single SQL query that finds "escalating 2-hop paths".
   - A 2-hop path consists of two edges: Edge 1 (A → B) and Edge 2 (B → C).
   - **Conditions:** 
     - `Edge1.target = Edge2.source`
     - `Edge1.timestamp < Edge2.timestamp` (chronological order)
     - `Edge1.amount < Edge2.amount` (escalating amount)
   - Using a **window function**, calculate the `total_amount` (`Edge1.amount + Edge2.amount`) and find the *single top path* (highest `total_amount`) for *each* starting node A. If there's a tie, order by node C's ID ascending.
   - The query should resolve the node IDs to their `name`s.
   
4. **Outputs:**
   - The script must execute the query and save the results to `/home/user/top_paths.csv` with the format `StartName,MiddleName,EndName,TotalAmount`. Do not include a header in the output file. Fields should be comma-separated.
   - The script must also run `EXPLAIN QUERY PLAN` on the exact same query and save the output to `/home/user/query_plan.txt`.

Make sure your script is executable (`chmod +x /home/user/process_graph.sh`) and runs successfully without user interaction.