You are a Database Administrator working with a locally managed knowledge graph. We use Python to parse and run graph queries on exported data. 

Currently, we have an edge list of a movie knowledge graph exported to `/home/user/graph.csv`. The CSV has no header, and each row contains two comma-separated node IDs representing an undirected edge. Nodes starting with `A:` are Actors, `M:` are Movies, and `D:` are Directors.

Your task is to write an optimized Python script at `/home/user/graph_query.py` that performs the following complex graph query and analytics pipeline:

1. **Load the Graph**: Read `/home/user/graph.csv` into an undirected graph. You may install and use the `networkx` library.
2. **Graph Analytics**: Calculate the standard Degree Centrality for all nodes in the graph.
3. **Knowledge Graph Pattern Matching**: Find all unique Actors (`A:`) who are connected to a Movie (`M:`) that is also connected to a Director (`D:`).
4. **Query Filtering/Optimization**: From the matched Actors, filter down to ONLY those Actors who are connected to at least one Movie directed by a "Top Director". A "Top Director" is defined as a Director whose Degree Centrality is STRICTLY GREATER than `0.10`.
5. **Output**: Identify the single Actor from the filtered list who has the highest Degree Centrality. Write ONLY their node ID (e.g., `A:SomeActor`) to the file `/home/user/query_result.txt`. If there is a tie, output the one that comes first alphabetically.

*Note: You must set up any virtual environments or install required packages yourself. Ensure your script handles standard CSV reading and writes the exact requested output format.*