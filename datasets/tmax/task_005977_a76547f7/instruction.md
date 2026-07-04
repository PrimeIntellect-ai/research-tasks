You are a data analyst tasked with processing a snapshot of a company's organizational knowledge graph. You have been provided with two CSV files containing the exported graph data:
1. `/home/user/data/nodes.csv` - Contains information about employees.
2. `/home/user/data/edges.csv` - Contains relationships between employees.

Your task is to write a Rust application that processes these CSV files to determine which department has the highest average "in-degree" centrality for the `reports_to` relationship.

Perform the following steps:
1. Initialize a new Rust project in `/home/user/graph_analyzer`.
2. Write a Rust program that reads both CSV files. You must infer the schema from the CSV headers.
3. Your Rust program must create an SQLite database at `/home/user/data/graph.db` with appropriate `nodes` and `edges` tables.
4. Insert the data from the CSV files into the SQLite database. You *must* use parameterized SQL queries to insert the records to prevent SQL injection and handle escaping properly.
5. Once the data is loaded, write and execute a SQL query (or a combination of SQL and Rust logic) to calculate the average in-degree of `reports_to` edges for each department. (The in-degree of a node is the number of `reports_to` edges where that node is the `target`). The average for a department is the total in-degree of all nodes in that department divided by the total number of nodes in that department.
6. Identify the department with the highest average in-degree.
7. Write the result to `/home/user/data/top_department.txt` in the exact format: `DepartmentName,AverageValue`. The average value must be formatted to exactly two decimal places (e.g., `Sales,1.50`).

Constraints:
- Use Rust as the primary programming language for reading, database creation, and querying.
- You may use external crates like `csv` and `rusqlite`.
- Ensure the database file `/home/user/data/graph.db` is successfully created and populated before your program exits.