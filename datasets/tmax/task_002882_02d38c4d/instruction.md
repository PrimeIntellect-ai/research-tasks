You are a data analyst preparing a transaction log for a graph database. You need to process a dataset using C++ and SQLite, optimize the query, and generate a Cypher script.

The dataset is located at `/home/user/transactions.csv`. It has the following columns:
`tx_id,sender,receiver,amount,timestamp`

Your objective is to write a C++ program at `/home/user/graph_builder.cpp` that performs the following steps:
1. Creates an in-memory SQLite database and a table named `transactions` with the appropriate schema.
2. Reads the `/home/user/transactions.csv` file and inserts all rows into the `transactions` table.
3. Creates a specific index on the `transactions` table to optimize the analytical window query (Step 4) so that it avoids an explicit sort step (the query plan should show it uses the index for the `ORDER BY` in the window function).
4. Executes the following analytical window query:
   Calculate the `running_total` of the `amount` sent by each `sender`, ordered by `timestamp`, as well as the `tx_rank` (using `ROW_NUMBER()`) of that transaction for that sender.
5. Captures the `EXPLAIN QUERY PLAN` output for this exact window query and saves it to `/home/user/query_plan.txt`.
6. Executes the actual query and iterates through the results to generate a Cypher script at `/home/user/import.cypher`.

For each row returned by the query, write a Cypher command to the output file in this exact format:
`MERGE (s:User {id: '<sender>'}) MERGE (r:User {id: '<receiver>'}) CREATE (s)-[:TRANSFERRED {tx_id: <tx_id>, amount: <amount>, running_total: <running_total>, rank: <tx_rank>}]->(r);`

Requirements:
- Install any necessary C++ SQLite development libraries to compile your program.
- Compile your program to `/home/user/graph_builder` using `g++` and execute it.
- Do not use third-party libraries other than the standard library and `sqlite3`.