You are a data analyst working for a manufacturing company. You only have access to standard Linux command-line tools (Bash, awk, grep, etc.) to process some exported CSV files.

You have been given two CSV files representing a Bill of Materials (BOM) and a component catalog:
1. `/home/user/components.csv`
   Schema: `id,name,type`
   Types can be `product`, `assembly`, or `raw`.
2. `/home/user/bom.csv`
   Schema: `parent_id,child_id,qty`
   This represents the immediate children needed to build a parent component, and the quantity of the child required.

Your task is to write a script or execute commands to perform a full hierarchical BOM explosion for the product with `id` equal to `P-01`. You need to calculate the total aggregated quantity of all base raw materials (components of type `raw`) required to build exactly ONE unit of `P-01`. 

Because assemblies can contain other assemblies, your solution must resolve the hierarchy recursively (or simulate it) and multiply the quantities appropriately down the tree.

Once you have calculated the total required quantities for each raw material, join them with their human-readable names. 

Write the final result to `/home/user/raw_materials_needed.csv`. 
The file must have exactly this format:
- A header row: `name,quantity`
- Followed by the raw material names and their total aggregated quantities.
- The rows must be sorted alphabetically by the `name` column.

Requirements:
- Only use standard Bash built-ins or common Linux coreutils (`awk`, `sed`, `grep`, `join`, `sort`, etc.).
- Do not use Python, Perl, or any external database engines.
- Ensure the output file is located exactly at `/home/user/raw_materials_needed.csv`.