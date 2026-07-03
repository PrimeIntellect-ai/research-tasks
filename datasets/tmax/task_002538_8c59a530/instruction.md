You are a data engineer responsible for building an ETL pipeline and API service that detects and analyzes database deadlocks.

We have a simulated environment with two upstream data services representing a database lock manager. 
There is a startup script located at `/app/start_services.sh`. You must run this script in the background to start the upstream services.
- The "Wait-for Edges" service runs on `http://127.0.0.1:9001`. The endpoint `GET /edges` returns a JSON list of lock dependencies representing transactions waiting for other transactions. Format: `[{"waiter": "T1", "holder": "T2"}, ...]` meaning transaction `T1` is waiting for transaction `T2` to release a lock.
- The "Metadata" service runs on `http://127.0.0.1:9002`. The endpoint `GET /nodes` returns a JSON list of transaction metadata. Format: `[{"tx_id": "T1", "user": "alice"}, ...]`

Your task is to write a Python HTTP API service using `Flask` or `FastAPI` (saved as `/home/user/etl_api.py`) that listens on `127.0.0.1:8080`. Your service must pull data from the two upstream services, construct a directed knowledge graph (`waiter` -> `holder`), and expose the following analytical endpoints:

1. `GET /api/deadlocks`
This endpoint must return a JSON response containing all deadlock cycles (simple cycles) in the graph.
- A cycle should be represented as a list of `tx_id`s. 
- To ensure a deterministic output, each cycle must start with the lexicographically smallest `tx_id` within that cycle, while preserving the cyclic order of nodes.
- The list of cycles must be sorted first by cycle length (ascending), and then lexicographically by the sequence of nodes in the cycle.
Response Schema:
```json
{
  "deadlocks": [
    ["T1", "T2", "T3"],
    ["T4", "T5", "T6", "T7"]
  ]
}
```

2. `GET /api/pagerank`
This endpoint calculates the PageRank of all transactions in the wait-for graph to identify the most central blocking transactions. 
- Use the `networkx` library's `pagerank` algorithm with `alpha=0.85`.
- Round the PageRank scores to 4 decimal places.
- Combine the results with the user metadata from the Metadata service. If a node is missing metadata, use `"user": "unknown"`.
- Support pagination via query parameters `page` (1-indexed, default: 1) and `limit` (default: 10).
- The results must be sorted by PageRank score descending, and in case of a tie, by `tx_id` ascending.
Response Schema:
```json
{
  "page": 1,
  "limit": 5,
  "total_nodes": 15,
  "results": [
    {"tx_id": "T2", "score": 0.1543, "user": "alice"},
    ...
  ]
}
```

Write the service, start the upstream dependencies, and run your API service in the background on port 8080. Leave it running so that the verification test suite can query it.