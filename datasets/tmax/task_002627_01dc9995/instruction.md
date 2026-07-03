You are acting as a Database Administrator for a smart warehouse system. Your system uses a local SQLite database to manage robot routing across a graph-like warehouse grid, but the routing API has been experiencing malicious inputs and stale routing weights.

You have two main objectives:

**Part 1: Update the Routing Graph via Video Analysis**
A warehouse monitoring camera has captured a video of a specific corridor (edge) that periodically experiences power fluctuations, which slow down the robots.
1. Analyze the video located at `/app/warehouse_traffic.mp4`.
2. Extract the frames and count the exact number of *completely black frames* (where all pixels have RGB values of 0, 0, 0). 
3. The database is located at `/app/warehouse.db`. It contains a table `edges (source TEXT, target TEXT, weight INTEGER)`. Update the `weight` of the edge from `source = 'C'` to `target = 'D'` to be exactly the number of black frames you counted.
4. Using a SQL recursive CTE (Common Table Expression), find the shortest path (lowest total weight) from node 'A' to node 'F'. Write the sequence of nodes visited (e.g., `A,C,D,F`) as a single line comma-separated string to `/home/user/shortest_path.txt`.

**Part 2: Build a Query Filter**
The routing API accepts custom graph traversal queries, but attackers have been submitting queries with SQL injections or poorly constructed unparameterized values. 
1. I have provided a corpus of queries in `/app/corpus/clean/` (valid, parameterized queries) and `/app/corpus/evil/` (malicious or unparameterized queries with SQL injections). 
2. Write a Python script at `/home/user/query_filter.py` that accepts a single command-line argument (the path to a `.sql` file).
3. The script must inspect the SQL text and exit with status code `0` if the query is safe (clean), and exit with status code `1` if it is unsafe (evil).
4. Unsafe queries typically include unescaped single quotes used for string termination, inline `OR 1=1` clauses, or raw string interpolations instead of `?` parameters. 

Your filter must successfully accept 100% of the clean corpus and reject 100% of the evil corpus.