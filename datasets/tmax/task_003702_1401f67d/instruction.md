You are acting as a log analyst investigating patterns in our application's web traffic. We have a set of raw, semi-structured session logs in a wide JSON format, but we need to normalize, flatten, anonymize, and export them to a structured CSV format for our analytics team.

Your task is to write and execute a Rust program that performs this ETL process. 

**Input Data:**
A file exists at `/home/user/raw_logs.json` containing an array of session objects. Each session object has:
- `session_id` (string)
- `client_ip` (string, IPv4)
- `user_id` (string)
- `events` (array of objects), where each event contains:
  - `timestamp` (string, ISO-8601)
  - `event_type` (string)
  - `request` (string, e.g., "GET /api/v1/users/123/profile HTTP/1.1")

**Processing Requirements:**
Create a Rust project in `/home/user/log_processor` to process this file with the following steps:
1. **Wide-to-Long Reshaping:** Flatten the data so that each individual event in the `events` array becomes its own row. Each event row must inherit the `client_ip` and `user_id` from its parent session.
2. **Tokenization and Normalization:** Parse the `request` string from each event to extract the HTTP method and the URL path. Normalize the URL path by replacing any numeric segments with the literal string `{id}`. For example, `"GET /api/v1/users/123/profile HTTP/1.1"` becomes method `"GET"` and normalized path `"/api/v1/users/{id}/profile"`. If the request string is empty or invalid, use `"UNKNOWN"` for both.
3. **Data Masking and Anonymization:** 
   - Mask the `client_ip` by replacing the last octet with `0` (e.g., `192.168.1.45` -> `192.168.1.0`).
   - Anonymize the `user_id` by hashing it using SHA-256 and storing the lower-case hex digest.
4. **Output Generation:** Write the processed records to a CSV file at `/home/user/processed_logs.csv`. 

**Output Format:**
The CSV file must have the following headers (in exactly this order):
`timestamp,event_type,method,normalized_path,masked_ip,anonymized_user_id`

Sort the final CSV rows in ascending order by `timestamp`.

Once your Rust program is written, compile and run it to produce `/home/user/processed_logs.csv`.