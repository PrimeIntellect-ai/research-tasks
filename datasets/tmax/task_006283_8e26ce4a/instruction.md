You are acting as a Database Administrator for a company that is migrating data from a legacy relational system into both a Document-based NoSQL database and a Graph database. 

Currently, there is a nightly reporting script that extracts employee project assignments. However, the script is taking excessively long and producing millions of rows because the original author made a mistake in the SQL query, resulting in an implicit cross join (Cartesian product).

Your environment contains a SQLite database located at `/home/user/company.db`. 

Your objectives are:
1. **Fix the SQL Query**: Look at the schema in `/home/user/company.db`. The buggy query is intended to list Employee Name, Department Name, and Project Name for all employees assigned to projects. Create a new file `/home/user/fixed_query.sql` with a corrected `SELECT` statement that properly joins the tables and avoids the cross join. Run this query and save the output as a CSV file at `/home/user/relational_export.csv` (include headers: `employee_name,department_name,project_name`, sorted by employee_name then project_name).

2. **Cross-Representation Mapping (Document)**: Write a multi-language script (e.g., Python) to query the database and generate a nested JSON structure representing the data model. Save it to `/home/user/document_export.json`. 
The JSON must be an array of Department objects, sorted by department ID. 
Format:
```json
[
  {
    "department_id": 1,
    "department_name": "Engineering",
    "employees": [
      {
        "employee_id": 101,
        "employee_name": "Alice",
        "projects": [
          {"project_id": 1001, "project_name": "Migration"}
        ]
      }
    ]
  }
]
```
*Note: Sort departments by department_id, employees by employee_id, and projects by project_id.*

3. **Cross-Representation Mapping (Graph)**: Generate two CSV files for Graph DB ingestion:
   - `/home/user/graph_nodes.csv`: headers `node_id,label,name`
     (node_id format: `dept_X`, `emp_X`, `proj_X` where X is the numeric ID. label: `Department`, `Employee`, `Project`).
   - `/home/user/graph_edges.csv`: headers `source,target,relationship`
     (source and target are node_ids. Relationships: Employee belongs to Department -> `WORKS_IN` (source: emp, target: dept). Employee assigned to Project -> `ASSIGNED_TO` (source: emp, target: proj)).
   Sort both CSV files alphabetically by the first column, then the second.

Ensure your scripts are fully self-contained and run successfully to produce the required files.