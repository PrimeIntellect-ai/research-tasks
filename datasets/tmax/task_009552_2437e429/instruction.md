You are acting as a Database Administrator and Python developer. We have an SQLite database located at `/home/user/analytics.db` containing usage data for a multi-tenant SaaS application. 

The database has the following schema:
- `users` (`id` INTEGER PRIMARY KEY, `tenant_id` TEXT, `name` TEXT, `created_at` TEXT)
- `sessions` (`id` INTEGER PRIMARY KEY, `user_id` INTEGER, `start_time` TEXT, `end_time` TEXT, `device_type` TEXT)
- `events` (`id` INTEGER PRIMARY KEY, `session_id` INTEGER, `event_type` TEXT, `timestamp` TEXT, `value` REAL)

Currently, our reporting is incredibly slow because the database lacks appropriate indexes, and our old scripts used inefficient N+1 queries.

Your task is to optimize this reporting process by doing the following:

1. Create a SQL file at `/home/user/optimize.sql` containing the optimal `CREATE INDEX` statements to speed up queries filtering by `tenant_id` on users, `device_type` on sessions, and `event_type` on events.
2. Apply these indexes to `/home/user/analytics.db`.
3. Write a Python script at `/home/user/fast_report.py` that accepts a `--tenant` command-line argument.
4. Inside `fast_report.py`, write a single, efficient, properly parameterized SQL query (using complex joins and aggregation) to find the top 5 users for the given tenant based on their total 'purchase' value exclusively from 'mobile' sessions. 
5. The query must calculate the sum of `events.value` where `events.event_type = 'purchase'` and `sessions.device_type = 'mobile'`. Order the results by the total purchase value in descending order, using the user's `name` in ascending order as a tie-breaker.
6. The script should execute this query and output the results as a JSON array to `/home/user/report_output.json`.

The JSON format must be exactly:
```json
[
  {
    "user_id": 123,
    "name": "Alice Smith",
    "total_purchase_value": 450.75
  },
  ...
]
```

To complete the task, run your script for `tenant_42`:
`python3 /home/user/fast_report.py --tenant tenant_42`

Ensure the JSON file is generated successfully at `/home/user/report_output.json`.