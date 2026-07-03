You are a data engineer debugging an ETL pipeline. You have been given two data sources:
1. An SQLite database `/home/user/users.db` containing a `users` table.
2. A NoSQL-style JSON lines dump of event streams in `/home/user/events.jsonl`.

The existing pipeline in the database has a corrupted index that has been returning stale rows, so we are bypassing the database for event aggregations and using the raw JSONL dump instead.

Your task is to write a Python script at `/home/user/etl.py` that performs the following analytical aggregation:
1. Reverse engineer the `users` table schema in `/home/user/users.db` to identify active users (there is a boolean/integer column indicating if they are active).
2. Read the `events.jsonl` file. Each line is a JSON object representing an event.
3. For **active users only**, calculate a rolling 2-event sum of `points` ordered by `timestamp` (i.e., the sum of points from the current event and the immediately preceding event for that user). If a user has only 1 event, the rolling sum is just the points of that single event.
4. Find the maximum rolling 2-event sum for each active user.
5. Output the results as a JSON object mapping the user ID (as a string) to their maximum rolling sum (as an integer). Save this JSON file to `/home/user/max_rolling.json`.

Ensure your Python script correctly handles missing previous events (window size of up to 2) and correctly filters out inactive users. Run your script to produce the final `max_rolling.json` file.