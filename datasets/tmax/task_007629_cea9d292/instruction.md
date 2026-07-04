You are a data analyst working for a logistics company. You have been given two CSV files detailing the company's warehouse network and transportation routes. Your task is to analyze these files using Python to determine the best warehouses to send excess stock to, based on available capacity and transit time.

The files are located at:
1. `/home/user/warehouses.csv`: Contains columns `warehouse_id`, `capacity`, and `current_stock`.
2. `/home/user/routes.csv`: Contains columns `source_id`, `target_id`, and `transit_time_days`. This represents a directed graph of routes between warehouses.

Write a Python script at `/home/user/analyze.py` that performs the following tasks:
1. Parse the CSV files.
2. Treat the routes as a directed graph where edges are weighted by `transit_time_days`.
3. Compute the shortest path distance (minimum total `transit_time_days`) from the source warehouse `WH-01` to all other reachable warehouses.
4. For each reachable warehouse (excluding `WH-01`), calculate an `urgency_score`. The formula is:
   `urgency_score = (capacity - current_stock) / shortest_transit_time_from_WH_01`
5. Sort the reachable warehouses in descending order by `urgency_score`. If there is a tie, sort alphabetically by `warehouse_id` in ascending order.
6. Output the top 3 warehouses (pagination/filtering) to a new CSV file located at `/home/user/top_warehouses.csv`.
   - The output CSV must have exactly two columns: `warehouse_id` and `urgency_score`.
   - The `urgency_score` must be rounded to exactly 2 decimal places (e.g., `150.00`, `66.67`).
   - Include the header row: `warehouse_id,urgency_score`.

Run your script to generate the output file before completing the task. You may use standard Python libraries or popular third-party libraries like `pandas` and `networkx` if they are installed, but the standard library is sufficient.