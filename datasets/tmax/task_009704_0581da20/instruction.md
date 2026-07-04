You are an automation specialist tasked with fixing and formalizing a mathematical ETL pipeline. We have a daily data dump of vector coefficients, but our upstream provider occasionally retries failed jobs, resulting in massive duplication. 

Your goal is to build an idempotent Python ETL script that reads a large file of vector data, mathematically deduplicates it, sorts it, and loads it into a database, then schedule this job.

**Step 1: The ETL Script**
Create a Python script at `/home/user/run_etl.py`.
The script must process the input file located at `/home/user/raw_vectors.csv`. 
The CSV file has no header. Each row has 11 columns: 
`record_id, c0, c1, c2, c3, c4, c5, c6, c7, c8, c9`
Where `record_id` is an integer, and `c0` through `c9` are integer coefficients of a polynomial.

For each row, you must compute a Mathematical Hash $H$:
$H = \left( \sum_{i=0}^{9} c_i \cdot 31^i \right) \pmod{1000000007}$

**Requirements for the pipeline:**
1. **Streaming & Processing:** Read the CSV efficiently. 
2. **Hash-based Deduplication:** Multiple rows might evaluate to the same hash $H$. You must deduplicate these. If a hash collision occurs, keep ONLY the record with the *smallest* `record_id`.
3. **Large-scale Sorting:** Sort the uniquely identified records by their hash $H$ in *descending* order.
4. **Database Bulk Export:** Insert the sorted, deduplicated records into a new SQLite database at `/home/user/etl_result.db`.
   - Table name: `processed_vectors`
   - Schema: `id INTEGER PRIMARY KEY, poly_hash INTEGER, coefficients TEXT`
   - `id` is the `record_id`.
   - `poly_hash` is your computed $H$.
   - `coefficients` is a single string of the coefficients joined by commas (e.g., `"1,2,3,4,5,6,7,8,9,10"`).

**Step 2: Execution and Scheduling**
1. Run your script once so that `/home/user/etl_result.db` is populated.
2. We need this pipeline to run automatically. Add a cron job for the current user that executes `/home/user/run_etl.py` using python3 exactly every 15 minutes (e.g., 0, 15, 30, 45 past the hour). 
3. Dump your installed crontab to `/home/user/crontab_backup.txt` (e.g., using `crontab -l`).

Ensure your code handles the required math correctly and securely closes database connections.