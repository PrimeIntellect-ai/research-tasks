You are a data analyst tasked with processing supply chain network data for a logistics company. You need to write and execute a Python script to process CSV files, build a graph representation of our network, perform specific graph algorithms, and export the results.

The data is located in `/home/user/logistics/` and consists of two files:
1. `nodes.csv` - Contains information about distribution centers. Columns: `node_id`, `name`, `is_active`
2. `edges.csv` - Contains information about the routes between centers. Columns: `source`, `target`, `weight`, `edge_type`

Your task has three main requirements:

1. **Graph Materialization & Filtering:**
   Read the CSV files and construct a directed graph. You must filter out any nodes where `is_active` is `False` (and remove any edges connected to them). You must also filter out any edges where `edge_type` is `'maintenance'`.

2. **Shortest Path Query & Format Conversion:**
   Calculate the shortest path (minimizing `weight`) from the node named 'Alpha' to the node named 'Kilo'. 
   Export this result to a JSON file located at `/home/user/report.json`. The JSON must have exactly this structure:
   ```json
   {
       "path": ["Alpha", "NextNode", "...", "Kilo"],
       "total_weight": 0
   }
   ```
   *Note: The `path` array must contain the string `name`s of the nodes, not their `node_id`s.*

3. **Complex Join & Sorting:**
   Find the 5 closest reachable nodes to 'Alpha' (excluding 'Alpha' itself) in the filtered graph. 
   Export this list to a CSV file located at `/home/user/top_destinations.csv`. 
   The CSV must have exactly two columns: `node_name` and `distance`. 
   The results must be sorted by `distance` in ascending order. If there is a tie, sort alphabetically by `node_name`.

You may use any standard Python libraries or install third-party libraries (like `pandas` and `networkx`) using `pip`. 
Ensure your final script creates the exact output files specified above.