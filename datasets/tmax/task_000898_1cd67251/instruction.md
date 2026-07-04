You are a database administrator tasked with optimizing and retrieving data from a problematic SQLite database.

We have an SQLite database located at `/app/sensor_data.db`. It contains a table named `readings` with the following schema:
`CREATE TABLE readings (id INTEGER PRIMARY KEY, sensor_id TEXT, timestamp DATETIME, value REAL, status TEXT);`

Recently, the database suffered a partial crash, and the index `idx_sensor_time` (on `sensor_id` and `timestamp`) is suspected to be corrupted, returning stale or duplicate rows during direct queries. 

Additionally, the exact filtering parameters for our daily report were lost in a system wipe, but we managed to recover a screenshot of the old reporting dashboard dashboard configuration, located at `/app/query_spec.png`.

Your task is to:
1. Analyze `/app/query_spec.png` (using OCR tools like `tesseract` which are installed) to extract the required `sensor_id`, `status` filter, sort order (by `timestamp`), and pagination limit.
2. Write a C++ application at `/home/user/query_app.cpp` that:
   - Connects to `/app/sensor_data.db` using the SQLite3 C++ API.
   - Executes a command to repair the database indexes (e.g., `REINDEX`) to ensure data consistency before querying.
   - Constructs a **parameterized query** using the parameters extracted from the image.
   - Executes the query to fetch the correct paginated results.
3. The C++ application must write the retrieved results to `/home/user/results.csv` with the header `id,value` and the corresponding rows.
4. Compile and run your C++ program. You may use `g++` and link against `libsqlite3`.

Ensure your C++ code handles errors gracefully and strictly uses parameterized queries to prevent SQL injection. The automated evaluation will check the accuracy of your retrieved IDs against the ground truth using a metric verifier.