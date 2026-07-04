You are a data analyst tasked with processing a large dataset of transaction events and feeding them into a proprietary graph database engine. 

You have been provided with a raw CSV file at `/home/user/events.csv` with the following columns: `event_id`, `timestamp`, `src_node`, `dst_node`, and `amount`.

Your objective is to write a Python script at `/home/user/pipeline.py` that performs the following steps:
1. Loads the CSV data.
2. Computes a rolling average of the `amount` for each `src_node` over a window of the last 3 events (including the current event), ordered strictly by `timestamp`. 
3. Filters the dataset to keep ONLY the events where the current `amount` is strictly greater than this rolling average.
4. Generates a sequence of graph ingestion commands and saves them to `/home/user/commands.txt`.

The graph ingestion commands must be formatted exactly as:
`ADD EDGE <src_node> <dst_node> <amount>`

You are provided with a proprietary database engine binary at `/app/graph_builder`. This binary processes the commands from standard input and computes a final graph state. 
However, `/app/graph_builder` has a known concurrency quirk: it processes edges in parallel batches. If edges originating from the same `src_node` are submitted out of chronological order, the transaction engine will deadlock and silently drop those edges. To maximize the integrity of the constructed graph, you must ensure that your generated commands in `/home/user/commands.txt` are sorted optimally to avoid this deadlock (e.g., sorted primarily by `src_node` and secondarily by `timestamp`).

The automated test will evaluate your output by piping `/home/user/commands.txt` into `/app/graph_builder` and comparing the resulting graph connectivity metric against the optimal target. Your score will be based on the percentage of valid edges successfully committed to the graph. You need to achieve an accuracy metric of >= 0.99 (99%).

You may use standard Python libraries like `pandas` or `sqlite3` to perform the window functions and analytical aggregations. Ensure your pipeline script handles the entire process autonomously when executed.