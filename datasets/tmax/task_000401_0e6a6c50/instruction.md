You are a Database Administrator working on performance optimization for a microservices architecture. A previous developer dumped the tracing data into a SQLite database located at `/home/user/tracing.db`, but left no documentation about the schema. 

Your task is to:
1. Reverse engineer the data model of `/home/user/tracing.db` to understand how services and their RPC calls (with latencies) are stored. The database contains a directed graph of service dependencies.
2. Write a Go program at `/home/user/analyzer.go` that takes a single command-line argument: the name of a starting service.
3. The Go program must connect to `tracing.db` and execute a **parameterized query** using a Recursive Common Table Expression (CTE) to traverse the service dependency graph.
4. The query must find the "critical path" (the single path with the highest total latency) originating from the provided service name.
5. The program should materialize this projected graph path into a JSON file at `/home/user/critical_path.json`.

The JSON file must have exactly this structure:
```json
{
  "start_service": "<Service Name>",
  "total_latency_ms": <Integer total latency>,
  "path": ["<Service Name 1>", "<Service Name 2>", "..."]
}
```

To complete the task:
- Initialize a Go module in `/home/user/` (e.g., `go mod init tracing`).
- You may use the `github.com/mattn/go-sqlite3` driver.
- Run your Go program passing `"API-Gateway"` as the argument: `go run analyzer.go "API-Gateway"`
- Ensure `/home/user/critical_path.json` is generated correctly.