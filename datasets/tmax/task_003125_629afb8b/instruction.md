You are a data engineer building a graph-based ETL pipeline. You have been provided with an undocumented JSON extract of social interactions at `/home/user/raw_data.json`. 

Your task is to write and execute a Python script (`/home/user/etl.py`) that performs the following steps:

1. **Data Model Reverse Engineering**: Inspect `/home/user/raw_data.json` to understand its schema. Identify where the author's user handle is stored and where the handles of users they mention are stored in each document.
2. **RDF Graph Construction**: Using the `rdflib` Python library, build an in-memory RDF graph. 
   - Define nodes for each user using the namespace `http://example.org/user/` (e.g., `http://example.org/user/alice`).
   - Create triples indicating mentions using the predicate `http://example.org/schema/mentions`.
3. **Graph Querying**: Execute a SPARQL query against your `rdflib` graph to extract all valid mention edges (who mentioned whom).
4. **Graph Analytics**: Using the results from your SPARQL query, build a directed graph in `networkx`. Add directed edges from the mentioning user to the mentioned user.
5. **PageRank**: Calculate the PageRank of all nodes in the directed graph using `networkx.pagerank` with `alpha=0.85` (use the default parameters for the rest).
6. **Output**: Save the resulting PageRank dictionary to `/home/user/pagerank.json`. The keys should be the raw user handles (e.g., `"alice"`, not the full URI), and the values should be the PageRank floats. Ensure the JSON is properly formatted.

You may install any required Python packages (e.g., `rdflib`, `networkx`) using pip.