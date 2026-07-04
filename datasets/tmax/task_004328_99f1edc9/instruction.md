You are a Database Administrator working on query optimization. The development team has provided you with a NoSQL dump of database access events in JSON Lines format, located at `/home/user/events.jsonl`. 

Your task is to write a script (in the language of your choice) that mimics a NoSQL aggregation pipeline to process this data, chain the results, and export them into a specific CSV format for the analytics team.

Here is what your aggregation pipeline must accomplish:
1. **Match (Filter):** Keep only the records where `event_type` is strictly `"query"` and the nested field `metadata.status` is strictly `"success"`.
2. **Group:** Group the filtered records by `user_id`.
3. **Aggregate:** For each user, calculate:
   - The total number of successful queries (`query_count`).
   - The average of the `metadata.duration` values (`avg_duration_ms`).
4. **Sort:** Sort the final aggregated data in descending order of `avg_duration_ms`. If there is a tie in the average duration, sort by `user_id` in ascending order.
5. **Export:** Write the results to a CSV file located at `/home/user/report.csv`.

**Formatting Requirements for `/home/user/report.csv`:**
- The first line must be exactly the header: `user_id,query_count,avg_duration_ms`
- The `avg_duration_ms` must be rounded to exactly two decimal places (e.g., `45.00`, `12.34`).
- No trailing commas or extra whitespace.

Complete this task by writing and running the necessary code to produce the final CSV file.