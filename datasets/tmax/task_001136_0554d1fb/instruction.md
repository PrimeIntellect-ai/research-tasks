You are acting as a Database Administrator optimizing and querying a graph-like organizational hierarchy. 

You have been provided with an SQLite database at `/home/user/company.db`. It contains two tables:
1. `employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT)`
2. `manager (emp_id INTEGER, manager_id INTEGER)` - represents the reporting structure. `manager_id` is the direct supervisor of `emp_id`. The CEO has no entry where they are the `emp_id` with a non-null `manager_id` (or their `manager_id` is NULL).

Some queries on this database are currently running slow, and the HR department needs a reporting tool to traverse this graph.

Your task is to write a bash script at `/home/user/get_network.sh` that takes exactly three arguments: `employee_id`, `limit`, and `offset`.

The script must do the following:
1. **Optimize**: Ensure that appropriate indexes exist on the `manager` table (specifically on `emp_id` and `manager_id`) to speed up graph traversal. The script should create these indexes if they do not already exist.
2. **Graph Traversal (Up)**: Compute the complete management chain starting from the top of the organization (the CEO) down to the provided `employee_id`. You must use a recursive CTE (Common Table Expression) to traverse the tree. Join with the `employees` table to get names and departments.
3. **Graph Traversal (Down) & Pagination**: Compute all subordinates (both direct and indirect) of the given `employee_id`. Sort them by their `id` in ascending order, and apply the `limit` and `offset` parameters for pagination.
4. **Output Format**:
   - First line must be the management chain formatted exactly as:
     `Chain: TopManagerName (TopDept) -> NextManagerName (NextDept) -> ... -> TargetName (TargetDept)`
   - Second line must be `Subordinates:`
   - Following lines must list the paginated subordinates formatted exactly as `ID | Name | Department`

Example output for `/home/user/get_network.sh 15 2 0`:
```
Chain: Alice Smith (Executive) -> Bob Jones (Engineering) -> Charlie Brown (Engineering)
Subordinates:
45 | Dave Davis | Engineering
82 | Eve Evans | QA
```

Constraints:
- Use `sqlite3` command-line tool within your bash script.
- Ensure the script is executable (`chmod +x`).
- Do not hardcode the data; your script must dynamically query `/home/user/company.db`.