You are acting as a compliance officer auditing a company's internal access logs. We need to identify unauthorized access attempts to restricted resources based on a hierarchical department structure.

You have been provided with an SQLite database at `/home/user/corp_auth.db` containing the company's access control lists, and a text file `/home/user/access_requests.txt` containing the access logs we need to audit.

The SQLite database has the following schema:
1. `employees` (emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER)
2. `departments` (dept_id INTEGER PRIMARY KEY, dept_name TEXT, parent_dept_id INTEGER) - Note: `parent_dept_id` is NULL for the root department.
3. `resource_policies` (resource_id TEXT PRIMARY KEY, required_dept_id INTEGER)

**Compliance Rule:**
An employee is authorized to access a resource ONLY IF their `dept_id` is exactly the `required_dept_id` for that resource, OR if their department is a direct or indirect descendant (child, grandchild, etc.) of the `required_dept_id` in the department hierarchy.

**Your Task:**
Write a C++ program at `/home/user/audit_processor.cpp` that reads `/home/user/access_requests.txt`.
The `access_requests.txt` file contains one request per line in the format: `emp_id,resource_id`

For each line, your C++ program must:
1. Connect to `/home/user/corp_auth.db` using the standard C SQLite3 library (`<sqlite3.h>`).
2. Construct a parameterized query (to avoid SQL injection and syntax errors) that utilizes a **Recursive CTE** (to walk the department graph) and joins the necessary tables to determine if the employee has access to the resource.
3. Write the results to `/home/user/audit_results.txt`. Each line must be formatted as: `emp_id,resource_id,STATUS` where `STATUS` is either `APPROVED` or `DENIED`.

**Requirements:**
- Compile your program using `g++ -std=c++17 -o /home/user/audit_processor /home/user/audit_processor.cpp -lsqlite3`.
- Execute the compiled binary so that it processes the file and generates `/home/user/audit_results.txt`.
- Do not modify the database or the `access_requests.txt` file.