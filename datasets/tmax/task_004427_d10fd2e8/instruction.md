You are a Database Administrator and C++ systems engineer tasked with optimizing a graph data extraction pipeline. 

We have a proprietary tool that generates a massive knowledge graph represented as relational tables in SQLite. The tool is provided as a stripped binary at `/app/data_generator`. 

When executed in a directory, `/app/data_generator` will create an SQLite database named `graph.db` containing two tables:
- `Nodes (id INTEGER PRIMARY KEY, type TEXT, value REAL)`
- `Edges (source INTEGER, target INTEGER, weight REAL)`

Your objective is to write a highly optimized C++ program (`/home/user/query_optimizer.cpp`) that performs a specific cross-query aggregation and outputs the results to `/home/user/results.csv`.

The analytical query you need to resolve is:
For every node of type 'AUTHOR', find all 'ARTICLE' nodes connected to it within exactly 2 hops (i.e., AUTHOR -> [any node] -> ARTICLE). 
Calculate the "Influence Score" for each AUTHOR, which is defined as the sum of `(ARTICLE.value * edge1.weight * edge2.weight)` for all valid 2-hop paths to an 'ARTICLE'. 
If there are multiple paths to the same article, sum them independently.
Finally, export the top 100 AUTHORs ordered by their Influence Score in descending order, then by their node ID in ascending order.

Your C++ program must:
1. Connect to the `graph.db` SQLite database.
2. Design and execute an index strategy (create the necessary indexes to make the query fast).
3. Execute the query using optimized SQL (Recursive CTEs or standard JOINS) and/or cross-query aggregation in C++.
4. Write the results to `/home/user/results.csv` with the format: `author_id,influence_score` (score formatted to 4 decimal places).

**Constraints & Performance:**
- You must compile your code with: `g++ -O3 /home/user/query_optimizer.cpp -lsqlite3 -o /home/user/query_optimizer`
- Your compiled program will be timed. The target threshold for your program's execution time (including index creation and querying) is **<= 1.5 seconds**. 
- Run `/app/data_generator` in `/home/user/` to generate the test database before testing your code.

Deliver your C++ source code in `/home/user/query_optimizer.cpp`.