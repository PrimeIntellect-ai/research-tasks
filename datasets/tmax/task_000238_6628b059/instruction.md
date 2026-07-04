I am a compliance officer auditing a legacy system, and I've been given a bare SQLite database file at `/home/user/compliance.db`. Unfortunately, the original developers left no documentation about the schema or table names. 

We suspect some users are attempting to structure large transactions to avoid detection. I need you to build a Python data pipeline to flag these users.

Please do the following:
1. Explore the database at `/home/user/compliance.db` to discover the table containing transaction logs and figure out its schema. There is only one relevant table containing user IDs, transaction amounts, and timestamps.
2. Write a Python script at `/home/user/audit_pipeline.py` that queries this database.
3. Your query must use SQL window functions to find any user who has a rolling sum of transaction amounts exceeding 50,000 across *any 3 consecutive transactions* (ordered by timestamp).
4. The Python script should execute this query and output the unique list of flagged user IDs to `/home/user/suspicious_users.json`. 

The output JSON file must strictly follow this exact format:
```json
{
  "flagged_users": [
    "user_1",
    "user_2"
  ]
}
```
The list of user IDs must be sorted in ascending alphabetical order. Do not hardcode the expected users in your script; your Python script must run the SQL query dynamically and output the JSON.