You are a database administrator tasked with extracting hierarchical data from an SQLite database and transforming it into a structured document format.

You have been provided with an SQLite database at `/home/user/company.db` containing two tables:
1. `employees` (`id` INTEGER PRIMARY KEY, `name` TEXT, `manager_id` INTEGER)
2. `salaries` (`employee_id` INTEGER, `salary` INTEGER)

Your objective is to write a Python script at `/home/user/analyze_org.py` that performs the following tasks:
1. Connects to `/home/user/company.db`.
2. Uses a recursive Common Table Expression (CTE) in SQL to find the employee named "Evelyn" and all her direct and indirect subordinates (the entire sub-organization under Evelyn).
3. Calculates the total combined salary of Evelyn and all her subordinates. The script should print ONLY this total integer value to standard output.
4. Constructs a nested JSON document representing Evelyn's organizational chart, merging relational data from both tables. The JSON structure for each employee must be:
   ```json
   {
     "name": "EmployeeName",
     "salary": 50000,
     "reports": [ ... ]
   }
   ```
   - If an employee has no subordinates, their `reports` list should be empty `[]`.
   - The `reports` list must be sorted alphabetically by the `name` of the subordinates.
5. Saves this JSON document to `/home/user/evelyn_org.json` with an indentation of 2 spaces.

Make sure the script is standalone and works entirely via the standard library `sqlite3` and `json` modules.