I need help building an ETL extraction step in Go. I inherited a local SQLite database (`/home/user/warehouse.db`) from a former data engineer, but they left no documentation. 

The database contains three tables (`sys_trx_01`, `sys_dim_a`, and `sys_dim_b`) that hold our transactional data, product categories, and region information, respectively. However, I don't know the exact column names or how they link together.

Your task:
1. Reverse engineer the schema of `/home/user/warehouse.db` to identify the primary and foreign key relationships between the three tables.
2. Write a Go program at `/home/user/etl_extract.go` that executes a single query (using standard `database/sql` and `github.com/mattn/go-sqlite3`) to extract the summarized data.
3. The query must use a CTE or subquery to first filter `sys_dim_a` for records where the status is 'active'. 
4. Join the tables to calculate the sum of the transaction amounts (from `sys_trx_01`) for each active category (from `sys_dim_a`) strictly for transactions in the 'East' region (from `sys_dim_b`). Only include transactions with a timestamp strictly after '2023-01-01 00:00:00'.
5. The Go program should execute this query and write the results to `/home/user/summary.jsonl` in JSON Lines format. 
6. Each line in the output file must be a valid JSON object with exactly two keys: `"category"` (string) and `"total_amount"` (float, rounded to 2 decimal places or left as standard float if exact).

To complete the task:
- Inspect the database.
- Write the Go code.
- Run `go mod init etl` and `go get github.com/mattn/go-sqlite3` in `/home/user`.
- Execute your Go program to generate `/home/user/summary.jsonl`.