You are a data engineer tasked with building a high-performance mathematical ETL pipeline. We have a batch of unnormalized 10-dimensional vector data that needs to be standardized, processed in parallel, and bulk-loaded into a relational database for a downstream machine learning system.

Here are your instructions:

1. **Input Data**: You will find a dataset at `/home/user/raw_vectors.csv`. This file contains 10,000 rows. Each row has 10 comma-separated floating-point numbers representing a 10D vector. There is no header.

2. **Parallel Normalization**: 
   Write a Python script (e.g., `/home/user/etl.py`) that reads the CSV file and L2-normalizes each vector. 
   - The L2 norm (Euclidean length) of each vector must become exactly 1.0. 
   - Round each component of the resulting normalized vector to exactly 6 decimal places.
   - **Requirement**: You must utilize Python's `multiprocessing` or `concurrent.futures` module to process the rows in parallel across multiple CPU cores.

3. **Database Bulk Import**:
   The Python script must bulk-insert the normalized vectors into an SQLite database located at `/home/user/vectors.db`.
   - The table must be named `normalized_vectors`.
   - The table must have 10 columns named `v1`, `v2`, `v3`, `v4`, `v5`, `v6`, `v7`, `v8`, `v9`, `v10` of type `REAL`.
   - Use an efficient bulk insert method (e.g., `executemany`).

4. **Verification Export**:
   After the database is populated, write a single SQL query using the `sqlite3` command-line tool to calculate the sum of the `v1` column across all rows in the `normalized_vectors` table. Save just the numeric output to `/home/user/v1_sum.txt`.

Ensure your script handles everything from reading the CSV to creating the SQLite database and populating it.