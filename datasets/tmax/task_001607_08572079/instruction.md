You are a data engineer building an ETL pipeline tool in C. You have been given an SQLite database file at `/home/user/knowledge.db` containing a knowledge graph. However, the documentation for the database schema has been lost.

Your task is to:
1. Reverse engineer the schema of `/home/user/knowledge.db` to understand how nodes and directed edges are stored. The graph has named nodes and directed edges between them.
2. Write a C program at `/home/user/path_finder.c` that uses the SQLite C API (`sqlite3.h`) to read this database.
3. The C program must take exactly two command-line arguments: the name of a starting node and the name of a destination node.
   Example: `./path_finder "StartNode" "EndNode"`
4. Inside the C program, construct parameterized SQL queries to safely retrieve node IDs and relationships (preventing SQL injection).
5. Implement a graph traversal algorithm (Breadth-First Search) in C to find the shortest directed path between the two nodes. If there are multiple paths of the same shortest length, resolve ties by choosing the node whose name comes first lexicographically at each step.
6. Compile your program to an executable named `/home/user/path_finder`. You can link SQLite using `-lsqlite3`.
7. Run your program with the arguments `"Alpha"` and `"Omega"`.
8. The program must output the names of the nodes in the shortest path, in order, from the start node to the destination node, writing one node name per line to the file `/home/user/path.txt`.

Ensure your C program handles potential errors (e.g., nodes not found) gracefully, but for the verification, we will only check the contents of `/home/user/path.txt` after you run the successful query from "Alpha" to "Omega".

Do not modify the database. Write the C code, compile it, and generate the output file.