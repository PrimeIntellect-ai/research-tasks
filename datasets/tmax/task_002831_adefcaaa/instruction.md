You are acting as a technical assistant to a compliance officer. We are auditing our internal systems to find unauthorized resource access. 

We have a SQLite database located at `/home/user/audit.db` containing three tables:
1. `users` (`user_id` TEXT, `dept_id` TEXT)
2. `permissions` (`dept_id` TEXT, `resource_id` TEXT) - Maps departments to the resources they are allowed to access.
3. `access_logs` (`user_id` TEXT, `resource_id` TEXT) - Logs of actual resources accessed by users.

I wrote a Python script at `/home/user/generate_report.py` that is supposed to find unauthorized access events (where a user accessed a resource not explicitly permitted for their department). However, the script is currently returning wildly incorrect results and huge numbers of false positives due to a bad SQL query that performs an implicit cross join.

Your task is to:
1. Fix the SQL query in `/home/user/generate_report.py` to correctly identify *only* unauthorized access events.
2. The script must project these violations into a graph edge list and export it to a CSV file at `/home/user/unauthorized_edges.csv`. The CSV should have a header row `user_id,resource_id` and contain the unauthorized access pairs. Sort the output alphabetically by `user_id`, then `resource_id`.
3. The script must also aggregate the data to calculate the total number of unauthorized access events per department, and export this summary as a JSON object to `/home/user/dept_summary.json` (e.g., `{"Engineering": 5, "HR": 2}`).

Please correct the Python script and run it so that the two output files are generated correctly.