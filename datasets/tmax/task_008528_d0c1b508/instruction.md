You are a data analyst for a logistics company. You have been provided with a dataset of shipping routes in a CSV file located at `/home/user/network.csv`. The file contains the following columns: `source_city`, `target_city`, `base_cost`, and `delay_factor`. 

Your task is to write a Python script at `/home/user/analyze.py` that processes this data, finds the optimal route, and generates an analytical report.

The script must fulfill the following requirements:
1. **Database Setup & Indexing**: 
   - Read `/home/user/network.csv` and load it into a local SQLite database at `/home/user/logistics.db` in a table named `routes`.
   - Implement an **index strategy** by creating a composite index on `source_city` and `target_city` to optimize future lookup queries.

2. **Graph Traversal & Shortest Path**:
   - The script should accept two command-line arguments: `--start` and `--end` (e.g., `python3 analyze.py --start Alpha --end Zeta`).
   - Using the data from the SQLite database, compute the shortest path between the start and end cities. The graph is **directed**.
   - The true cost of an edge is calculated as: `base_cost + (base_cost * delay_factor)`.

3. **Query-to-Pipeline & Window Functions**:
   - Once the shortest path is found, insert the sequence of the path into a new SQLite table called `path_sequence` with columns: `step_order` (integer, starting at 1), `city_name` (text), and `hop_cost` (real). For the start city, the `hop_cost` is 0.0. For subsequent cities, `hop_cost` is the true cost from the previous city to this city. Use **parameterized queries** for all insertions to prevent SQL injection.
   - Execute a SQL query on the `path_sequence` table that utilizes a **window function** to calculate the `cumulative_cost` (the running total of `hop_cost` ordered by `step_order`).
   
4. **Output**:
   - The script must export the result of the window function query to a CSV file at `/home/user/optimal_route.csv`.
   - The output CSV must have exactly these columns: `step_order,city_name,hop_cost,cumulative_cost`.
   - Float values should be rounded to 2 decimal places in the CSV.

Run your script using `--start Alpha` and `--end Zeta` to generate the final `/home/user/optimal_route.csv`. Ensure your database file `/home/user/logistics.db` is left intact with the tables and indexes created.