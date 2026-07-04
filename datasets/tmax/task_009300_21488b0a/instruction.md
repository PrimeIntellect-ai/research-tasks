You are assisting a compliance officer in auditing system access records. The access records have been exported as an RDF graph in Turtle format at `/home/user/access_graph.ttl`. 

Your task is to analyze this graph to identify highly accessed systems, which represent elevated security risks. You may use any programming language (e.g., Python with `rdflib` and `networkx`), but you must accomplish the following:

1. Write a script to query the RDF graph using SPARQL. Extract all relationships where a User has accessed a System. The relevant triples use the predicate `http://example.org/audit#accessed`.
2. Construct a bipartite graph from these results (Users and Systems).
3. Compute the degree (count of unique users) for each System.
4. Output the results to a JSON file at `/home/user/system_audit.json`.
5. The JSON file must strictly conform to this schema: a JSON array of objects, where each object has two keys: `"system"` (the full URI of the system as a string) and `"user_count"` (an integer representing the number of unique users that accessed it).
6. Sort the JSON array in descending order of `"user_count"`. If there is a tie, sort alphabetically by the `"system"` URI.

Ensure your final output is correctly formatted and located exactly at `/home/user/system_audit.json`.