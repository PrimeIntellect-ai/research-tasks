You are an AI assistant helping a research scientist organize a citation knowledge graph. 

The researcher has a SQLite database located at `/home/user/citation_graph.db` containing two tables:
1. `papers` (id INTEGER PRIMARY KEY, title TEXT)
2. `citations` (from_id INTEGER, to_id INTEGER)

We need to extract a specific subgraph pattern to analyze intermediary papers. Specifically, we want to find all papers `X` that act as a bridge between two specific papers `A` and `B`. The pattern is: `A` cites `X`, and `X` cites `B`. 

Your task is to write a C program at `/home/user/process_graph.c` that does the following:
1. Takes two integer arguments from the command line: `source_id` (A) and `target_id` (B).
2. Connects to the `/home/user/citation_graph.db` SQLite database.
3. Uses a **parameterized query** to find all paper IDs and titles for the bridging papers `X`.
4. Performs **output schema validation** in C: skip any paper `X` where the `title` is `NULL` or is an empty string `""`.
5. Writes the validated results to `/home/user/valid_nodes.json` as a valid JSON array of objects. Each object must have the schema: `{"id": <integer>, "title": "<string>"}`. If no valid nodes are found, output an empty array `[]`.

To complete this task:
1. Install any necessary development libraries for SQLite in C.
2. Write the C program `/home/user/process_graph.c`.
3. Compile it to an executable named `/home/user/process_graph`.
4. Run your program with `source_id = 10` and `target_id = 50`.

The automated test will verify the presence of the compiled executable and the exact contents of `/home/user/valid_nodes.json`.