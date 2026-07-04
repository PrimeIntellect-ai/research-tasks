You are a data analyst investigating a financial network. We have a multi-service pipeline set up in `/app/` that includes:
- PostgreSQL (port 5432): Stores the base graph of user accounts and historical transactions.
- Redis (port 6379): Caches risk scores.
- Flask API (port 5000): Provides real-time entity verification and risk scoring via `http://127.0.0.1:5000/score/<account_id>`.

A junior analyst wrote a Python script at `/home/user/detector.py` to filter incoming daily transaction CSVs. It is supposed to identify and reject "suspicious" transactions based on the following criteria:
1. The transaction is part of a circular transfer path (A -> B -> C -> A) of length up to 4 accounts, found via a recursive CTE in PostgreSQL.
2. The sender's 7-day moving average transaction volume exceeds 10,000, calculated using SQL window functions.
3. The sender's risk score from the Flask API is > 0.8.

However, the current `detector.py` script contains a severe bug: the recursive CTE in the SQL query has an implicit cross join, causing it to return massive amounts of incorrect paths, misclassifying valid transactions, and occasionally timing out. It also fails to cache the Flask API responses in Redis, overwhelming the API.

Your task:
1. Start the services using the provided `/app/start_services.sh` script.
2. Fix `/home/user/detector.py` so that it correctly implements the graph traversal without cross joins, correctly computes the window function, and properly utilizes Redis caching for the Flask API.
3. The script must be invoked as: `python /home/user/detector.py <input_csv_path> <output_csv_path>`. It should read the input CSV, filter OUT (reject) any transaction that meets the suspicious criteria, and write the remaining (clean) transactions to the output CSV.

We will test your `detector.py` against two directories of CSV files:
- `/home/user/corpora/clean/`: Contains normal, legitimate transactions. Your script must preserve 100% of these in the output.
- `/home/user/corpora/evil/`: Contains known money-laundering patterns. Your script must filter out (reject) 100% of these transactions.