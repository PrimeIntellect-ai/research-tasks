You are a data engineer building a lightweight ETL pipeline. We have a daily export of transaction data from our NoSQL document database, stored as a JSONL (JSON Lines) file. You need to process this data to extract graph metrics for our fraud detection team.

The input data is located at: `/home/user/transactions.jsonl`
Each line is a JSON object representing a directed edge in our transaction graph, with the following schema:
`{"tx_id": "string", "sender": "string", "receiver": "string", "amount": number}`

Your task is to write a Rust program that:
1. Reads the NoSQL dump from `/home/user/transactions.jsonl`.
2. Calculates the **In-Degree Centrality** for every node in the graph (i.e., count the total number of incoming transactions each `receiver` node gets).
3. Exports the top 3 receiving nodes with the highest in-degree to a CSV file at `/home/user/top_nodes.csv`.

**Output Specifications:**
- The CSV file `/home/user/top_nodes.csv` must NOT have a header row.
- Each row must be formatted exactly as: `node_id,in_degree`
- Sort the top 3 results in descending order by `in_degree`.
- If two or more nodes have the exact same in-degree, resolve ties by sorting the `node_id` alphabetically in ascending order (e.g., "A" comes before "B").

We have already initialized a Cargo project for you at `/home/user/graph_etl` with `serde` and `serde_json` dependencies included. Write your Rust code in `/home/user/graph_etl/src/main.rs`, compile, and execute it to generate the CSV file.