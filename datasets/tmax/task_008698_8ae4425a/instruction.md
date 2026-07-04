You are acting as a Database Administrator and C++ Developer. We have a SQLite database located at `/home/user/db_perf/sales.db` containing e-commerce data, but the current reporting process is extremely slow and outputs raw CSV instead of the hierarchical document format our frontend needs.

Your task is to analyze the schema, optimize the database with indexes, and write a C++ program that efficiently aggregates the data and exports it as a JSON document.

Here are the specific requirements:

1. **Schema Analysis & Optimization**:
   - The database contains four tables: `users`, `orders`, `order_items`, and `products`.
   - Analyze the schema using the `sqlite3` CLI.
   - Design an index strategy to optimize a query that joins all four tables, filters orders by status 'COMPLETED', and groups by user region and product category.
   - Write your index creation statements to `/home/user/db_perf/indexes.sql` and apply them to the database.

2. **C++ Aggregation Program**:
   - Write a C++ program at `/home/user/db_perf/aggregator.cpp`.
   - You may install `libsqlite3-dev` and use `nlohmann-json` (you can download the single-header `json.hpp` using `wget https://github.com/nlohmann/json/releases/download/v3.11.2/json.hpp`).
   - The program must connect to `sales.db`.
   - It should calculate the `total_revenue` (sum of `quantity * price`) and `completed_order_count` (count of distinct orders) for each product `category` within each user `region`. Only include 'COMPLETED' orders.
   - Compile your program to `/home/user/db_perf/aggregator`.

3. **Format Conversion & Export**:
   - The compiled C++ program must output a JSON file to `/home/user/db_perf/regional_summary.json`.
   - The JSON must exactly match this structure (an array of region objects, each containing an array of category objects):
     ```json
     [
       {
         "region": "North",
         "categories": [
           {
             "category": "Electronics",
             "revenue": 15430.50,
             "order_count": 142
           },
           ...
         ]
       },
       ...
     ]
     ```
   - Both arrays (regions, and categories within regions) must be sorted alphabetically by their respective names.

Ensure your code compiles, runs successfully, and generates the required JSON file with the correct aggregated metrics.