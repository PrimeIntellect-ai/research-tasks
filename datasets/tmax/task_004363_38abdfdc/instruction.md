You are a database administrator working with a Go application that processes sales data. You have been given an SQLite database at `/home/user/sales.db` with the following schema:

```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    region TEXT,
    salesperson TEXT,
    amount REAL,
    sale_date DATE
);
```

Currently, our reporting is slow and relies on extremely inefficient self-joins. Your task is to optimize the database and write a Go program to generate a clean JSON report using modern SQL window functions.

Perform the following tasks:
1. **Optimize Query Execution**: Manually connect to `/home/user/sales.db` and create a covering index named `idx_sales_perf` on the `sales` table to optimize grouping by `region` and `salesperson`.
2. **Write the Reporting Script**: Create a Go program at `/home/user/generate_report.go`.
    * It must connect to `/home/user/sales.db` using the `github.com/mattn/go-sqlite3` driver.
    * It must execute a single, highly efficient SQL query utilizing window functions to calculate:
        - The total sales `amount` for each `salesperson`.
        - The `rank` of each salesperson within their `region` based on total sales (highest sales = rank 1).
        - The total sales for the entire `region` (using an analytical window function, not a subquery).
    * Filter the final results to only include the top 2 salespeople per region (where rank <= 2).
3. **Export the Results**: The Go program must execute this query and export the results to `/home/user/top_sales.json`. The JSON file must be an array of objects with the exact following structure, ordered by `region` (ascending) and then `rank` (ascending):

```json
[
  {
    "region": "North",
    "salesperson": "Alice",
    "total_sales": 5000.50,
    "region_total": 12000.00,
    "rank": 1
  },
  ...
]
```

To complete this task:
- You must initialize a Go module in `/home/user` and get the sqlite3 driver.
- Compile and run your Go code to generate the `top_sales.json` file.
- Ensure the database index is created.