You are a data engineer building an ETL pipeline. Your current objective is to project a bipartite graph (users and items) into a unipartite item-item graph based on shared user interactions.

You have been provided an input file at `/home/user/data/user_item.csv` (which has no header). Each line contains two comma-separated values: `user_id,item_id`. This represents an edge in a bipartite graph where a user interacted with an item.

Your task is to write a Go program at `/home/user/project_graph.go` that performs the following:
1. Reads the bipartite edge list from `/home/user/data/user_item.csv`.
2. Projects it into an item-item graph. An edge exists between `item_A` and `item_B` if they share at least 2 common users. 
3. The "weight" of this item-item edge is the number of distinct users who interacted with both items.
4. Outputs the materialized item-item edges to `/home/user/output/item_item_edges.csv`.

**Constraints and Output Requirements:**
* The output file must be a CSV with no header, containing three columns: `item_1,item_2,weight`.
* For every pair, ensure that `item_1` is lexicographically strictly less than `item_2` (e.g., if "apple" and "banana" share users, it must be "apple,banana,W", never "banana,apple,W").
* Only include pairs where `weight >= 2`.
* Sort the output lines primarily by `weight` in descending order. If weights are equal, sort by `item_1` in ascending lexicographical order. If `item_1` is also equal, sort by `item_2` in ascending lexicographical order.
* Create the `/home/user/output/` directory if it does not exist.
* Execute your Go script so the output file is generated.

Do not write anything else to the output file. Just the comma-separated values.