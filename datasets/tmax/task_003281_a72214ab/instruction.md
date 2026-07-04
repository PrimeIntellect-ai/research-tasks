You are a data engineer working for a manufacturing company. You need to build an ETL script that flattens a Bill of Materials (BOM) hierarchy into a simple list of required components and their total quantities.

You have been provided an SQLite database at `/home/user/manufacturing.db`. 
The database contains two tables that represent a directed acyclic graph of parts:
1. `components`
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
2. `bom`
   - `parent_id` (INTEGER) - Foreign key to components.id
   - `child_id` (INTEGER) - Foreign key to components.id
   - `quantity` (INTEGER) - Number of `child_id` required to make ONE `parent_id`

Your task is to write a Python script at `/home/user/flatten_bom.py` that queries this database to calculate the total absolute quantity of every sub-component required to build exactly ONE unit of the component with `id = 1` ("Final Product"). 

Requirements for the script:
1. Use an SQL Recursive Common Table Expression (CTE) to traverse the hierarchy starting from `id = 1`.
2. As you traverse down the graph, you must multiply the quantities. For example, if product 1 requires 4 of component A, and component A requires 5 of component B, then product 1 requires 20 of component B.
3. If a component is reached through multiple paths in the graph, its total required quantity should be the sum of the quantities from all paths.
4. The script must output the final aggregated results to `/home/user/bom_flattened.json`.
5. Do not include the top-level product (`id = 1`) in the final output.

The output at `/home/user/bom_flattened.json` must strictly be a JSON array of objects, with each object matching this schema:
`{"component_id": <int>, "component_name": "<str>", "total_quantity": <int>}`

The JSON array must be sorted by `component_id` in ascending order.