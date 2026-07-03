You are a data analyst working with a hierarchical dataset of company assets represented as a graph. You are provided with a SQLite database `/home/user/graph.db` that contains two tables: `nodes` (id TEXT PRIMARY KEY, weight INTEGER) and `edges` (source TEXT, target TEXT).

Currently, there is a Python script `/home/user/concurrent_update.py` that attempts to concurrently update the weights of several nodes. However, it often fails with a SQLite deadlock (`database is locked`) because different threads attempt to update the same sets of nodes in different orders, causing a classic circular wait deadlock. Additionally, the script uses unsafe string concatenation instead of parameterized queries.

Your task consists of two parts:

1. **Fix the Deadlock and Query Construction:**
   Modify `/home/user/concurrent_update.py` so that:
   - It uses proper parameterized queries (e.g., `?` placeholders) instead of f-strings for the SQL `UPDATE` statement.
   - It prevents the deadlock by sorting the list of node IDs lexicographically before acquiring locks/executing the updates within each transaction. This ensures all threads acquire row locks in a consistent order.
   - Run the script to successfully update the database.

2. **Recursive Graph Query:**
   After the database is successfully updated, write a SQL script at `/home/user/analyze.sql` that uses a Recursive Common Table Expression (CTE) to find the node 'ROOT' and all of its transitive dependencies (children, grandchildren, etc.) following the `edges` table (`source` to `target`).
   - The query must calculate the sum of the `weight` of the 'ROOT' node and all its transitive dependencies.
   - Execute this query and save the single integer result to `/home/user/root_total_weight.txt`.

Ensure your final output file strictly contains the integer sum and nothing else.