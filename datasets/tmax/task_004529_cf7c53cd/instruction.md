You are a database administrator tasked with analyzing a complex supply chain network. You need to combine recursive SQL queries, graph analytics, and NoSQL-style JSON document aggregation to identify cost structures, critical components, and supply bottlenecks.

You have been provided with two data sources:
1. A SQLite database at `/home/user/supply_chain.db` containing a `components` table with the following schema:
   `CREATE TABLE components (id INTEGER PRIMARY KEY, name TEXT, parent_id INTEGER, required_qty INTEGER, unit_cost REAL)`
   This table represents a Bill of Materials (BoM). `parent_id` points to the assembly that requires the component. `required_qty` is the number of units needed for one unit of the parent. The root component (Hyperdrive) has `id=1` and `parent_id=NULL`.

2. A JSON file at `/home/user/suppliers.json` simulating a NoSQL document collection of supplier inventories. Each document contains a supplier ID and an array of components they provide along with the available capacity.

Your objective is to write a Python script (e.g., `analyze.py`) that performs the following operations and outputs a final report:

**1. Recursive Cost Calculation (SQL)**
Write a recursive CTE in SQLite to calculate the total aggregate cost to build ONE unit of the root component (id=1). The total cost of a component is its `unit_cost` plus the sum of the total costs of all its children (where each child's total cost is multiplied by its `required_qty`).

**2. Graph Analytics (Python / NetworkX)**
Extract the dependency graph from the database. Build a directed graph using `networkx` where directed edges point from a parent component to its child component. 
Calculate the in-degree centrality of all nodes in this network to identify "bottleneck" items. Find the top 2 components with the highest in-degree centrality.

**3. NoSQL-style Aggregation**
Read `/home/user/suppliers.json`. Using Python data structures (simulating an aggregation pipeline), compute the total available supply capacity for every component across all suppliers.

**4. Generate Report**
Output the results to `/home/user/optimization_report.json` strictly in the following JSON format:
```json
{
  "total_root_cost": 0.00,
  "top_2_central_components": [id1, id2],
  "total_capacity_by_component": {
    "1": 0,
    "2": 0
  }
}
```
*Note for lists/arrays: Order `top_2_central_components` by centrality descending, then by ID ascending.*

Ensure you install any necessary dependencies (like `networkx`) locally before running your script.