You are a data analyst tasked with processing a daily retail export file using C and SQLite. 

There is an input file located at `/home/user/data.csv`. It contains four columns with a header row:
`date` (string), `store_id` (integer), `revenue` (float), and `visitors` (integer).

Your task is to:
1. Write a C program at `/home/user/process.c` and compile it to `/home/user/process`.
2. The program must read `/home/user/data.csv` and calculate summary statistics grouped by `store_id`. For each `store_id`, calculate:
   - Total revenue (sum of revenue)
   - Total visitors (sum of visitors)
   - Maximum daily revenue
3. The program must write these summary statistics to `/home/user/summary.csv`. The output file must NOT have a header row. The columns must be `store_id,total_revenue,total_visitors,max_revenue`. Format floating-point numbers to exactly 2 decimal places. Sort the output in ascending order by `store_id`.
4. The C program must implement pipeline logging by appending exactly these three lines to `/home/user/pipeline.log`:
   - `[INFO] Starting processing`
   - `[INFO] Processed <N> rows` (where <N> is the number of data rows processed, excluding the header)
   - `[INFO] Output written to summary.csv`
5. After creating the summary CSV, use the `sqlite3` command-line tool to create a database at `/home/user/analytics.db`.
6. Inside the SQLite database, create a table named `store_stats` with the schema: `store_id INTEGER, total_revenue REAL, total_visitors INTEGER, max_revenue REAL`.
7. Bulk import the `/home/user/summary.csv` file into the `store_stats` table.

Do not use third-party CSV parsing libraries in C; standard library string manipulation (`strtok`, `sscanf`, etc.) is sufficient for this simple format.