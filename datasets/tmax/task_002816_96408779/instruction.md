You are a data engineer building an ETL pipeline to process social network data. You have been provided a document-based dataset of user interactions, and you need to project it into a graph model to extract a specific topological pattern.

The input data is located at `/home/user/interactions.jsonl`. Each line is a JSON object representing a directed interaction, for example:
`{"source_node": "alice", "target_node": "bob", "interaction_type": "follows"}`

Your objective is to:
1. Reverse engineer the document model into a graph. You only care about edges where the `interaction_type` is `"follows"`.
2. Write a C program at `/home/user/find_triangles.c` that reads the filtered edges and materializes a directed graph in memory.
3. Use this C program to perform graph pattern matching to find all directed triangles. A directed triangle is a cycle of exactly three nodes: A -> B -> C -> A.
4. Normalize each found triangle so that it is represented starting with the lexicographically smallest node name. For example, if you find `bob -> charlie -> alice -> bob`, it should be normalized to `alice,bob,charlie`.
5. Sort all normalized triangles lexicographically by the first node, then the second node, then the third node.
6. Apply pagination/filtering to your results: output exactly the first 5 triangles (or fewer if less than 5 exist) to a file named `/home/user/triangles.csv`.

Output File Format Requirements (`/home/user/triangles.csv`):
- Pure CSV format, no headers.
- Exactly 3 columns per line: `Node1,Node2,Node3`.
- Max 5 lines (the top 5 lexicographically sorted triangles).

You may use standard Linux shell utilities (like `grep`, `awk`, `sed`) to pre-process the JSONL file into a simpler format before reading it with your C program if you wish. Ensure your C program compiles successfully with standard `gcc` (e.g., `gcc -O2 /home/user/find_triangles.c -o /home/user/find_triangles`).