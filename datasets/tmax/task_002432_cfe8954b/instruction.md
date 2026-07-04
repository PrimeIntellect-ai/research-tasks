You are a data analyst working with a custom graph processing pipeline. We have a set of CSV files representing a social network graph, and we need to compute the shortest path between two users.

Currently, we rely on a combination of C and bash tools for performance. 

Your task is to:
1. Write a C program at `/home/user/shortest_path.c` that reads a directed graph from a CSV file (`edges.csv`) and computes the shortest path between two node IDs using Breadth-First Search (BFS). 
   - The program should take three command-line arguments: `<edges_csv_path> <start_node_id> <end_node_id>`.
   - It should print the sequence of node IDs in the shortest path, separated by spaces (e.g., `1 2 3`). If no path exists, print `NO_PATH`.
2. Write a bash script `/home/user/pipeline.sh` that:
   - Compiles the C program.
   - Takes two arguments: `<start_id> <end_id>`.
   - Runs the compiled C program using the files in `/home/user/data/edges.csv`.
   - Reads `/home/user/data/nodes.csv` to map the output IDs to user names.
   - Outputs a validated JSON representation of the path to `/home/user/path_output.json`.

The CSV files are located at:
- `/home/user/data/nodes.csv` (columns: `id,name`)
- `/home/user/data/edges.csv` (columns: `source,target`)

The output JSON in `/home/user/path_output.json` must strictly follow this schema:
```json
{
  "path": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
  ],
  "length": 2
}
```
(Where `length` is the number of edges in the path).

Note: The maximum node ID will not exceed 1000. All IDs are positive integers. The graph is unweighted. If there are multiple shortest paths, any valid shortest path is acceptable.

After writing the scripts, execute `/home/user/pipeline.sh 1 7` so that the output JSON is generated.