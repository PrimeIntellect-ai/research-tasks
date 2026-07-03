You are a data engineer building an ETL pipeline to process a NoSQL database dump of a social network's activity graph.

Your task is to analyze a raw JSON-lines dump of graph edges, find entities matching a specific Knowledge Graph pattern, compute a graph metric for them, and export the parameterized results.

The input data is located at `/home/user/social_graph.jsonl`. 
Each line is a JSON object representing a directed edge with the following schema:
`{"src": "NodeA", "dst": "NodeB", "rel": "relation_type"}`
The `rel` can be either `"mentions"` or `"follows"`.

You need to write a Python script to perform the following:
1. Parse the JSONL file and build an in-memory directed graph.
2. Pattern Matching: Identify all "Pure Target" nodes. A "Pure Target" is defined as a node that has at least one incoming `"mentions"` edge, but ZERO outgoing `"mentions"` edges.
3. Graph Analytics: For every identified "Pure Target" node, calculate its In-Degree Centrality specifically for the `"follows"` relation (i.e., the total raw count of incoming `"follows"` edges to that node).
4. Data Export: Export the results to a CSV file at `/home/user/pure_targets.csv`.
   - The CSV must have exactly two columns with the headers: `node_id,follower_count`
   - Only include the identified "Pure Target" nodes.
   - Sort the results primarily by `follower_count` in descending order, and secondarily by `node_id` in alphabetical order.
   - Output only the top 3 nodes. If there are fewer than 3, output all of them.

Ensure your Python script runs successfully and creates the exact expected CSV output file. You may use standard Python libraries.