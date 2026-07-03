You are a data engineer building an ETL pipeline to process and aggregate gaming telemetry data. You need to combine document-oriented event logs with relational user profiles.

Your environment contains the following input data:
1. `/home/user/data/events.jsonl`: A JSON-lines file representing a NoSQL export of game events. Each line is a JSON object with keys: `user_id` (string), `event_type` (string), and `score` (integer). There may be multiple lines per user.
2. `/home/user/data/users.db`: An SQLite database containing a table `users` with schema `(user_id TEXT PRIMARY KEY, region TEXT)`.

Your task is to write and execute a Python script (`/home/user/etl_pipeline.py`) that performs the following steps:

1. **NoSQL Aggregation Simulation:** Parse `/home/user/data/events.jsonl`. For each unique `user_id`, find all events where `event_type` is `"level_complete"`. Sort these scores in descending order and keep ONLY the top 3 highest scores per user (if a user has fewer than 3, keep all of them). Sum these top scores to calculate the `user_top3_score`.
2. **Relational Join & Analytical Window Functions:** Load this aggregated score data into the SQLite database `/home/user/data/users.db` (e.g., as a temporary table) and join it with the `users` table.
3. **Cross-Query Summarization:** Using SQL Window Functions, compute:
    - `region_rank`: The rank of the user within their region based on their `user_top3_score` (1 being the highest score in that region). Use standard `RANK()` function.
    - `region_total_score`: The sum of the `user_top3_score` for ALL users within that specific region.
4. **Data Export:** 
    - Create the directory `/home/user/output/` if it does not exist.
    - Export the final joined and ranked dataset to `/home/user/output/region_leaderboard.csv`. The CSV must have exactly these columns in order: `region`, `user_id`, `user_top3_score`, `region_rank`, `region_total_score`. Order the rows alphabetically by `region` (ASC), then by `region_rank` (ASC).
    - Create a summary JSON file at `/home/user/output/etl_summary.json` containing exactly this structure:
      `{"total_users_processed": X, "top_region": "REGION_NAME", "top_region_score": Y}`
      *(Where total_users_processed is the count of unique users who had at least one "level_complete" event, and top_region is the region string with the highest `region_total_score`).*

Do not use external data processing libraries like Pandas; standard Python libraries (`sqlite3`, `json`, `csv`, etc.) are fully sufficient and expected.