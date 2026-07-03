You are acting as a compliance officer auditing an internal system for potential data exfiltration. 
You have been provided with an SQLite database at `/home/user/audit.db` containing two tables:

1. `system_graph` (columns: `source`, `target`, `relation`) - Represents the system architecture as a directed graph. Sources and targets can be users, microservices, or databases.
2. `access_logs` (columns: `log_id`, `user_id`, `resource`, `timestamp`, `details_json`) - Contains access logs. `timestamp` is an integer UNIX epoch. `details_json` is a JSON string containing metadata like the access status.

Your task is to identify anomalous access patterns based on the following compliance rules:
1. **Knowledge Graph Pattern:** Find all users (nodes) that have a path of length EXACTLY 2 (i.e., User -> Service -> Resource) to the target node `'Customer_Data'`.
2. **NoSQL-style Filtering & Windowed Aggregation:** For these specific users, analyze their access to the `'Customer_Data'` resource. 
   - Only consider logs where the JSON extracted from `details_json` has `"status": "SUCCESS"`.
   - Calculate a rolling count of these successful accesses using a window function. The window should evaluate the number of accesses within a rolling 3600-second (1 hour) timeframe for each user.
3. **Flagging:** A user is flagged if their rolling count of successful accesses to `'Customer_Data'` exceeds 3 within any 3600-second window.

Write and execute a Python script to perform this query. Extract the distinct `user_id`s of all flagged users.
Output the flagged user IDs in alphabetical order, one per line, to the file `/home/user/flagged.txt`.