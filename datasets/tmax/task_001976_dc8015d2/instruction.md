You are a database administrator tasked with fixing a buggy reporting script. 

We have an SQLite database located at `/home/user/company.db` containing a knowledge graph of employee collaborations. The tables are:
- `employees` (id, name, dept_id)
- `departments` (id, name)
- `collaborations` (emp_id_1, emp_id_2, weight)

There is a Python script `/home/user/generate_report.py` that is supposed to extract the collaboration graph for a specific department (paramaterized, currently set to department ID 1) and output a JSON array of collaboration objects. 

However, the script has two issues:
1. The SQL query contains an implicit cross join that causes it to return wrong results (duplicate rows with incorrect department names). You need to analyze the schema and fix the query so that it correctly links the `departments` table to the first employee's department.
2. The script currently just prints the raw data. You need to update the script to format the output as JSON, validate it against the JSON schema located at `/home/user/schema.json`, and save the valid JSON to `/home/user/report.json`.

Please fix the SQL query to resolve the cross join, ensure the query remains parameterized, add the necessary output validation using the `jsonschema` python package, and run the script to produce `/home/user/report.json`. 

Do not change the target department ID (it should remain 1).