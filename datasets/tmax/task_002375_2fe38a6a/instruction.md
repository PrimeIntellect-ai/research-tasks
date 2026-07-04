You are a data analyst working for a manufacturing company. You have been given two CSV files representing a complex Bill of Materials (BOM) graph for various products.

Your task is to process these CSVs, construct a localized relational database, optimize it for graph traversal, and compute the total raw materials required to fulfill a specific order.

**Input Files:**
You will find two files in `/home/user/data/`:
1. `items.csv`: Contains `item_id`, `item_name`, and `item_type` (which can be 'product', 'subassembly', 'part', or 'raw_material').
2. `bom.csv`: Contains `parent_id`, `child_id`, and `quantity`. This represents the directed edges of the manufacturing graph (how many of `child_id` are needed to make one `parent_id`).

**Requirements:**
1. **Database Initialization:** Create an SQLite database at `/home/user/supply_chain.db`.
2. **Data Import:** Import the CSV data into two tables named `items` and `bom`.
3. **Index Strategy:** Create appropriate indexes on the `bom` table to optimize downward graph traversal (finding children of a parent) and on the `items` table for fast primary key lookups.
4. **Parameterized Graph Query:** Write a script or command that takes a target `item_id` and a `target_quantity` as parameters, and executes a Recursive Common Table Expression (CTE) to traverse the BOM graph. 
5. **Execution:** Use your script to calculate the total quantities of all **raw materials** (where `item_type = 'raw_material'`) needed to build **50 units** of the product with `item_id` equal to `PROD-001`.
6. **Output:** Save the results to `/home/user/materials_needed.csv`. The file must contain exactly three columns: `leaf_item_id`, `leaf_item_name`, and `total_quantity_needed`. The output must include a header row, and the data rows must be sorted alphabetically by `leaf_item_id`.

Ensure that your recursive query correctly multiplies quantities down the graph (e.g., if A needs 2 of B, and B needs 3 of C, then A needs 6 of C).