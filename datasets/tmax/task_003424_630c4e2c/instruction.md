You are a data analyst working for a logistics company. You have been provided with several CSV files representing the company's supply chain network. You need to write a C++ program to analyze this data, build a graph representation, and execute a specific routing query.

The data is located in `/home/user/data/` (you can assume this directory and the files already exist):

1. `warehouses.csv`
   Columns: `w_id,name,region`
   Description: Lists all warehouses.

2. `routes.csv`
   Columns: `src_w_id,dst_w_id,distance,risk_score`
   Description: Directed routes between warehouses. `distance` is an integer representing kilometers. `risk_score` is an integer from 1 to 10.

3. `inventory.csv`
   Columns: `w_id,item_id,quantity`
   Description: Current stock levels of items in each warehouse.

**Your Task:**
Write a C++ program at `/home/user/solve.cpp` that reads these CSV files and finds the shortest path (minimum total distance) from the starting warehouse `W001` to *any* warehouse that currently stocks at least 50 units of `ITEM-999`. 

**Critical Constraints:**
- The routing must strictly avoid any individual route (edge) that has a `risk_score` of 8 or higher.
- If there are multiple target warehouses meeting the inventory criteria, choose the one that results in the smallest total distance from `W001`.
- All routes are directed (`src_w_id` -> `dst_w_id`).

**Output Requirements:**
Your C++ program should be compiled and executed. It must create a file at `/home/user/result.txt` containing exactly two lines:
1. The ordered, comma-separated list of warehouse IDs in the optimal path (starting with `W001` and ending with the target warehouse).
2. The total distance of this path.

Example `/home/user/result.txt`:
W001,W012,W045,W088
125