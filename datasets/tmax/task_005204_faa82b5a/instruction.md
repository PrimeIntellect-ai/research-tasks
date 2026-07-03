You are acting as a Database Administrator and Python Developer. We have an urgent issue with our daily analytical reporting pipeline.

Currently, we have a Python script at `/home/user/report_generator.py` that connects to an SQLite database (`/home/user/ecommerce.db`) and generates a JSON report mapping our relational e-commerce data into a hierarchical document graph (mapping customers to their top 3 most expensive orders using analytical window functions).

However, there are three major problems:
1. The reporting script relies on a vendored version of the `pypika` query builder located at `/app/pypika`. The package cannot be installed right now due to a broken installation file.
2. Once installed, the script takes far too long to run and generates incorrect results. We suspect the query logic inside `/home/user/report_generator.py` is constructing an implicit cross join instead of a proper inner join between `orders` and `order_items`. 
3. The query is generally unoptimized. The database lacks proper indexes to support the analytical window functions and joins.

Your task is to:
1. Fix the broken vendored package in `/app/pypika` and install it in the local environment (`pip install -e /app/pypika`).
2. Fix the query building logic in `/home/user/report_generator.py` so that `orders` and `order_items` are joined correctly on their corresponding keys, removing the cross join.
3. Optimize the SQLite database (`/home/user/ecommerce.db`) by creating the appropriate indexes so the query runs as fast as possible. 
4. Run the script to generate the final `/home/user/output.json`.

The automated verifier will evaluate your solution based on a performance metric: your fixed script must execute in under 0.5 seconds on a hidden test dataset of similar structure, and the output JSON must perfectly reflect the correct top 3 orders per customer without duplicated cross-join rows.