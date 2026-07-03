You are a Database Administrator dealing with an old, inefficient legacy system. We have a relational database that stores the schema metadata of our entire data warehouse. This metadata is stored in a SQLite database located at `/home/user/data_catalog.db`.

The database has the following schema:
- `tables` (table_id INTEGER PRIMARY KEY, table_name TEXT)
- `foreign_keys` (fk_id INTEGER PRIMARY KEY, from_table_id INTEGER, to_table_id INTEGER)

We currently use a proprietary, compiled query optimization engine to calculate "join costs" between arbitrary tables. This engine is located at `/app/legacy_join_cost_engine`. It takes two arguments (Source Table ID and Destination Table ID) and outputs a single integer representing the cost. 
Usage: `/app/legacy_join_cost_engine <src_table_id> <dst_table_id>`

The legacy engine is stripped, unmaintained, and highly inefficient for bulk operations. Your task is to write a highly optimized Python replacement that behaves exactly like the legacy engine.

Requirements:
1. Write a Python script at `/home/user/optimized_cost_engine.py`.
2. The script must take exactly two command-line arguments: `<src_table_id>` and `<dst_table_id>`.
3. It must connect to `/home/user/data_catalog.db`, parse the relationships, and map the relational schema into a graph structure.
4. It must compute the exact same integer join cost as the legacy engine for any given pair of valid table IDs. If no path exists, it must output what the legacy engine outputs for disconnected tables.
5. You can use any reverse-engineering tools (`objdump`, `strings`, `strace`, or treating it as a black box) to figure out the mathematical model the legacy binary uses to calculate the join cost. (Hint: It involves graph traversal and node centrality/degree properties).
6. Print only the final integer to standard output, exactly matching the legacy binary's format.

Do not modify the SQLite database or the legacy binary.