You are a data engineer tasked with building an ETL pipeline to analyze internal communication networks. 

You have been provided with an SQLite database at `/home/user/data/comms.db` containing three tables:
1. `departments`: `id` (INTEGER), `name` (TEXT)
2. `users`: `id` (INTEGER), `name` (TEXT), `department_id` (INTEGER)
3. `messages`: `id` (INTEGER), `sender_id` (INTEGER), `receiver_id` (INTEGER), `timestamp` (DATETIME)

Your goal is to write a Python script at `/home/user/etl_pipeline.py` that performs the following steps:

**Phase 1: SQL Extraction & Window Functions**
Connect to the SQLite database and write a query using CTEs, complex joins, and window functions to extract:
- `user_id`
- `name` (user's name)
- `department_name`
- `messages_sent`: Total number of messages sent by the user.
- `dept_rank`: The rank of the user within their department based on `messages_sent` in descending order. Use the `RANK()` window function. If users have the same number of messages sent, they should share the same rank.

**Phase 2: Graph Analytics (NetworkX)**
Using the `messages` table, construct a directed graph where:
- Nodes represent `user_id`s.
- Directed edges represent messages sent from `sender_id` to `receiver_id`.
- The `weight` of each edge is the total count of messages sent from that sender to that receiver.

Calculate the PageRank for all nodes in the graph using NetworkX's `pagerank` algorithm. Use the parameters `alpha=0.85` and `weight='weight'`.

**Phase 3: Data Merging and Output**
Combine the extracted SQL data with the computed PageRank scores. 
Output the top 3 users with the highest PageRank scores into a JSON file at `/home/user/output/key_communicators.json`.

The JSON must be a list of dictionaries, strictly matching this format and sorted by `pagerank` descending:
```json
[
  {
    "user_id": 1,
    "name": "Alice",
    "department_name": "Sales",
    "messages_sent": 42,
    "dept_rank": 1,
    "pagerank": 0.1543
  },
  ...
]
```
*Note: Round `pagerank` to exactly 4 decimal places.*

**Requirements:**
- Ensure you create the `/home/user/output` directory if it doesn't exist.
- You may install any standard data Python packages you need (e.g., `pandas`, `networkx`).
- Execute your script so that the JSON file is created successfully.