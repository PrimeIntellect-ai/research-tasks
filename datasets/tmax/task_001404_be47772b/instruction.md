You are a Database Administrator tasked with processing a sales database and serving the results based on notes left by the lead data engineer.

There is a SQLite database located at `/app/sales.db`. It contains a table named `daily_sales` with the following schema:
`CREATE TABLE daily_sales (id INTEGER PRIMARY KEY, store_id INTEGER, date TEXT, revenue REAL);`

Your task has three parts:
1. Read the image `/app/memo.png`. It contains handwritten requirements from your lead regarding a specific analytical query, the expected result format, and the API serving details. You must use OCR (e.g., `tesseract`) or other tools to read it.
2. Execute the required SQL query against `/app/sales.db`. The query will involve window functions. Export the result in the format requested in the memo.
3. Set up a continuously running network service that serves the extracted data according to the exact protocol, port, endpoint, and authentication requirements specified in the memo.

You can use Bash, SQLite CLI, `jq`, and Python to accomplish this. Ensure the service stays running so it can be verified. Run your server in the background or in a way that it remains active.