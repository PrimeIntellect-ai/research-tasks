You are a data engineer building a graph processing ETL pipeline. You have been provided with two CSV files representing a directed graph of microservices and their traffic:
1. `/home/user/data/nodes.csv` (Columns: `id`, `category`) - Defines each service and its domain category.
2. `/home/user/data/edges.csv` (Columns: `src`, `dst`, `weight`) - Defines directed traffic from a source service to a destination service and the traffic volume (weight).

Your task is to write a Go program at `/home/user/etl.go` that performs the following:
1. **Schema Analysis & Ingestion:** Parse the two CSV files and load them into a local, in-memory SQLite database.
2. **Window Functions & Aggregation:** Execute a SQL query that calculates the total incoming traffic (`in_weight`) for each destination node (`dst`). Use SQL Window Functions to assign a `rank` to each node based on its `in_weight` (descending), partitioned by the node's `category`.
3. **Filtering & Chaining:** Filter the results to only include the top 2 nodes per category (i.e., `rank <= 2`). 
4. **Format Conversion & Export:** Export the queried results to a JSON file at `/home/user/output.json`. The exported JSON must strictly conform to the following schema structure:
```json
{
  "top_nodes": [
    {
      "id": "<node_id>",
      "category": "<category>",
      "in_weight": <integer>,
      "rank": <integer>
    }
  ]
}
```
5. Sort the `top_nodes` array primarily by `category` (alphabetical, ascending) and secondarily by `rank` (ascending).

Requirements:
* The Go code must be self-contained and runnable via `go run /home/user/etl.go`.
* You may initialize a Go module in `/home/user` and download necessary third-party packages (e.g., `github.com/mattn/go-sqlite3`).
* Use `CGO_ENABLED=1` if your chosen SQLite driver requires CGO.