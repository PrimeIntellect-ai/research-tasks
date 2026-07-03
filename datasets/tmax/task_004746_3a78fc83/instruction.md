You are a data engineer building an ETL pipeline. You need to write a Go program that extracts hierarchical department data from a relational database, joins it with a NoSQL-style JSON dump of sales transactions, and computes aggregated metrics.

Your Go program must be saved to `/home/user/etl.go` and when executed, it should produce a summary JSON file at `/home/user/summary.json`.

**Data Sources:**
1. **SQLite Database:** `/home/user/data.db`
   - Table: `departments(id INTEGER, parent_id INTEGER, name TEXT, is_active INTEGER)`
   - Contains a hierarchical tree of departments. `parent_id` is NULL for root departments.
   - *Warning:* The database has a corrupted index named `idx_active` on the `is_active` column, which occasionally returns stale or deleted rows in production. To ensure data integrity, your Go script **must** execute a `DROP INDEX IF EXISTS idx_active;` statement before querying the `departments` table.

2. **Sales Transactions:** `/home/user/sales.json`
   - A JSON array of transaction objects.
   - Format: `[{"tx_id": "...", "dept_id": INT, "items": [{"price": INT}, ...]}, ...]`

**Business Logic:**
1. **Hierarchy & Filtering:** Retrieve all departments. A department should be processed only if `is_active = 1`. Furthermore, if a department is inactive, all of its nested sub-departments must also be ignored entirely, regardless of their own `is_active` status.
2. **Aggregation:** Calculate the total sales for each valid department. A department's total sales is the sum of the `price` of all items in transactions mapped to that `dept_id`, **plus** the total sales of all its valid recursive sub-departments.
3. **Output:** Write the results to `/home/user/summary.json` as a JSON array of objects with the keys `dept_id` and `total_sales`.
   - Only include valid (active and not descendants of inactive) departments in the output.
   - The array must be sorted by `dept_id` in ascending order.
   - Format example: `[{"dept_id": 1, "total_sales": 500}, {"dept_id": 2, "total_sales": 200}]`

**Constraints & Notes:**
- You may install external Go packages if needed (e.g., `github.com/mattn/go-sqlite3`), but ensure your environment is properly initialized (`go mod init`, `go get`, etc.).
- The output JSON file must be strictly formatted as described for automated verification.