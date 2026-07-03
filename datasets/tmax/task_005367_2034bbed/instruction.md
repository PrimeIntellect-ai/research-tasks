You are a data analyst investigating database deadlocks. You have been provided with a CSV file at `/home/user/wait_for.csv` representing transaction wait-for relationships. The file has a header row `tx_waiting,tx_holding`, followed by rows of integer transaction IDs, where `tx_waiting` is blocked by `tx_holding`.

Your task is to:
1. Write a C program at `/home/user/detect.c` that reads `/home/user/wait_for.csv`.
2. The C program must generate a SQLite-compatible SQL script at `/home/user/query.sql`.
3. The generated SQL script (`query.sql`) must perform the following:
   - Create a table named `wait_for` with columns `tx_waiting INTEGER` and `tx_holding INTEGER`.
   - Insert all the data rows from the CSV into the `wait_for` table (the C program should generate the `INSERT` statements based on the CSV).
   - Use a recursive Common Table Expression (CTE) to traverse the wait-for graph and find all transactions that are part of a deadlock. A deadlock is defined as a cycle in the wait-for graph with a path length of up to 5 edges (i.e., a transaction ultimately waiting on itself).
   - Execute a `SELECT` statement that outputs ONLY the distinct transaction IDs that are part of a deadlock (i.e., the starting nodes of the detected cycles), sorted in ascending numerical order.
4. Compile your C program: `gcc -o /home/user/detect /home/user/detect.c`
5. Run your C program to generate the SQL script: `/home/user/detect`
6. Execute the generated SQL script against a new SQLite database and save the output: `sqlite3 /home/user/test.db < /home/user/query.sql > /home/user/deadlocks.txt`

The final output file `/home/user/deadlocks.txt` should contain exactly one transaction ID per line for all transactions involved in deadlocks.