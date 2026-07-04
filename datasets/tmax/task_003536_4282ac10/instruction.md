You are a database administrator tasked with optimizing a data pipeline. A junior developer recently left the company, leaving behind an undocumented SQLite database at `/home/user/analytics.db`. They also left a requirement to build a reporting tool, but no code.

Your task is to reverse-engineer the database schema and write a script to generate a parameterized summary report. You can use any programming language (e.g., Python, Node.js, Bash with `sqlite3` CLI) to accomplish this.

Requirements:
1. Create an executable script located at `/home/user/generate_report.sh` (or `.py`, `.js`, etc., but you must create a wrapper script `/home/user/generate_report.sh` that we can execute).
2. The script must accept exactly three command-line arguments in this order:
   - `ORDER_STATUS` (string, e.g., 'completed' or 'refunded')
   - `MIN_INTERACTION_DURATION` (integer, e.g., 30)
   - `OUTPUT_JSON_PATH` (string, the file path where the output should be saved)
3. The script must connect to `/home/user/analytics.db` and securely construct a parameterized query (to prevent SQL injection) using the provided command-line arguments.
4. The output must aggregate data across the different undocumented tables to compute the following for every customer:
   - `customer_name`: The full name of the customer.
   - `total_spent`: The sum of all order amounts for this customer where the order status matches the `ORDER_STATUS` parameter. If no orders match, this should be `0`.
   - `total_interaction_time`: The sum of all interaction durations (in seconds) for this customer where the interaction duration is greater than or equal to `MIN_INTERACTION_DURATION`. If no interactions match, this should be `0`.
5. The output must be written to the `OUTPUT_JSON_PATH` as a perfectly valid JSON array of objects. 
6. The JSON array must be sorted by `total_spent` in descending order. If there is a tie, sort by `customer_name` in alphabetical order.
7. Only include customers who have at least one recorded interaction (regardless of duration) OR at least one recorded order (regardless of status).

Example execution:
`/bin/bash /home/user/generate_report.sh "completed" 60 /home/user/report.json`

Ensure your script handles parameterized queries correctly and performs the aggregations efficiently using SQL joins and group by clauses (rather than fetching all rows into memory).