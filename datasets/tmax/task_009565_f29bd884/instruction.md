You are a Database Administrator tasked with optimizing and analyzing a microservice communication database. The data is stored in an SQLite database located at `/home/user/microservices.db`.

The database has the following schema:
```sql
CREATE TABLE services (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE calls (
    source_id INTEGER,
    target_id INTEGER,
    call_count INTEGER,
    latency_ms REAL,
    FOREIGN KEY(source_id) REFERENCES services(id),
    FOREIGN KEY(target_id) REFERENCES services(id)
);
```

Your goal is to build a Go-based data pipeline that performs cross-query aggregation and graph analytics to identify the major bottleneck service. 

Follow these exact steps:
1. Initialize a Go module at `/home/user/pipeline` and write a Go program named `analyze.go`.
2. Your program must connect to the SQLite database (using `github.com/mattn/go-sqlite3`).
3. Using SQL Window Functions within your Go program, query the database to find the "Top 2" highest-latency outgoing calls for *each* `source_id`.
4. Using only this filtered subset of "Top 2" edges, construct a directed graph in Go.
5. Perform graph analytics to calculate the **in-degree** (number of incoming edges) for each target service in this sub-graph.
6. Identify the service with the highest in-degree in the sub-graph. If there is a tie, resolve it by selecting the one with the highest average `latency_ms` among its incoming edges in the sub-graph.
7. Your Go program must write the result to a JSON file at `/home/user/optimized_report.json` with the following exact format:
```json
{
  "top_service": "Service Name",
  "in_degree": 0,
  "avg_latency": 0.0
}
```

Requirements:
- You must write and execute the Go program to produce the JSON file.
- Do not modify the original database.
- Use standard SQLite features and Go logic.