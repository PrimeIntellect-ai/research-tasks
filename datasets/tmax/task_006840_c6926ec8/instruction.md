You are assisting a compliance officer in auditing a financial transaction network to detect potential money laundering techniques. 

The data is stored in an SQLite database at `/home/user/compliance.db`. 
There are two tables:
1. `entities` (id, name, domain) - Represents accounts. Domains can be 'Internal' or 'External'.
2. `transactions` (tx_id, source_id, target_id, amount, tx_date) - Represents directed money transfers between entities.

The compliance team uses a Python script located at `/home/user/audit.py` to find suspicious "Domain Hop" transaction paths. A "Domain Hop" is defined as a sequence of exactly two transactions (A -> B and B -> C) where:
1. Entity A and Entity C belong to the SAME domain.
2. Entity B belongs to a DIFFERENT domain than A and C.
3. The amount transferred from B to C is STRICTLY GREATER THAN the average outgoing transaction amount of Entity B (calculated across all of Entity B's outgoing transactions in the database).

Currently, `/home/user/audit.py` is producing wildly incorrect results and running very slowly. The previous developer made a mistake in the SQL query, resulting in an implicit cross join that pairs unrelated transactions and entities.

Your task is to:
1. Analyze the database schema and the buggy query in `/home/user/audit.py`.
2. Fix the SQL query in `/home/user/audit.py` so that it correctly identifies the "Domain Hop" paths. You MUST use a window function (e.g., `AVG() OVER (...)`) in a CTE or subquery to calculate the average outgoing transaction amounts for the entities efficiently.
3. The script must execute the query and output the results to `/home/user/flagged_paths.csv`.

The output CSV must have exactly these columns, including the header:
`A_name,B_name,C_name,t1_amount,t2_amount`

Sort the final results in the CSV by `t2_amount` in descending order. If there is a tie, sort by `A_name` in ascending alphabetical order.

You may rewrite the Python script entirely if you wish, as long as it queries `/home/user/compliance.db` and produces the correct `/home/user/flagged_paths.csv`.