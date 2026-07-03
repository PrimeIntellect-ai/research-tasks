You are a data analyst optimizing logistics for a regional supply chain. You have been provided with two CSV files in your home directory (`/home/user/`):
1. `routes.csv` - Contains the available shipping routes. Columns: `source`, `destination`, `cost`.
2. `orders.csv` - Contains a list of fulfillment orders. Columns: `order_id`, `origin`, `destination`.

Your task requires utilizing Graph processing and NoSQL aggregation pipelines. Follow these steps precisely:

1. **Database Initialization**: 
   MongoDB is pre-installed on this system. Initialize a local MongoDB instance running as the current user. Create a database directory at `/home/user/mongo_data` and start `mongod` in the background, bound to port 27017.

2. **Data Ingestion & Graph Computation**:
   Write a Python script (using `pymongo` and `networkx`) that:
   - Reads `routes.csv` and builds a directed graph.
   - Reads `orders.csv` and uses Dijkstra's algorithm to compute the shortest (cheapest) path for each order from its `origin` to its `destination`. If a path does not exist, the cost should be `-1`.
   - Inserts each order into a MongoDB database called `logistics`, collection `processed_orders`. Each document must have the exact fields: `order_id` (int), `origin` (string), `destination` (string), `path` (array of strings representing the route), and `total_cost` (float).

3. **NoSQL Aggregation**:
   Once the data is populated, write a second Python script that executes a MongoDB aggregation pipeline on the `processed_orders` collection. The pipeline must:
   - Filter out orders where a path was not found (`total_cost` == -1).
   - Group the remaining orders by `origin`, calculating the `average_cost` (float) of all successfully routed orders originating from there, and `successful_orders` (the count of such orders).
   - Sort the results descending by `average_cost`.
   - Paginate the results: Skip the first 1 record, and Limit the result to the next 3 records.

4. **Export**:
   The Python script should export the results of the aggregation pipeline directly into a JSON file at `/home/user/final_report.json`. The output should be a JSON array of objects, e.g.:
   `[{"_id": "CityA", "average_cost": 150.5, "successful_orders": 2}, ...]`

Ensure your final JSON file exactly matches the requested format and is correctly paginated.