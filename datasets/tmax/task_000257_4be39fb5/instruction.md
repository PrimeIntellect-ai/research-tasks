You are a data engineer tasked with building the extraction and transformation step of an ETL pipeline. 

You have been given a legacy SQLite database at `/home/user/telemetry.db`. Unfortunately, there is no documentation for the schema. 

Your task is to:
1. Explore the database to understand its structure. You will find a table containing user activity logs.
2. Write a Python script at `/home/user/process_etl.py` that connects to this database and extracts specific analytical metrics.
3. For every event where the event type is `'checkout'`, calculate the number of seconds since that *same user's* immediately preceding event (of any type). If the checkout is the user's first ever event, the value should be `null`. You must use SQL Window functions for this calculation.
4. The output must be written to a JSON Lines file at `/home/user/transformed_events.jsonl`. 
5. Before writing a record to the output file, your Python script must validate the dictionary against the JSON schema provided at `/home/user/schema.json`. You should use the `jsonschema` Python library to accomplish this. Discard any records that fail validation.

The output JSON object for each row must have the following exact keys (which match the schema):
- `user_id` (integer)
- `event_id` (integer)
- `timestamp` (string, ISO-8601 format as found in the DB)
- `seconds_since_last_event` (integer or null)

Ensure your script runs successfully and generates `/home/user/transformed_events.jsonl` correctly.