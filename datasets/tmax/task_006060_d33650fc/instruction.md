You are a data engineer building an ETL pipeline that processes hierarchical organizational data. 

We have an RDF graph in Turtle format located at `/home/user/org_chart.ttl`. This graph represents employees and their reporting lines using the `http://example.org/org#reportsTo` predicate.

Your task is to write and execute a Python script (`/home/user/etl_graph.py`) that performs the following steps:
1. Load the RDF graph from `/home/user/org_chart.ttl`.
2. Execute a recursive SPARQL query to identify all employees who "deeply report" to `http://example.org/CEO`. A "deep report" is defined as an employee who reports to the CEO via a chain of 2 or more `reportsTo` edges (i.e., they are not direct reports to the CEO, but report to someone who eventually reports to the CEO).
3. Materialize these findings into a new projected graph. For every deep report found, add a triple to this new graph: `<?employee> <http://example.org/org#deepReportsTo> <http://example.org/CEO>`.
4. Serialize this new projected graph to a file located at `/home/user/projected.nt` in the N-Triples (`nt`) format. 

Requirements:
- You must use the `rdflib` library in Python (you may need to install it).
- Ensure the output file contains ONLY the materialized `deepReportsTo` triples.
- Run the script so that `/home/user/projected.nt` is generated successfully.