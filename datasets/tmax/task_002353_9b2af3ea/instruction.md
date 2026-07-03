You are acting as a Database Administrator for a logistics company. We have a SQLite database located at `/home/user/logistics.db` containing unoptimized, raw data about our couriers, their deliveries, and customer reviews. 

The database has the following schema:
- `couriers` (id INTEGER PRIMARY KEY, name TEXT)
- `deliveries` (id INTEGER PRIMARY KEY, courier_id INTEGER, delivery_time_mins INTEGER, created_at DATETIME)
- `reviews` (delivery_id INTEGER PRIMARY KEY, rating INTEGER)

Your task consists of two parts:

**Part 1: Database Optimization**
Our reporting queries are currently running very slowly. Analyze the schema and the reporting requirements below, and create a SQL script at `/home/user/optimize.sql` containing the `CREATE INDEX` statements necessary to optimize joining deliveries to reviews, filtering reviews by rating, and querying deliveries by courier and creation time. 

**Part 2: Analytical Reporting**
Write a Python script at `/home/user/report.py` that connects to `/home/user/logistics.db` and executes a single, highly optimized SQL query using window functions, complex joins, and aggregations to generate our "Top 10 Couriers Report". 

The query must compute the following for every courier:
1. `recent_avg_time`: The rolling average of `delivery_time_mins` for the courier's **last 5 deliveries** (ordered by `created_at`). Use window functions to calculate this. Only the final moving average (the one calculated at their most recent delivery) should be used as their `recent_avg_time`.
2. `total_5_star_reviews`: The total number of 5-star reviews the courier has received across all time.
3. `overall_rank`: The rank of the courier based on their `recent_avg_time` (Ascending, so lower time = better rank). Use `DENSE_RANK()` for this.

Your Python script should execute this query and output the top 10 couriers (ordered by `overall_rank` ascending, then `courier_id` ascending) to a CSV file at `/home/user/metrics.csv`.

The CSV must have exactly this header:
`courier_id,courier_name,recent_avg_time,total_5_star_reviews,overall_rank`

*Note: Round `recent_avg_time` to 2 decimal places.*

Ensure your Python script runs cleanly and produces the exact output requested.