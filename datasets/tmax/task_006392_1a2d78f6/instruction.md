You are a database administrator planning a complex schema migration. We need to modify the `users` table, but we first need to identify every downstream table that might be affected due to foreign key relationships.

I have provided a JSON representation of our relational database schema at `/home/user/schema.json`. This file contains a cross-representation mapping of the database, detailing table names and their foreign key constraints.

Your task is to:
1. Write a Python script at `/home/user/find_deps.py` that parses `/home/user/schema.json`.
2. The script must perform a recursive hierarchical search (simulating a recursive CTE) to find all tables that depend on the `users` table, either directly (having a foreign key referencing `users`) or indirectly (having a foreign key referencing a table that depends on `users`, etc.).
3. The script must output the names of all affected dependent tables to a file located at `/home/user/users_dependencies.txt`. 
4. The output file must contain exactly one table name per line, sorted in alphabetical order. Do not include the original `users` table in the output.

Ensure your Python script runs successfully and generates the correct output file.