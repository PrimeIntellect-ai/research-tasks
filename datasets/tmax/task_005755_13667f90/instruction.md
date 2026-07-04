You are a data engineer tasked with building a local ETL pipeline that processes relational communication data, projects it into a directed graph, and exports network metrics.

We have a SQLite database located at `/home/user/company_data.db`. It contains two tables:
1. `users`: `id` (INTEGER), `name` (TEXT), `department` (TEXT)
2. `messages`: `id` (INTEGER), `sender_id` (INTEGER), `receiver_id` (INTEGER), `sent_at` (TEXT in YYYY-MM-DD format)

Your task is to write a Python script at `/home/user/etl_graph.py` that performs the following:
1. **Parameterized Query Construction:** The script must accept four command-line arguments using the `argparse` module:
   - `--db`: Path to the SQLite database.
   - `--start-date`: The start date (inclusive) in YYYY-MM-DD format.
   - `--end-date`: The end date (inclusive) in YYYY-MM-DD format.
   - `--output`: Path to the output JSON file.
   It must use parameterized SQL queries (e.g., using `?` placeholders) to extract records to prevent SQL injection and properly handle the date filtering.

2. **Graph Projection:** From the filtered `messages` table, project the data into a directed unweighted graph. 
   - Nodes represent users.
   - A directed edge exists from User A to User B if User A sent *at least one* message to User B within the specified date range. Multiple messages between the same users do not increase the edge weight (unweighted).

3. **Materialization & Export:** Calculate the "in-degree" for each user in the projected graph (the number of unique users who sent them a message in the time period).
   - Export the results to the path specified by `--output` as a JSON array of objects.
   - Only include users who have an in-degree > 0.
   - Each object must have the keys: `"user_id"` (int), `"name"` (string), and `"in_degree"` (int).
   - The JSON array must be sorted by `in_degree` in descending order. If there is a tie, sort by `user_id` in ascending order.
   - Format the JSON with an indentation of 2 spaces.

Example expected invocation (you don't need to run it, our test suite will):
`python3 /home/user/etl_graph.py --db /home/user/company_data.db --start-date 2023-01-01 --end-date 2023-03-31 --output /home/user/report.json`

Ensure your script is executable and robust. Only use Python's standard library (e.g., `sqlite3`, `json`, `argparse`).