You are a data analyst given the task of analyzing a company's logistics network.

You are provided with two CSV files in the `/home/user/` directory:
1. `locations.csv` - Contains the columns `loc_id` and `loc_name`.
2. `routes.csv` - Contains the columns `source_id`, `dest_id`, and `distance`. These represent directional routes from a source location to a destination location and their respective distances in miles.

Your task is to write a script or command-line pipeline (using Python, SQL via SQLite, bash, or a combination thereof) to:
1. Load and parse the CSV data.
2. Find the shortest path (minimum total distance) from the location named "Warehouse_Alpha" to the location named "Store_Omega".
3. Export the results to a JSON file located at `/home/user/shortest_path.json`.

The output JSON must strictly match the following format:
```json
{
  "path": [
    "Warehouse_Alpha",
    "Some_Intermediate_Hub",
    "Store_Omega"
  ],
  "total_distance": 150
}
```
Replace the list and distance with the actual computed shortest path. The `path` array must contain the `loc_name` strings in the exact order they are visited.

Do not guess the data; write the necessary code to process the CSV files and compute the answer dynamically.