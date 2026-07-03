You are a data analyst working on a graph data pipeline. We ingest hierarchical data from CSV files (`id,parent_id`), which are then loaded into a SQL database. However, some CSV files contain cycles, which cause our recursive CTEs to infinite-loop or produce implicit cross joins downstream.

Your task is to create a Go-based classifier that acts as a filter to reject "evil" CSV files (containing cycles) while accepting "clean" CSV files (valid trees/forests).

Requirements:
1. Write a Go program at `/home/user/classifier.go`.
2. It must take a single file path as a CLI argument: `go run /home/user/classifier.go <path_to_csv>`.
3. If the CSV contains a cycle (Evil), the program must print `EVIL` to stdout and exit with code 1.
4. If the CSV does not contain a cycle (Clean), it must print `CLEAN` to stdout and exit with code 0.
5. The CSV files have a header `id,parent_id`. A row like `A,B` means an edge from A to B. (If `parent_id` is empty, it's a root node).

To help you, we have vendored a third-party graph package at `/app/graph` (a clone of a popular Go graph library). However, the previous developer made a typo in the vendored package's source code, causing it to fail to compile.
You must:
- Fix the bug in the vendored package at `/app/graph`.
- Use this package in your `classifier.go` to build a directed graph and check for cycles. (Set up your `go.mod` to replace the module path with the local `/app/graph` directory).

Ensure your classifier perfectly separates clean from evil files.