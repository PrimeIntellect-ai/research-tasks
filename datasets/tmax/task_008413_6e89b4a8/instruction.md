You are a data engineer tasked with building a high-performance ETL component in C. We have a relational database that stores hierarchical graph data representing our company's reporting structure. 

We need to calculate the total salary burden of all indirect and direct subordinates under the "Engineering" umbrella, broken down by department, and export this data to a JSON file.

**Environment Details:**
- A SQLite database is located at `/home/user/data/company.db`.
- The database contains three tables:
  - `departments` (`id` INTEGER PRIMARY KEY, `name` TEXT)
  - `employees` (`id` INTEGER PRIMARY KEY, `name` TEXT, `department_id` INTEGER, `salary` REAL)
  - `reporting_lines` (`manager_id` INTEGER, `subordinate_id` INTEGER)

**Your Objectives:**
1. Write a C program at `/home/user/etl_graph.c`.
2. The program must connect to `/home/user/data/company.db` using the SQLite C API (`sqlite3.h`).
3. Your C program must execute a query that:
   - Uses a Recursive Common Table Expression (CTE) to traverse the `reporting_lines` graph, starting from the employee named "Alice" (who is the VP of Engineering). You must find all her direct and indirect subordinates.
   - Joins the graph traversal results with the `employees` and `departments` tables.
   - Aggregates the total `salary` of these subordinates, grouped by the department name. (Do not include Alice's own salary in the total).
4. The C program must export the aggregated results to a JSON file at `/home/user/output/dept_costs.json`.
5. Compile your C program to an executable named `/home/user/etl_graph` and run it. You may need to install `libsqlite3-dev` or similar packages if they are missing.

**Output Format:**
The file `/home/user/output/dept_costs.json` must be a valid JSON array of objects, sorted alphabetically by department name. Each object must have exactly two keys: `"department"` (string) and `"total_salary"` (number, with exactly 2 decimal places).
Example:
```json
[
  {
    "department": "Backend",
    "total_salary": 240000.00
  },
  {
    "department": "Frontend",
    "total_salary": 185500.00
  }
]
```

Ensure the output directory exists before writing to it.