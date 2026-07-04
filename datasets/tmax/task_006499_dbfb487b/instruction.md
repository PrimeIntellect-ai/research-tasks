You are a data analyst tasked with reverse-engineering an implicit organizational influence graph from raw CSV exports. You have been provided with two files located in your home directory:

1. `/home/user/employees.csv`
   Columns: `emp_id` (integer), `name` (string), `manager_id` (integer, can be empty)
2. `/home/user/communications.csv`
   Columns: `sender_id` (integer), `receiver_id` (integer), `timestamp` (ISO8601 string), `bytes` (integer)

Your task is to write a Go program (`/home/user/analyze.go`) that performs the following operations:

1. **Database Initialization & Data Loading:**
   Read the two CSV files and load them into an in-memory SQLite database. You will need to initialize a Go module and fetch the `github.com/mattn/go-sqlite3` driver.

2. **Analytical Aggregation & Window Functions:**
   Using SQL within your Go program, calculate an "Influence Score" for each employee.
   The formula for the Influence Score is: 
   `(Number of direct subordinates * 2) + (Number of DISTINCT receivers the employee sent messages to)`.
   
   Using an SQL Window Function (`DENSE_RANK()`), rank the employees based on their Influence Score in descending order.

3. **Output Reporting:**
   Write the top 3 employees based on this rank to a file named `/home/user/report.csv`.
   Format: `emp_id,name,score,rank`
   (Do not include a header row, just the data).

4. **Cypher Graph Generation:**
   To facilitate further graph analytics in a Neo4j database, your Go program must generate a valid Cypher script saved to `/home/user/import.cypher`.
   The script must contain the exact following statements based on the data:
   - For every employee: `CREATE (:Employee {emp_id: <id>, name: '<name>'});`
   - For every subordinate to manager relationship: `MATCH (sub:Employee {emp_id: <sub_id>}), (mgr:Employee {emp_id: <mgr_id>}) CREATE (sub)-[:REPORTS_TO]->(mgr);`
   - For every distinct sender-receiver pair in the communications log: `MATCH (s:Employee {emp_id: <sender_id>}), (r:Employee {emp_id: <receiver_id>}) CREATE (s)-[:COMMUNICATED_WITH]->(r);`
   
   Ensure the statements are grouped (all Employee nodes first, then REPORTS_TO edges, then COMMUNICATED_WITH edges), with each statement on a new line.

Write, compile, and execute the Go program to produce `/home/user/report.csv` and `/home/user/import.cypher`.