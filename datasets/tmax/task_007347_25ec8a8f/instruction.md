You are a data analyst working with a system that processes event logs. You have been given a Go script that ingests CSV data containing JSON payloads into a local SQLite database (`/home/user/events.db`). 

However, the ingestion script (`/home/user/process.go`) is currently failing. It attempts to insert data concurrently into two tables (`users` and `events`) but suffers from a classic transaction deadlock ("database is locked") because different goroutines acquire table locks in conflicting orders.

Your objectives:
1. **Fix the Deadlock:** Modify `/home/user/process.go` to resolve the concurrent transaction deadlock so that all records from `/home/user/data.csv` are successfully inserted into `/home/user/events.db` without errors. Run the script to populate the database.
2. **Perform Document-Style Aggregation:** Write a new Go script at `/home/user/aggregate.go` that queries the SQLite database. Using SQLite's built-in JSON functions (treating the `payload` column as a NoSQL document), calculate the total `duration` of events for each `user_id`. 
3. **Format Output:** Your `aggregate.go` script must execute the query and save the aggregated results as a JSON array to `/home/user/output.json`. Each object in the array should have `"user_id"` (integer) and `"total_duration"` (integer), sorted by `total_duration` in descending order.
4. **Query Optimization:** To optimize the aggregation, create an index on the `user_id` column in the `events` table. Then, execute an `EXPLAIN QUERY PLAN` for your aggregation query and save the raw console output of the plan to `/home/user/plan.txt`.

Ensure your Go scripts compile and run cleanly, and the final output files (`output.json` and `plan.txt`) are correctly formatted.