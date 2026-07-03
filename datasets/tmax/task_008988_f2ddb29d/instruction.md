You are a data engineer building an ETL pipeline to process hierarchical cost data. You have a raw data file located at `/home/user/raw_costs.csv`.

The CSV file has the following format (no header row):
`node_id,parent_id,cost,department`
- `node_id`: Integer (unique identifier for the node)
- `parent_id`: Integer (id of the parent node. `0` indicates a root node)
- `cost`: Integer (the isolated cost of this specific node)
- `department`: String (up to 20 characters, e.g., "Engineering")

Your task is to write a C program and a Bash script to process this data.

1. Create a C program at `/home/user/rollup.c`.
This program must:
- Read `/home/user/raw_costs.csv`.
- Calculate the **total hierarchical cost** for every node. The total hierarchical cost of a node is its own `cost` plus the total hierarchical cost of all its descendants.
- Accept exactly three command-line arguments in this order: `department`, `offset`, `limit`.
  Example: `./rollup Engineering 1 2`
- Filter the results to only include nodes that belong to the specified `department`.
- Sort the filtered nodes by their calculated **total hierarchical cost** in descending order. If there is a tie, sort by `node_id` in ascending order.
- Apply pagination using the `offset` (number of records to skip) and `limit` (maximum number of records to return).
- Print the final paginated list to standard output in the format: `node_id,total_cost` (one per line).

2. Create a bash script at `/home/user/pipeline.sh`.
This script must:
- Compile your C program using `gcc` into an executable named `/home/user/rollup`.
- Execute the compiled program to query for the "Engineering" department, skipping the 1st highest cost (offset 1), and returning the next 2 highest costs (limit 2).
- Redirect the standard output of this execution to a file named `/home/user/final_output.txt`.

Ensure `/home/user/pipeline.sh` is executable and runs without errors.