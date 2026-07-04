You are a data analyst working with network topology data. You have been given two CSV files representing a network of routers and the latency of links between them.

The files are located at:
1. `/home/user/data/routers.csv` - Contains columns: `router_id`, `properties`
   The `properties` column contains a JSON string with metadata about the router, for example: `{"region": "US-East", "active": true, "capacity": 100}`
2. `/home/user/data/links.csv` - Contains columns: `source`, `target`, `latency_ms`

Your task is to write a Python script at `/home/user/analyze.py` that does the following:
1. Maps this CSV data into an in-memory SQLite database.
2. Uses parameterized SQLite queries with JSON extraction functions (simulating NoSQL document querying) to find all "valid" routers. A valid router is defined as having `"active": true` and a `"capacity"` greater than or equal to 50.
3. Builds an undirected graph using the `networkx` library (you may install it using `pip install --user networkx` if it's not installed) containing ONLY the valid routers. If a link in `links.csv` connects to a router that is invalid or missing, that link must be ignored.
4. Computes the shortest path (based on `latency_ms` as the weight) between router `"R1"` and router `"R15"`.
5. Writes the total latency of this shortest path into a file located at `/home/user/answer.txt` in the exact format: `Total Latency: <integer>`

Requirements:
- Ensure your Python script runs without errors and produces the `answer.txt` file.
- Do not hardcode the expected answer; your script must compute it dynamically from the CSV files.