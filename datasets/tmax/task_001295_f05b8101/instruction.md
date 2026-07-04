You are a database administrator tasked with optimizing and extracting hierarchical data from a hybrid relational-document database. 

You have been provided an SQLite database at `/home/user/company.db`. This database contains a single table named `personnel` which stores employee records. The schema was poorly documented, but you know it contains an `id` (integer), a `reports_to` (integer, nullable) indicating their manager's `id`, and a `document` (text) column containing a JSON payload with varying NoSQL-style schemas.

The `document` JSON consistently contains a `compensation` object, which may have `base` and `bonus` numeric fields (if a field is missing, assume it is 0).

Your task is to write a Python script at `/home/user/calculate_costs.py` that computes the total compensation cost (base + bonus) for *every* employee's entire reporting tree (including themselves, their direct reports, their direct reports' reports, and so on). 

Your script must:
1. Reverse engineer the tree structure and extract the compensation data from the JSON documents. (You may use SQLite recursive CTEs and JSON functions, or do it entirely in Python).
2. Calculate the total cost and the total number of people in each employee's tree.
3. Validate the output to ensure it perfectly matches the required schema.
4. Output the results to `/home/user/manager_costs.jsonl` (one JSON object per line).

The output in `manager_costs.jsonl` must conform exactly to this schema for every line:
`{"manager_id": <int>, "total_tree_cost": <float>, "tree_size": <int>}`

Ensure the file is sorted by `manager_id` in ascending order.