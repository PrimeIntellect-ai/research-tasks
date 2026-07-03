You are acting as a technical compliance officer auditing access controls in our infrastructure. We have an SQLite database containing organizational groups, employees, and resource access policies. 

Your objective is to map out the access graph, optimize the query path, and identify all employees who have indirect or direct unauthorized access to sensitive financial data.

The database is located at `/home/user/audit.db` and has the following schema:
- `employees` (`id` INTEGER PRIMARY KEY, `name` TEXT)
- `groups` (`id` INTEGER PRIMARY KEY, `name` TEXT)
- `group_members` (`employee_id` INTEGER, `group_id` INTEGER)
- `group_hierarchy` (`parent_group_id` INTEGER, `child_group_id` INTEGER) 
  *Note: A member of a `child_group_id` automatically inherits all access policies assigned to its `parent_group_id`, as well as any ancestors up the tree.*
- `access_policies` (`group_id` INTEGER, `resource_name` TEXT, `access_level` TEXT)

Please complete the following tasks:
1. Initialize a Go module in `/home/user/audit` and write a Go program named `find_violations.go`.
2. Use `database/sql` and `github.com/mattn/go-sqlite3` to connect to `/home/user/audit.db`.
3. Inside your Go program, first execute SQL statements to create appropriate indexes on `group_hierarchy` and `group_members` to optimize recursive graph traversals.
4. Write a recursive Common Table Expression (CTE) in SQL to project the group inheritance graph and materialize the effective permissions for all employees.
5. Filter the results to find all employees who have either `'WRITE'` or `'ADMIN'` access to the resource `'FINANCIAL_RECORDS'`.
6. Sort the resulting employee names alphabetically (A-Z).
7. Write the sorted list of employee names, one per line, to a text file at `/home/user/violations.log`.

Your script must run successfully and produce the exact `violations.log` file when `go run find_violations.go` is executed.