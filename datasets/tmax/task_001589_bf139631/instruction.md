You are a Database Administrator tasked with optimizing a logistics network by analyzing historical shipment data. 

You have been provided an SQLite database at `/home/user/logistics.db`. The database schema is undocumented, but it contains information about locations, shipping routes, and individual shipment logs. 

Your task is to reverse-engineer the schema and perform a graph analytics operation to identify the most critical logistical hub. Specifically, you need to:
1. Analyze the tables to understand how locations, routes, and shipments are related (cross-representation mapping).
2. Write a Python script `/home/user/find_hub.py` that reads the SQLite database and builds a directed graph. The nodes are the locations, and the directed edges are the routes.
3. The "weight" of each directed edge must be the total number of historical shipments that have traveled along that specific route.
4. Calculate the weighted out-degree for each location (the total number of shipments originating from that location).
5. Identify the location with the highest weighted out-degree.
6. Write the *name* (not the ID) of this optimal hub location to a file named `/home/user/optimal_hub.txt`.

The output file `/home/user/optimal_hub.txt` should contain exactly the name of the location and nothing else. You may install and use any standard Python packages like `networkx` or `pandas` if you wish, though you can also solve this using standard library tools and SQL queries.