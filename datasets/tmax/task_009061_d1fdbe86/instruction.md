You are a Data Engineer building an ETL pipeline to analyze e-commerce telemetry. 

You have two disparate data sources located in your environment:
1. **Relational Database**: An SQLite database at `/home/user/data/users.db`. It contains a table named `users` with the schema: `(id INTEGER PRIMARY KEY, name TEXT, country TEXT, age INTEGER, status TEXT)`.
2. **Document Data (NoSQL pattern)**: A directory at `/home/user/data/events/` containing multiple JSON files. Each file represents a user session and contains nested event arrays. Example format:
```json
{
  "session_id": "sess_001",
  "user_id": 105,
  "events": [
    {"type": "pageview", "timestamp": "2023-10-01T10:00:00Z"},
    {"type": "purchase", "amount": 120.50, "currency": "USD"}
  ]
}
```

**Your Objective:**
Write and execute a Python script at `/home/user/etl_pipeline.py` that performs the following steps:
1. Parse the JSON session files and extract all `purchase` events.
2. Calculate the total purchase amount for each `user_id` across all their sessions. (Some users may have multiple sessions, and some sessions may have multiple purchases. Sum them all).
3. Query the `users.db` database to join these purchase totals with user demographics.
4. **Filter** out any users whose `status` is not exactly `'active'`.
5. **Aggregate** the data into cohorts based on `country` and `age_group`. The age groups must be strictly defined as:
   - `'18-25'` (18 to 25 inclusive)
   - `'26-35'` (26 to 35 inclusive)
   - `'36-50'` (36 to 50 inclusive)
   - `'51+'` (51 and above)
6. For each cohort, calculate the **average total spend** (the sum of total spends of active users in the cohort divided by the number of active users in that cohort who made at least one purchase). Round the average to 2 decimal places.
7. **Sort** the cohorts descending by the average total spend, and then alphabetically by country in case of a tie.
8. Apply **pagination/limiting** to output only the **top 3** cohorts.
9. Save the final result to `/home/user/cohort_report.json` as a JSON array of objects with the following exact keys: `country`, `age_group`, `avg_spend`.

Ensure you run your script and successfully generate the `/home/user/cohort_report.json` file.