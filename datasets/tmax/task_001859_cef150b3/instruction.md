You are a data analyst for a retail company. You have been given a compressed data dump located at `/home/user/remote_dump.tar.gz`. This archive contains a single file: `transactions.csv`.

Previous attempts to process this file with simple shell scripts failed because the `description` column contains embedded newline characters, causing rows to be silently split or dropped. 

Your task is to build a Python-based data processing pipeline that correctly handles the embedded newlines, computes mathematical aggregates, and exports the results to a database.

Perform the following steps:
1. Extract `transactions.csv` from `/home/user/remote_dump.tar.gz`.
2. Write a Python script to parse `transactions.csv` accurately. The CSV has the following headers: `transaction_id`, `category`, `price`, `volume`, `description`.
3. For each `category`, calculate the following metrics:
   - `total_volume`: The sum of the `volume`.
   - `total_value`: The sum of (`price` * `volume`) for all transactions in the category.
   - `vwap` (Volume-Weighted Average Price): `total_value` divided by `total_volume`.
4. Round both `total_value` and `vwap` to exactly 2 decimal places.
5. Sort the grouped results in descending order by `total_value`. If there is a tie, sort by `category` ascending alphabetically.
6. Save the aggregated and sorted data into a local SQLite database located at `/home/user/metrics.db`.
   - The table must be named `category_metrics`.
   - The columns must be exactly: `category` (TEXT), `total_volume` (INTEGER), `total_value` (REAL), `vwap` (REAL).
7. Finally, use the SQLite command-line tool to perform a bulk export of the entire `metrics.db` database into a SQL text file located at `/home/user/export.sql`.

Ensure all file paths are exact and the final SQL export file contains the standard SQLite dump output.