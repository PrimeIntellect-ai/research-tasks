You are a Database Administrator and Data Engineer tasked with analyzing a company's internal communication network to identify key information bottlenecks and cross-departmental traffic patterns. 

An SQLite database containing the communication logs has been provided at `/home/user/company.db`. 

The database has the following schema:
- `departments` (id INTEGER PRIMARY KEY, name TEXT)
- `employees` (id INTEGER PRIMARY KEY, name TEXT, department_id INTEGER)
- `communications` (id INTEGER PRIMARY KEY, sender_id INTEGER, receiver_id INTEGER, bytes INTEGER, timestamp DATETIME)

Your task is to build a Go-based data pipeline that queries this database, constructs an in-memory graph, performs graph analytics, and outputs a final analytical report.

Instructions:
1. Initialize a Go module in `/home/user/analyzer/` and write your application in `/home/user/analyzer/main.go`. You will need to use an SQLite driver (e.g., `github.com/mattn/go-sqlite3`).
2. **Cross-Department Traffic (SQL Aggregation):** 
   Write a query with complex joins to calculate the total `bytes` transferred between every unique pair of departments. The communication is undirected for this aggregation (e.g., traffic from Engineering to Sales and Sales to Engineering should be summed together). 
   Represent the department pairs as a string formatted as `"DeptA-DeptB"` where `DeptA` comes alphabetically before `DeptB` (e.g., `"Engineering-Sales"`).
3. **Graph Construction & Centrality:**
   Query the database to build an undirected graph of employee communications. An edge exists between Employee A and Employee B if A sent a message to B, or B sent a message to A.
   Calculate the "Degree Centrality" for each employee, defined simply as the number of unique employees they have communicated with. Identify the top 3 employees with the highest degree centrality. If there is a tie in degree, order by employee ID ascending.
4. **Shortest Path:**
   Using the same undirected employee graph, implement a graph traversal algorithm to find the shortest path (minimum number of hops/edges) between employee ID `1` and employee ID `7`.
5. **Output Generation:**
   Your Go program must output the results as a strictly formatted JSON file at `/home/user/analyzer/report.json`. 

The JSON must exactly match this structure:
```json
{
  "cross_dept_traffic": {
    "Engineering-Sales": 1500,
    "Marketing-Sales": 800
  },
  "top_central_employees": [3, 4, 2],
  "shortest_path_1_to_7": [1, 3, 4, 7]
}
```
*(Note: The above values are placeholders, you must compute the actual values from the database).*

Ensure your Go code compiles, executes successfully, and accurately produces `/home/user/analyzer/report.json` with the correct calculations.