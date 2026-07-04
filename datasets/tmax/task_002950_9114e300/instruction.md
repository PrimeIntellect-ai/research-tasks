You are assisting a compliance officer who is auditing system access. You have been provided with an SQLite database file at `/home/user/audit.db`. You do not have documentation for the schema, so you must explore the database to understand its structure. 

Your objective is to generate an audit report of all employees who have accessed the resource named `SECRET_VAULT`.

Specifically, you need to write and execute an SQLite query (or a bash script containing the query) that creates a CSV report at `/home/user/audit_results.csv` meeting the following requirements:
1. Include a header row: `employee,access_time,top_manager`
2. `employee`: The name of the user who accessed the `SECRET_VAULT`.
3. `access_time`: The *earliest* time this user accessed the `SECRET_VAULT`.
4. `top_manager`: The name of the user at the very top of this employee's reporting chain (i.e., the ancestor in the hierarchy who does not report to anyone). If the employee does not report to anyone, they are their own top manager.
5. The rows must be ordered alphabetically by the `employee` name.

You must accomplish this using the `sqlite3` command-line tool. Evaluate the tables, write a query using recursive CTEs to traverse the management hierarchy, and extract the earliest access using appropriate aggregation or window functions.