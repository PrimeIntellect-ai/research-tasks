You are a Database Administrator taking over a legacy logistics tracking system. The previous DBA left behind an undocumented SQLite database at `/home/user/logistics.db`. 

Your goals are to reverse engineer the data model, perform graph analytics to identify network bottlenecks, and write an optimized analytical query to extract delivery metrics.

Please complete the following tasks:

1. **Reverse Engineer the Data Model**: 
   Analyze the tables in `/home/user/logistics.db`. There are three poorly named tables: `t1_x` (represents locations/nodes), `t2_y` (represents bidirectional connections/edges between locations with distances), and `t3_z` (represents historical deliveries). 

2. **Graph Analytics**:
   Write a Python script at `/home/user/graph_analysis.py` that reads the nodes and edges from the database to build a graph network. Using the `networkx` library, calculate the unweighted Betweenness Centrality of all nodes. 
   Find the name of the location with the highest betweenness centrality (the primary bottleneck). Write the exact name of this location to `/home/user/bottleneck.txt`.

3. **Window Functions & Analytical Aggregation**:
   We need to audit expensive deliveries. Write an optimized SQL query that uses Window Functions to find the top 2 most expensive deliveries (based on the `cost` column) for *each* `region_code`. 
   However, you must *only* include deliveries where the source and destination locations are directly connected in the network with a `distance` strictly greater than 100.
   Save your SQL query to `/home/user/query.sql`.

4. **Query Export**:
   Execute your query against the database and export the results to a JSON file at `/home/user/expensive_deliveries.json`. The JSON should be a list of objects, ordered by `region_code` (ascending) and then by `cost` (descending). Each object must have the following keys:
   - `delivery_id` (integer)
   - `region_code` (string)
   - `cost` (float)
   - `source_name` (string - the name of the origin location)
   - `dest_name` (string - the name of the destination location)

Make sure to install any required Python packages (like `networkx` or `pandas`) using pip. Do not use root/sudo.