You are helping a researcher organize and query a knowledge graph dataset. 

The dataset is stored in an SQLite database at `/home/user/dataset.db`. The researcher has lost the exact schema documentation, but they know it contains nodes and directed edges representing relationships between different research concepts.

Your task is to write a C program that connects to this database, reverse-engineers the schema to find the right tables/columns, and performs the following graph analytics queries:

1. Identify the node ID with the highest in-degree (the node with the most incoming edges). If there is a tie, select the one with the smallest node ID.
2. Find all node IDs that have a directed path of length exactly two to this highly-connected node (i.e., nodes `A` where a path `A -> B -> HighlyConnectedNode` exists). 

Write your C code to `/home/user/query.c`. Your program should use the `sqlite3` C library.
When executed, your program must create a file named `/home/user/result.txt` with the following format:
- The first line must contain the ID of the node with the highest in-degree.
- The subsequent lines must contain the IDs of the nodes that have a path of length exactly 2 to that node, sorted in ascending order, one ID per line.

Requirements:
- You must use C to perform the database querying. 
- You can use shell commands to explore the database schema first if you wish (e.g., using the `sqlite3` CLI), but the final query and output generation must be done by running your compiled C program.