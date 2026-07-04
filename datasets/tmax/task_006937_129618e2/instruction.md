You are a data analyst investigating a series of suspicious financial transactions. You have been given two CSV files representing a transaction network (a directed graph where users are nodes and transactions are edges). 

The files are located at:
1. `/home/user/users.csv` (columns: `id,name`)
2. `/home/user/transactions.csv` (columns: `tx_id,sender_id,receiver_id,amount`)

Your task is to write a single Bash script at `/home/user/detect_cycles.sh` that completely automates the following workflow:

1. **Database Initialization**: Programmatically create a new SQLite database at `/home/user/graph.db` and import the two CSV files into tables named `users` and `transactions`.
2. **Graph Query**: Use `sqlite3` to execute a graph-like query (using Common Table Expressions/joins) to find all "Length-3 Cycles". A Length-3 Cycle is defined as a sequence of exactly 3 distinct users (A, B, C) where:
    - User A sends money to User B
    - User B sends money to User C
    - User C sends money to User A
    - **Condition**: Every transaction in this specific cycle must have an `amount` >= 500.
3. **Cross-query Aggregation**: Your Bash script must pipeline the output of the SQL query into standard Unix text processing tools (like `awk`, `sort`, etc.) or handle it within SQL, to calculate the **total sum of outgoing transaction amounts** for each user, but *only* counting the transactions that strictly participated in the identified valid Length-3 cycles. 
4. **Formatting**: The final output should be written to `/home/user/cycle_summary.csv` with the headers `name,total_outgoing_cycle_amount`. The rows must be sorted alphabetically by the user's `name`. 

Make sure the script is executable (`chmod +x`). 
When we test your solution, we will simply run `/home/user/detect_cycles.sh` and then inspect the contents of `/home/user/cycle_summary.csv`. Do not assume any pre-existing database exists. Clean up or overwrite `/home/user/graph.db` if your script is run multiple times.