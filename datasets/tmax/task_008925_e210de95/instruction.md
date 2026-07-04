You are helping a researcher organize and analyze an academic collaboration dataset. The researcher has written a Rust program to process a document-oriented dataset of collaborations (`/home/user/dataset.jsonl`), project it into a SQLite database as a graph, compute the degree centrality (number of unique collaborators) for each researcher, and write the top results to a file. 

However, the researcher's current implementation in `/home/user/graph_processor` is failing. It attempts to process the data concurrently using multiple threads, but it immediately crashes with SQLite `database is locked` errors (a form of transaction deadlock/contention). Furthermore, it is missing the logic to properly compute the degree centrality using an optimized SQL aggregation pipeline.

Your task is to fix the Rust project so that it successfully:
1. Reads the NoSQL-style JSONL file at `/home/user/dataset.jsonl`. Each line is a JSON object: `{"researcher": "Name", "collaborators": ["Name1", "Name2"]}`. Note that collaborations are undirected (if A collaborates with B, B collaborates with A, even if only one direction is listed in the JSON).
2. Uses parameterized queries to populate a SQLite database at `/home/user/graph.db` with a materialized graph of these relationships. You must fix the database locking/deadlock issues (e.g., by optimizing the query plan, fixing the transaction logic, or using a single-writer approach).
3. Computes the degree centrality for every researcher in the graph (the count of unique collaborators they have).
4. Writes the top 3 researchers with the highest degree centrality to `/home/user/top_nodes.txt` in exactly this format:
```
1. <ResearcherName> - <Degree>
2. <ResearcherName> - <Degree>
3. <ResearcherName> - <Degree>
```
If there is a tie in degree, order them alphabetically by the researcher's name.

You can modify the Rust code in `/home/user/graph_processor` however you see fit, as long as the final binary can be built and run using `cargo run` to produce the correct `/home/user/top_nodes.txt` and `/home/user/graph.db`.