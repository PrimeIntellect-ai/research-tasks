You are acting as a data analyst. You have been given a set of undocumented CSV files representing a network topology in `/home/user/network_data/`. 

Your objectives are to reverse-engineer the schema, validate the data integrity, and perform a graph traversal calculation.

1. **Schema Analysis & Validation**:
Examine the CSV files in `/home/user/network_data/`. There are two files: `nodes.csv` and `edges.csv`. 
Find any edges that reference non-existent nodes (either in the source or destination column). 
Extract these orphaned edge records and save them to a new file at `/home/user/validation_errors.csv`. The file should strictly contain the exact header from `edges.csv` followed by the invalid rows in the same format.

2. **Graph Traversal (Shortest Path)**:
Using the valid edges (ignore the orphaned records identified in step 1), calculate the shortest path based on the connection costs from the node named 'Alpha' to the node named 'Omega'.
You may write a script in Python, Ruby, Perl, or any standard tool available in a Linux environment to compute this.

3. **Output Format**:
Write the result of your shortest path computation to `/home/user/shortest_path.json`. The JSON file must strictly follow this schema:
```json
{
  "path": [ <list of integer node IDs in the path, starting with Alpha's ID and ending with Omega's ID> ],
  "total_cost": <integer representing the sum of the costs on the path>
}
```

Ensure all output files are placed exactly at the specified absolute paths.