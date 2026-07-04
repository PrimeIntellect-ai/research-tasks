You are a data analyst troubleshooting a broken data pipeline. 

You have a large CSV file located at `/home/user/events.csv`. The file contains user activity logs with the following columns: `timestamp`, `user_id`, `event_type`, `payload`. 

The `payload` column contains JSON-like strings. However, due to a bug in the upstream logging system, the JSON strings often contain malformed unicode escape sequences (e.g., `\u02Z`, `\u001`) which causes standard JSON parsers like `json.loads()` to throw exceptions. 

Your task is to write a Python script that processes this CSV file and extracts the necessary information without failing on the malformed JSON.

Requirements:
1. **Streaming**: Read the CSV file line-by-line to minimize memory usage (assume the real file could be gigabytes in size).
2. **Extraction**: Use regular expressions to extract the `browser` (string) and `duration` (integer) fields from the malformed `payload` column. 
3. **Imputation**: Some payloads are missing the `duration` field entirely. For any row missing the `duration`, impute it with a default value of `30`.
4. **Aggregation**: Calculate the total session duration for each `user_id`. Also, determine the last seen `browser` for the user with the highest total session duration.
5. **Template Generation**: Identify the single `user_id` with the highest total session duration. Create an output file at `/home/user/report.txt` using exactly this template:
   `User {user_id} had the highest total duration of {total_duration} seconds. Their last recorded browser was {browser}.`

Write and execute the Python script to generate `/home/user/report.txt`.