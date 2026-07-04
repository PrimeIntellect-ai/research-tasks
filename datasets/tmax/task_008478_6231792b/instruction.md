You are a data engineer building an ETL pipeline to map relational and document data into a flattened knowledge graph representation, and then querying it.

You have been provided with two data sources in `/home/user/data/`:
1. `docs.jsonl`: A document database dump where each line is a JSON object containing a `doc_id` (string) and a list of `keywords` (array of strings).
2. `mapping.csv`: A relational mapping file with headers `doc_id,category` that links each document to a specific domain category.

Your task involves three steps:

**Step 1: Cross-Representation Mapping & Graph Projection**
Write a Python script (or use command-line tools) to join the documents with their categories. Materialize a bipartite graph connecting `Category` to `Keyword`. 
Save this graph as an edge list in `/home/user/edges.tsv`. 
- The format must be exactly two columns separated by a single tab: `Category\tKeyword`.
- The file must contain only UNIQUE edges (if multiple documents in the same category have the same keyword, only list the edge once).
- Do not include a header row.
- Sort the file alphabetically by Category, then by Keyword.

**Step 2: Knowledge Graph Pattern Matching**
Using your materialized graph (`edges.tsv`), find the category that has the highest number of overlapping (shared) keywords with the `Cybersecurity` category. 

**Step 3: Output the Result**
Write the name of the category with the highest overlap (excluding `Cybersecurity` itself) to a file named `/home/user/top_match.txt`. The file should contain only the category name on a single line.

Make sure to leave `/home/user/edges.tsv` and `/home/user/top_match.txt` in the exact formats specified.