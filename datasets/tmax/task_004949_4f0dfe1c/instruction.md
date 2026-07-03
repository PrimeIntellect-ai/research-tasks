As a data analyst, I am working on an anti-money laundering (AML) project. We have a proprietary graph analytics engine compiled as a standalone Linux application. Unfortunately, the source code for this engine was lost, and we only have a stripped binary located at `/app/analyzer_oracle`.

We need to migrate this pipeline into a pure Python implementation so we can integrate it with our modern NoSQL and graph databases (like Neo4j and MongoDB). 

Your task is to write a Python CLI application at `/home/user/graph_pipeline.py` that behaves exactly like the `/app/analyzer_oracle` binary. 

Here is what we know about the pipeline:
1. Both the binary and your script must accept a single argument: the path to a CSV file containing transaction data.
2. The CSV has the following headers: `source_id`, `target_id`, `amount`, `timestamp`, `transaction_type`.
3. The binary reads the CSV, filters the data through a specific aggregation pipeline (which you'll need to figure out by observing the binary's behavior with test CSVs), and constructs a directed graph.
4. It then computes a specific centrality metric or clustering coefficient for the nodes and outputs the result as a strict JSON string to `stdout`.
5. The JSON output conforms to a specific schema, mapping string node IDs to their float centrality/analytics scores (rounded to 4 decimal places).

To succeed, you must:
1. Reverse engineer or treat the `/app/analyzer_oracle` as a black box to deduce the exact filtering rules (e.g., ignoring certain `transaction_type`s or filtering by `amount` threshold).
2. Deduce the exact graph analytics algorithm it applies (e.g., PageRank, Degree Centrality, Closeness).
3. Implement the exact equivalent pipeline in `/home/user/graph_pipeline.py` using Python (you may use `pandas`, `networkx`, or any standard library).
4. Ensure your output is BIT-EXACT with the binary's output for any given valid CSV input. It must print a valid JSON object mapping `source_id`/`target_id` (as strings) to their computed metric (as floats) to standard output.

We will verify your script against the oracle using thousands of randomly generated CSV files.