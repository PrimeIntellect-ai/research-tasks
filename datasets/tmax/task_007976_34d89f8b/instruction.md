You are a database administrator tasked with optimizing and analyzing a hierarchical data structure for our organization. We store our reporting structure in an SQLite database, but we currently lack an efficient way to analyze the depth and size of management trees (a form of graph centrality and materialization).

Your task has three parts:

1. **Parameterized Query Scripting:**
   Write a Bash script at `/home/user/get_subordinates.sh` that takes a single employee ID as an argument. 
   The script must query the SQLite database located at `/home/user/db/org_chart.db`. 
   It must use a **Recursive CTE** (Common Table Expression) to calculate the total number of indirect and direct subordinates for that employee. 
   You must use parameterized query construction in your bash script to pass the argument safely to SQLite (do not just concatenate the string into the query).
   The script should output exactly: `Subordinate count for <emp_id>: <count>`

2. **Graph Materialization:**
   Write an SQL query (which you should execute against the database) that calculates this subordinate count for *all* employees and materializes the result into a new table named `hierarchy_metrics`.
   The table should have the schema: `hierarchy_metrics(emp_id INTEGER PRIMARY KEY, total_subordinates INTEGER)`.

3. **Graph Analytics (Centrality):**
   Find the employee who acts as the "top Vice President" — defined as the employee with the highest `total_subordinates` who is *not* the ultimate CEO (i.e., their `manager_id` is NOT NULL in the `employees` table).
   Save the result in `/home/user/top_vp.log` in the exact format: `emp_id:count`

**Database details:**
- Path: `/home/user/db/org_chart.db`
- Table: `employees(emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER)`

Ensure your bash script has executable permissions.