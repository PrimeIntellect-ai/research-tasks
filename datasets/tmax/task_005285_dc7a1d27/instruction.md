You are acting as a data analyst processing transaction records to uncover hidden relationships between customers. You have a file `/home/user/transactions.csv` containing a bipartite graph of users and the products they have purchased. 

The CSV has a header and the following columns: `user_id,product_id,timestamp`.

Your task is to write a Bash script `/home/user/analyze_graph.sh` that orchestrates a local SQLite database to project this bipartite graph into a materialized unipartite user-to-user graph, and allows querying the results.

The script must accept two arguments for pagination: `page_number` (1-indexed) and `page_size`. 
Example usage: `./analyze_graph.sh 2 10`

The script must perform the following actions:
1. Check if the database `/home/user/graph.db` exists. If it does not exist, initialize it by importing the `transactions.csv` file into a table named `transactions`.
2. Design and create appropriate indexes on the `transactions` table to optimize the upcoming self-join (graph projection). 
3. Project and materialize a new graph (as a table named `user_graph`) representing co-purchases. An edge exists between `user1` and `user2` if they purchased the same `product_id`. 
   - The materialized table should have columns: `user1, user2, weight`.
   - `weight` is the number of distinct `product_id`s they both purchased.
   - To avoid duplicate undirected edges, ensure `user1 < user2`.
   - Filter the materialized edges to only include pairs with a `weight >= 2`.
4. Query the `user_graph` table to retrieve the requested page of results. 
   - The results must be sorted by `weight` DESCENDING, then by `user1` ASCENDING, then by `user2` ASCENDING.
   - Use the `page_number` and `page_size` arguments to apply the correct `LIMIT` and `OFFSET`.
   - Print the resulting rows to standard output as comma-separated values (no header, just `user1,user2,weight`).

Requirements:
- Ensure your Bash script has executable permissions (`chmod +x`).
- Use `sqlite3` via Bash to execute the SQL operations. 
- You must create indexes before doing the projection to ensure optimal performance.
- The projection must be materialized (saved as a table) so subsequent calls to the script do not recompute the graph. Only create the `user_graph` table if it doesn't already exist.

Note: `sqlite3` is already available on the system.