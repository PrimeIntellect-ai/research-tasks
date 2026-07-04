You are a data engineer building the first stage of a new ETL pipeline. We have a dump of NoSQL transactional logs from a legacy system. The logs implicitly define a directed graph of relationships between users, but the data model is unstructured and undocumented. 

Your task is to reverse-engineer this implicit schema, extract the graph, compute a basic centrality metric, and output the result for the next stage of the pipeline.

The raw data is located at `/home/user/data/transactions.jsonl`. Each line is a JSON object representing a transaction event. 
Through your schema analysis, you will discover that each transaction has a source entity and an array of destination entities.

Using Rust, write a script that processes this file to:
1. Parse the NoSQL JSON dump and map the implicit relationships to a directed graph. A relationship is formed from the source entity to EACH destination entity in the transaction. 
2. Calculate the in-degree and out-degree for every entity in the graph. 
3. Identify the entity with the highest total degree (in-degree + out-degree). If there is a tie, select the entity with the lexicographically smallest name.
4. Output the result for this top entity as a JSON file to `/home/user/etl_output.json` with exactly the following keys:
   `top_entity` (string), `total_degree` (integer), `in_degree` (integer), `out_degree` (integer).

To help you get started quickly, an empty Rust Cargo project has been initialized at `/home/user/graph_etl`. It already has `serde` and `serde_json` configured in its `Cargo.toml`. 

Write your Rust code in `/home/user/graph_etl/src/main.rs`, compile, and run it to produce the final `/home/user/etl_output.json` file.