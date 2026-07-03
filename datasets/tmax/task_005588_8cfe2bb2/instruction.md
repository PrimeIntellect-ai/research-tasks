You are a data analyst assisting with processing a dataset of e-commerce transactions. 

I have a raw CSV file containing transaction records at `/home/user/data/sales.csv`. The file has the following columns:
`tx_id` (string), `user_id` (string), `amount` (float), `timestamp` (string, ISO8601 format).

I need you to write a Go program at `/home/user/analyzer.go` that performs the following data pipeline operations:

1. **Database Setup:** Read the `sales.csv` file and load the data into a local SQLite database file named `/home/user/sales.db`. (You can drop and recreate the table if the program is run multiple times).
2. **Analytical Query:** Construct a parameterized SQL query that calculates a moving average of the `amount` for each `user_id`. Specifically, for each transaction, compute the average of the current transaction amount and the up-to 2 preceding transaction amounts for that same user, ordered by `timestamp` ascending. 
3. **Filtering & Pagination:** The query must filter out any rows where the original transaction `amount` is less than or equal to a specified `min_amount`. The results should be sorted globally by `user_id` ascending, then `timestamp` ascending. The query must also apply `LIMIT` and `OFFSET` for pagination.
4. **Parameterized Execution:** The `min_amount`, `limit`, and `offset` must be safely passed to the SQL query as parameters (do not use string concatenation for these values to prevent SQL injection).
5. **Output:** The program should accept these parameters via command-line flags (`-min`, `-limit`, `-offset`). It must execute the query and write the result to `/home/user/report.csv`. The output CSV must contain the columns: `tx_id`, `user_id`, `amount`, `timestamp`, `moving_avg` (rounded to 2 decimal places).

Please write the Go code, initialize the necessary Go module at `/home/user`, install any required dependencies (e.g., `github.com/mattn/go-sqlite3` requires CGO, so ensure `CGO_ENABLED=1` is used if needed), and run your program with the following arguments:
`-min 30.0 -limit 6 -offset 2`

Ensure the final output file `/home/user/report.csv` contains the header row and the exact 6 rows corresponding to the parameters provided.