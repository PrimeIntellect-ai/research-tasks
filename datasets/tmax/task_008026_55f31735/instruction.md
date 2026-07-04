You are a data engineer building an ETL pipeline to analyze financial transaction graphs. 

You have been provided with a raw JSONL data file at `/home/user/data/transactions.jsonl`. This file contains NoSQL-style document logs of various system events. Some are 'transfer' events between users, representing directed edges in a financial graph.

Your goal is to extract these edges, load them into a relational database, design an index strategy, and perform an analytical graph query.

**Phase 1: NoSQL Aggregation & Extraction**
1. Write a Python script named `/home/user/scripts/extract.py` that reads `/home/user/data/transactions.jsonl`.
2. Filter the stream to only include records where `"event_type" == "transfer"` and `"status" == "success"`.
3. Extract the `sender`, `receiver`, `timestamp`, and `amount` fields.
4. Output this cleaned data to a CSV file at `/home/user/data/edges.csv` with headers `source,target,timestamp,amount`.

**Phase 2: Database Design & Loading**
1. Create a SQLite database at `/home/user/db/graph.sqlite`.
2. Write a SQL script at `/home/user/scripts/schema.sql` to create a table `Edges(source TEXT, target TEXT, timestamp INTEGER, amount REAL)`.
3. In the same script, design and create the necessary **indexes** on the `Edges` table to optimize continuous path traversals (querying where one transaction's target becomes the next transaction's source, ordered by time).
4. Load the `edges.csv` data into the `Edges` table.

**Phase 3: Graph Analytics Query**
Write a SQL script at `/home/user/scripts/analyze.sql` that executes the following logic and outputs the results to `/home/user/results/top_paths.csv`.
1. Find all continuous transaction paths of exactly 3 hops (4 nodes: A -> B -> C -> D).
2. A valid path requires that the `timestamp` of hop 2 is strictly greater than hop 1, and hop 3 is strictly greater than hop 2.
3. For each valid path, calculate the `total_amount` (sum of the 3 amounts).
4. Use a **window function** to assign a `path_rank` to each path, partitioned by the starting node (`source` of hop 1), ordered by the `total_amount` descending.
5. Filter the results to only include paths where `path_rank = 1` (the top path for each starting node).
6. Sort the final results globally by `total_amount` descending, and paginate to keep only the top 5 overall paths.
7. The output CSV `/home/user/results/top_paths.csv` must have exactly these headers: `start_node,end_node,total_amount`. (`start_node` is the source of hop 1, `end_node` is the target of hop 3).

Make sure all directories (`/home/user/scripts`, `/home/user/data`, `/home/user/db`, `/home/user/results`) are created as needed.