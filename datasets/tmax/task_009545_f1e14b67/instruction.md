You are acting on behalf of a compliance officer who is auditing an organization's access control systems. You have been provided with an SQLite database at `/home/user/audit.db` containing two tables:

1. `employees`
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `manager_id` (INTEGER) - References `id` of the manager. If NULL, the employee is a Department Head.
   - `department` (TEXT)

2. `access`
   - `employee_id` (INTEGER)
   - `system_name` (TEXT)
   - `risk_level` (INTEGER)

Your task is to write a C program at `/home/user/audit_report.c` that connects to this database and generates a specific compliance report. 

The program must execute a query that uses:
1. A **Recursive CTE** to determine the top-level "Department Head" (the ultimate manager with no `manager_id`) for every employee in the hierarchy.
2. A **Window Function** to rank the systems accessed within each department based on `risk_level` (Descending order). If there is a tie in risk level, break the tie by ordering `system_name` in Ascending alphabetical order.

The program must execute the query and write the top 2 highest-risk system accesses per department (Rank <= 2) to a CSV file located at `/home/user/compliance_report.csv`. 

The CSV file must have the following exact header row and be ordered by `Department Head` (Ascending), `Rank` (Ascending), and `Employee` (Ascending):
`Department Head,Employee,System Name,Risk Level,Rank`

Requirements:
- Write the C program in `/home/user/audit_report.c`.
- Compile it to an executable at `/home/user/audit_report`.
- You must use the SQLite C API (`#include <sqlite3.h>`).
- Execute the compiled program to generate `/home/user/compliance_report.csv`.
- Ensure standard CSV formatting (comma-separated, newline-terminated).