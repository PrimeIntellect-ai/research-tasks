You are assisting a compliance officer auditing an internal access control system. The system's data is stored in a SQLite database located at `/home/user/audit_system.db`, but the schema documentation has been lost. 

Your task is to reverse engineer the data model, analyze the query performance, and write a C program to cross-reference relational access logs with JSON-based clearance policies to find compliance violations.

Perform the following steps:
1. **Reverse Engineer Data Model:** Inspect `/home/user/audit_system.db`. There are two main tables: one storing employee details and their JSON clearance policies, and another storing access logs for restricted projects.
2. **Query Plan Interpretation:** We need to ensure that querying access logs by employee is efficient. Check if there is an index on the foreign key linking the access logs to the employee table. If not, write a bash command to create an index named `idx_emp_access` on that column. Then, generate the SQLite `EXPLAIN QUERY PLAN` for a `SELECT` statement that joins the employee table and the access logs table to retrieve all employee names and the projects they accessed. Save the exact output of this query plan to `/home/user/query_plan.txt`.
3. **Cross-Representation Mapping & Verification:** Write a C program at `/home/user/check_compliance.c`. The program must:
   - Read the employee and access log data (you can choose to interact with the database directly using the SQLite C API, or dump the data to a file using bash and parse it in C).
   - Parse the JSON clearance column. A clearance policy looks like `{"level": 3, "projects": ["Alpha", "Beta"]}`.
   - An employee is authorized to access a project ONLY IF the project's name exists in their JSON `projects` array. The `level` field is not relevant for this audit.
   - Find all access log entries where an employee accessed a project they are NOT authorized for.
4. Compile the program to `/home/user/check_compliance` and execute it.
5. The C program must output the violations to `/home/user/violations.log`. Each line in the log must be in the format:
   `[Employee Name] unauthorized access to [Project Name]`
   (Sort the output alphabetically by Employee Name, then by Project Name).

Constraints:
- Only use standard C libraries or the SQLite C API (`libsqlite3-dev` is installed) and `cJSON` or basic string parsing for JSON. (Since basic string parsing of JSON arrays is straightforward in C, you can implement a simple string search).
- Bash shell tools are permitted to assist in dumping data if you prefer not to use the SQLite C API directly.