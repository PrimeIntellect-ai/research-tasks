You are a data engineer tasked with building an ETL pipeline step that extracts transaction data, performs graph-based network analysis to identify key actors, and outputs strictly validated data.

Your workspace contains a SQLite database at `/home/user/transactions.db`. 
You also have a JSON schema definition at `/home/user/schema.json`.

Your objective is to write and execute a Python script that performs the following steps:

1. **Extract**: Connect to `/home/user/transactions.db`. Use a **parameterized query** to select all transactions where the `amount` is strictly greater than `50.0`, and the `tx_date` is between `'2023-01-01'` and `'2023-01-31'` (inclusive). 

2. **Transform (Graph Analytics)**: 
   - Using the `networkx` library, build a directed graph from the filtered transactions. 
   - Nodes represent accounts (`sender` and `receiver`).
   - Edges represent the flow of money. The weight of an edge from node A to node B should be the *sum* of all transaction amounts from A to B within the filtered data.
   - Calculate the PageRank of the nodes using `networkx.pagerank()` with `alpha=0.85` and `weight='weight'`.

3. **Validate and Load**:
   - Identify the top 3 accounts with the highest PageRank scores. Sort them in descending order of their PageRank.
   - Construct a JSON object structured exactly like this:
     ```json
     {
       "metadata": {
         "threshold": 50.0,
         "date_start": "2023-01-01",
         "date_end": "2023-01-31"
       },
       "top_nodes": [
         {"account": "Account_X", "pagerank": 0.1234},
         ...
       ]
     }
     ```
   - Validate this JSON dictionary against the schema provided at `/home/user/schema.json` using the `jsonschema` Python library.
   - If validation passes, write the JSON output to `/home/user/output_graph_metrics.json` with an indentation of 2 spaces.

You may need to install `networkx` and `jsonschema` if they are not already present in your environment (`pip install networkx jsonschema`).