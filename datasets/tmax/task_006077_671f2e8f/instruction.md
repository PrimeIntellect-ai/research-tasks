You are a database administrator tasked with optimizing and extracting data from an undocumented legacy SQLite database. 

You have been given an SQLite database file at `/home/user/supply_chain.db`. The database contains information about various facilities and the transit routes between them, but the schema is undocumented. 

Your objectives are:
1. **Reverse Engineer the Schema**: Inspect the database to find the tables representing facilities (nodes) and transit routes (directed edges). 
2. **Graph Traversal**: Write a Python script `/home/user/process_routes.py` that connects to this database and computes the shortest transit time from the starting facility named `Factory_Alpha` to all other facilities of type `Warehouse`. 
   - You must only traverse routes that are currently "active" or "open". Closed routes must be ignored.
   - Transit time is the sum of the edge weights along the path.
3. **Filtering, Sorting, and Pagination**: 
   - Filter the results to strictly include destinations of type `Warehouse` that are reachable.
   - Sort the reachable warehouses by their `total_transit_time` in ascending order.
   - If two warehouses have the same transit time, break ties by sorting by their facility ID in ascending order.
   - Paginate the sorted results: extract exactly 3 records starting from offset 2 (i.e., skipping the first 2 results).

**Output Specification**:
Your script `/home/user/process_routes.py` must output the final paginated results to a JSON file at `/home/user/route_results.json`. 
The JSON should be a list of objects, each containing exactly these keys:
- `destination_id` (integer)
- `destination_name` (string)
- `total_transit_time` (integer)

Example output format for `/home/user/route_results.json`:
```json
[
  {
    "destination_id": 9,
    "destination_name": "Warehouse_X",
    "total_transit_time": 45
  },
  ...
]
```
Ensure your Python script runs successfully and produces the expected JSON file.