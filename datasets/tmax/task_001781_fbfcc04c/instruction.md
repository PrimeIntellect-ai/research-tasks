You are a data analyst tasked with analyzing a CSV file containing transaction logs. The system is experiencing locking issues, and we suspect that high peak concurrency on specific resources is the root cause. 

Your task is to calculate the maximum number of concurrently active transactions for each resource using SQLite.

You have been provided with a CSV file at `/home/user/transactions.csv` containing the following headers:
`tx_id`, `resource_id`, `start_ts`, `end_ts`
(Timestamps are integer Unix epochs).

Perform the following steps:
1. Create a new SQLite database at `/home/user/analysis.db`.
2. Import the `transactions.csv` file into a table named `transactions`.
3. Design and create one or more database indexes to optimize queries filtering or grouping by resource and temporal bounds. Save the exact SQL `CREATE INDEX` statements you use into a file named `/home/user/indexes.sql`.
4. Using a single SQL query (which may include CTEs and Window Functions), calculate the peak (maximum) number of concurrently active transactions for each `resource_id`. A transaction is considered active from `start_ts` to `end_ts` inclusive. If one transaction ends at the exact same timestamp another begins, they are considered concurrent at that timestamp.
5. Export the results of your query to a CSV file at `/home/user/peak_concurrency.csv`. The file should have no headers, and the columns must be `resource_id` and `max_concurrent`. The results must be sorted by `resource_id` in ascending order.

Use standard Linux CLI tools (like `sqlite3`, `bash`, `cat`) to complete this task.