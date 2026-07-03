You are a database administrator tasked with fixing a data processing pipeline. 

We store our system's interaction graph in two TSV (tab-separated) files:
1. `/home/user/nodes.tsv`: Contains system entities. Columns are `node_id`, `entity_name`, and `role`.
2. `/home/user/edges.tsv`: Contains directed interactions. Columns are `source_id`, `target_id`, and `action_type`.

A previous administrator tried to write a query to find the "Execute Out-Degree" for all users with the role "Admin". That is, they wanted to count how many 'Execute' actions each 'Admin' initiated (where the Admin is the `source_id`). However, their script caused an implicit cross join and returned massively inflated numbers.

Your task is to write a bash command or script to correctly compute this metric using standard Linux CLI tools (like `awk`, `grep`, `join`, `sort`, `uniq`, etc.). 

Requirements:
1. Find all nodes in `/home/user/nodes.tsv` where the `role` is exactly `Admin`.
2. For these Admin nodes, count the number of times their `node_id` appears as a `source_id` in `/home/user/edges.tsv` where the `action_type` is exactly `Execute`.
3. If an Admin has zero 'Execute' actions, they do not need to be included in the output.
4. Save the results to `/home/user/admin_execute_stats.tsv`.
5. The output file must contain exactly two tab-separated columns: `entity_name` and `execute_count`.
6. The output must be sorted by `execute_count` in descending order. If there is a tie, sort by `entity_name` in ascending alphabetical order.

You may create any temporary files you need in `/home/user/`, but the final output must be exactly formatted in `/home/user/admin_execute_stats.tsv`.