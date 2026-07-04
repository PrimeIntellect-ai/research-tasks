You are a database administrator tasked with optimizing a complex analytics workflow for a messaging platform. The platform recently exported a large chunk of message metadata as a NoSQL document dump. 

Your objective is to build a Python script at `/home/user/analyze.py` that processes this data, projects it into a graph, identifies key influencers, and performs analytical window aggregations on their activity.

Here are the exact requirements for your script:

1. **Data Source:** Read the NoSQL dump located at `/home/user/data/messages.jsonl`. Each line is a JSON object with keys: `msg_id` (int), `sender` (string), `receiver` (string), `timestamp` (string, ISO format), and `bytes` (int).
2. **Graph Projection & Materialization:** Aggregate the data to build a directed graph. An edge from `sender` to `receiver` should have a weight equal to the *total sum of bytes* sent from that sender to that receiver across all messages.
3. **Graph Processing:** Calculate the PageRank of all users in this graph using NetworkX's `pagerank` function (use `alpha=0.85` and `weight='weight'`). Identify the Top 3 users with the highest PageRank scores. Break ties alphabetically by user name.
4. **Window Function / Analytical Aggregation:** Filter the original `messages.jsonl` data to only include messages where the `sender` is one of the Top 3 PageRank users. For each of these messages, compute a new field called `cumulative_bytes`. This field must represent the cumulative sum of `bytes` sent by that specific `sender` up to and including the current message, ordered by `timestamp` (and then `msg_id` if timestamps are identical). You can use DuckDB, Pandas, or pure Python for this step.
5. **Sorting, Pagination, and Filtering:** Take the filtered dataset (which now includes `cumulative_bytes`) and sort it globally by `timestamp` ascending, then `msg_id` ascending. We need to paginate this data to send to a dashboard. Assuming a page size of 5 items, extract exactly **Page 2** (which corresponds to items index 5 through 9, i.e., the 6th through 10th items).
6. **Output:** Save the paginated result as a JSON array of objects to `/home/user/report.json`. Each object must contain exactly: `msg_id`, `sender`, `timestamp`, `bytes`, and `cumulative_bytes`.

You may install any required Python packages (like `networkx`, `pandas`, or `duckdb`) into the user environment using `pip`.