You are an expert data analyst and database engineer. We have a set of raw data in CSV format, and a preliminary database setup that is currently failing due to concurrent transaction deadlocks and extreme slowness. 

Your objectives are:
1. **Analyze the specifications:** Read the image at `/app/system_design.png`. It contains handwritten notes from the senior engineer regarding the necessary indexing strategy, connection PRAGMAs (to resolve the deadlock/locking issues), and the target performance metric. Tesseract OCR is installed if you need it.
2. **Setup the Database:** We have a large CSV file at `/home/user/raw_data/orders.csv` (which you will need to generate a sample of for testing, assume it has columns: `order_id` (TEXT), `customer_id` (TEXT), `amount` (REAL), `order_date` (TEXT)). Create an SQLite database at `/home/user/analytics.db` and load this data.
3. **Implement the Fixes:** 
    - Apply the exact index strategy detailed in the image.
    - Configure the SQLite connection parameters to eliminate the "database is locked" errors caused by concurrent readers and writers (as hinted in the image).
4. **Implement the Data API:** Write a Python module `/home/user/query_api.py` with a function `get_customer_summary(db_path, customer_id, page, page_size)`.
    - This function must use **parameterized queries** to prevent injection and improve query plan caching.
    - It should perform a cross-query aggregation: returning a dictionary containing `{"total_orders": X, "total_spent": Y, "recent_orders": [list of order_id sorted by order_date DESC limited by pagination]}`.
    - Ensure correct result sorting, pagination (using `page` and `page_size`), and filtering.
5. **Generate the Metric Benchmark:** Write a script `/home/user/benchmark.py` that spins up 4 concurrent processes (using `multiprocessing`), each making 500 random calls to `get_customer_summary` while another process continuously inserts new rows. Measure the total time taken by the reader processes and save this execution time as a simple float in `/home/user/execution_time.txt`.

Our automated test suite will import your `query_api.py`, run a strict performance benchmark under high concurrency, and evaluate the execution time.