You are a database administrator tasked with optimizing and implementing a reporting query for an e-commerce platform.

A SQLite database is located at `/home/user/ecommerce.db` with the following schema:
- `customers` (id INTEGER PRIMARY KEY, name TEXT, region TEXT)
- `orders` (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, order_date TEXT)

Your task is to write a Go program at `/home/user/generate_report.go` that generates a regional top-customer report using window functions and parameterized queries.

The Go program must:
1. Accept two command-line flags: `-region` (string) and `-limit` (int).
2. Connect to the SQLite database at `/home/user/ecommerce.db` (you may use `github.com/mattn/go-sqlite3`).
3. Execute a single, highly optimized SQL query that:
   - Filters customers by the provided `region` using a parameterized query (to prevent SQL injection).
   - Calculates the `total_spend` for each customer in that region.
   - Assigns a `rank` to each customer based on their `total_spend` in descending order (highest spend is rank 1).
   - Calculates a `running_total` of spend in that region, ordered by rank (the sum of `total_spend` of the current customer and all higher-ranked customers).
   - Limits the final result to the top N customers specified by the `limit` parameter.
4. Output the results to a CSV file at `/home/user/report.csv` with the exact header:
   `name,total_spend,rank,running_total`
   followed by the rows of data.

Ensure your Go environment is properly initialized (e.g., running `go mod init report` and `go get github.com/mattn/go-sqlite3` in `/home/user/`). The file `/home/user/generate_report.go` must compile successfully.