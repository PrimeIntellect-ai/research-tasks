You are a database administrator tasked with optimizing and analyzing a semantic knowledge graph. We have an RDF dataset of academic papers and their citation relationships located at `/home/user/graph.ttl`.

Your task is to analyze this schema and write a script (in Python using `rdflib`, or any other tool you prefer) that executes a SPARQL query to find the most "central" papers based on their in-degree (number of times they are cited). 

Requirements:
1. Find papers that have an `http://example.org/year` greater than or equal to `2010`.
2. Calculate the in-degree of these papers (number of incoming `http://example.org/cites` edges).
3. Sort the results by in-degree in descending order. If there is a tie, sort by the paper's URI in ascending order.
4. Paginate/Limit the results to return only the top 3 papers.
5. Save the output to `/home/user/top_papers.csv` with exactly two columns: `uri,in_degree`. The CSV must have a header.

Example output format:
```csv
uri,in_degree
http://example.org/paper1,4
http://example.org/paper3,2
```

Note: The graph uses the `http://example.org/` namespace. Papers are of type `http://example.org/Paper`.
You may need to install necessary libraries (e.g., `pip install rdflib`) to run your queries.