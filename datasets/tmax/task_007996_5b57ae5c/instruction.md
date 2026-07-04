You are acting as a Database Administrator and Systems Programmer. You need to analyze corporate communication data to build a department-level dependency graph using C and SQLite3.

There is an SQLite database located at `/home/user/corp.db` with the following schema:
- `employees` (emp_id INTEGER PRIMARY KEY, name TEXT, department TEXT)
- `communications` (sender_id INTEGER, receiver_id INTEGER, message_count INTEGER)

Your objective is to write a C program that connects to this database, performs an analytical query to project a graph of department interactions, and outputs the results.

Requirements for the SQL Query (executed within your C program):
1. Aggregate the total `message_count` between departments (sender's department to receiver's department). Ignore intra-department communications (where sender and receiver are in the same department).
2. For each sender department, find the single receiver department they communicate with the *most* (highest total message count).
3. You MUST use a window function (e.g., `RANK()`, `DENSE_RANK()`, or `ROW_NUMBER()`) to determine this top connection per department.
4. Order the final results alphabetically by the sender department.

Requirements for the C Program:
1. Write the program in `/home/user/graph_projector.c`.
2. Use the SQLite3 C API (`sqlite3.h`).
3. Compile the program to an executable named `/home/user/graph_projector`. (You may need to install `libsqlite3-dev` and link appropriately).
4. When executed, the program must write the result of the query to a file at `/home/user/top_connections.csv`.
5. The CSV file must have the following format (no headers):
   `sender_department,receiver_department,total_messages`

Example of expected output in the CSV:
```
Engineering,Marketing,450
HR,Engineering,120
Marketing,Sales,890
```

Ensure the output file exactly matches this format and is written successfully when `/home/user/graph_projector` is executed.