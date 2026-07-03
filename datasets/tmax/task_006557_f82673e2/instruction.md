You are acting as a database administrator managing a relational database that stores a knowledge graph. We suspect that due to some recent schema migrations, querying specific graph patterns has become extremely inefficient or returns malformed data. 

Your task is to reverse engineer the schema of the SQLite database located at `/home/user/graph_data.db` and write a Python script that extracts a specific graph pattern using parameterized queries.

Write a Python script at `/home/user/find_triangles.py` that accepts exactly one command-line argument: a relationship type (a string, e.g., `"KNOWS"`).

The script must:
1. Connect to `/home/user/graph_data.db`.
2. Use a **parameterized SQL query** to find all directed cyclic triangles of the given relationship type. A directed cyclic triangle exists if there are edges: Node A -> Node B, Node B -> Node C, and Node C -> Node A, all having the exact relationship type passed via the command line.
3. Validate and format the output. The output must be saved to `/home/user/triangles.json` as a JSON array of arrays. Each inner array must contain the three node IDs of the triangle, **sorted in ascending numerical order** (to avoid permutation duplicates). 
4. Ensure the outer JSON array contains only unique triangles (no duplicate arrays).
5. The script must execute cleanly without errors when run as `python3 /home/user/find_triangles.py "KNOWS"`.

Ensure your query is robust and relies exclusively on parameterized construction to prevent SQL injection, simulating a production-grade optimization task.