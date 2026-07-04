You are a data engineer tasked with building a robust ETL pipeline in Rust. We have an SQLite database at `/home/user/data.db` containing two tables:

1. `users` 
   - `user_id` (INTEGER)
   - `username` (TEXT)
2. `events`
   - `event_id` (INTEGER)
   - `user_id` (INTEGER)
   - `event_date` (TEXT, format 'YYYY-MM-DD')
   - `score` (REAL)
   - `comment` (TEXT)

Note: Some of the `comment` fields contain embedded newlines, which have historically broken our naive shell-script exports.

Your objective is to write and execute a Rust application that acts as an ETL pipeline to do the following:
1. Extract the data from the `users` and `events` tables.
2. Join the events with their corresponding user information.
3. For each user, compute a 3-event rolling average of the `score`, ordered by `event_date` ascending. 
   - The rolling average for a given event should be the mean of the current event's score and up to two immediately preceding events for that same user. 
   - If a user has fewer than 3 events up to that point, average the available events (e.g., the first event's rolling average is just its own score).
4. Load the transformed data back into `/home/user/data.db` into a new table named `rolling_stats` with the following schema:
   - `user_id` (INTEGER)
   - `username` (TEXT)
   - `event_date` (TEXT)
   - `rolling_avg` (REAL) - Rounded to exactly 2 decimal places.

Requirements:
- Create your Rust project in `/home/user/etl`.
- You may use crates like `rusqlite` to directly read/write the database, or export to CSV using `sqlite3`, process with the `csv` crate, and bulk import back. The choice is yours, provided embedded newlines in `comment` do not corrupt the join or ordering.
- Do not modify the existing tables.

Once your Rust program finishes executing and the `rolling_stats` table is successfully populated, exit.