You are a data engineer tasked with building an ETL pipeline that extracts financial transaction records from a NoSQL store, performs graph-based network analysis, and loads the enriched data into a relational data warehouse for querying.

Your objective is to complete the following steps in the `/home/user` directory.

1. **Environment Setup:**
   - Install `mongodb`, `pymongo`, and `networkx`. (You can use `sudo apt-get update && sudo apt-get install -y mongodb` or similar for your environment).
   - Start a local MongoDB instance in the background. Store its data in `/home/user/mongo_data` and log to `/home/user/mongo.log`.
   - A file named `/home/user/transactions.jsonl` has been provided. Load this JSON Lines file into your local MongoDB database named `fin_data`, inside a collection named `transactions`.

2. **Data Extraction & Aggregation (Python):**
   - Write a Python script `/home/user/etl_pipeline.py`.
   - In the script, connect to MongoDB. Execute a **NoSQL aggregation pipeline** to calculate the total transaction volume (sum of `amount`) between every unique `sender` and `receiver` pair.
   - Filter the aggregated results directly in the MongoDB pipeline to only include pairs where the total volume is strictly greater than `50`.

3. **Graph Analytics (Python):**
   - Using the aggregated and filtered results, build a directed graph using `networkx` (`DiGraph`), where nodes are the entities and edges have a `weight` attribute equal to the total volume.
   - Calculate the PageRank centrality for all nodes in this graph (use the default `networkx.pagerank` parameters: alpha=0.85).

4. **Data Loading & Relational Querying (Python):**
   - Create a local SQLite database at `/home/user/warehouse.db`.
   - Create two tables: `nodes` (columns: `node_id` TEXT PRIMARY KEY, `pagerank` REAL) and `edges` (columns: `sender` TEXT, `receiver` TEXT, `volume` REAL).
   - Use **parameterized SQL queries** to safely insert the calculated PageRank values into the `nodes` table and the filtered aggregated edges into the `edges` table.
   - Execute a complex SQL query using JOINs to find the single "Most Influential Transfer". This is defined as the edge that has the highest combined PageRank of its sender and receiver (i.e., `sender_pagerank + receiver_pagerank`).
   - Write this single highest-ranking record to `/home/user/result.csv` with the exact header: `sender,receiver,volume,combined_pagerank`. Format floats to 4 decimal places.

Ensure `/home/user/etl_pipeline.py` is fully functional and produces the correct `result.csv` when run.