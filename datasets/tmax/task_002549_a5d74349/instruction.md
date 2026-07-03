You are assisting a compliance officer who is auditing a financial database for money laundering. 

We have an SQLite database at `/home/user/financial_graph.db` containing two tables:
1. `entities` (`id` INTEGER PRIMARY KEY, `name` TEXT)
2. `transactions` (`tx_id` INTEGER PRIMARY KEY, `sender_id` INTEGER, `receiver_id` INTEGER, `amount` REAL, `timestamp` TEXT)

There is a Python script at `/home/user/audit_transactions.py` designed to find "circular" transaction patterns of length 3 (Entity A sends to Entity B, B sends to C, and C sends back to A), where every transaction in the chain has an amount strictly greater than a parameterized threshold (e.g., 10,000). 

Currently, the script is broken. It runs indefinitely and returns completely wrong results because the SQL query contains an implicit cross join. Furthermore, the database lacks the necessary indexes to efficiently query this graph-like relationship.

Your task is to:
1. Fix the SQL query in `/home/user/audit_transactions.py` so it correctly identifies the `sender_id` of the first transaction (Entity A) in these circular chains. Ensure the query uses parameterized inputs for the amount thresholds to prevent SQL injection and properly traverses the graph structure.
2. The query must return distinct `sender_id`s.
3. Optimize the database by executing SQL commands to create at least two indexes on the `transactions` table that will speed up this specific graph traversal (indexing the sender and receiver columns).
4. Run the fixed script with a threshold of `10000`. Have the script save the resulting `sender_id`s to `/home/user/flagged_entities.csv`, with one integer ID per line, sorted in ascending order.

Do not change the name of the script. Focus on fixing the query logic, adding indexes, and producing the output file.