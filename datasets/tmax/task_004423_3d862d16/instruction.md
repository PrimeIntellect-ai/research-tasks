You are an AI assistant helping a Compliance Officer audit an internal corporate network for suspicious information flow. We suspect that certain employees are acting as unauthorized information brokers. 

You need to write a C++ tool that analyzes internal communications from a SQLite database, identifies key persons of interest using a graph centrality metric, and outputs a paginated, sorted report.

Here are the details:
The database is located at `/home/user/corp_data.db`.
It has two tables:
1. `employees` (id INTEGER PRIMARY KEY, name TEXT, department TEXT)
2. `communications` (id INTEGER PRIMARY KEY, sender_id INTEGER, receiver_id INTEGER, timestamp TEXT, sensitivity_level INTEGER)

Write a C++ program at `/home/user/audit_tool.cpp` that does the following:
1. **Index Strategy**: Connects to the SQLite database and executes SQL statements to create the following indexes (if they don't exist) to optimize our queries:
   - `idx_comm_filter` on `communications (sensitivity_level, timestamp)`
   - `idx_comm_edges` on `communications (sender_id, receiver_id)`
2. **Parameterized Query & Filtering**: Prepares a parameterized query to find all communications where `sensitivity_level >= ?` AND `timestamp` is between `'2023-01-01 00:00:00'` and `'2023-12-31 23:59:59'`. The `?` should be bound to a command-line argument.
3. **Graph Analytics & Aggregation**: For this filtered subset of communications, calculate the In-Degree (number of messages received) and Out-Degree (number of messages sent) for every employee involved. Then, compute their "Broker Score", defined as `(In-Degree * Out-Degree)`.
4. **Result Sorting & Pagination**: Cross-reference the results with the `employees` table to get the names and departments. Sort the results primarily by Broker Score in DESCENDING order, and secondarily by Employee Name in ASCENDING order. Limit the output to the top `N` records (where `N` is provided as a command line argument).
5. **Output**: Write the final results to `/home/user/audit_report.csv` including a header row. Format: `EmployeeID,Name,Department,InDegree,OutDegree,BrokerScore`.

Your program should be compiled to `/home/user/audit_tool` and must take exactly two integer arguments:
`./audit_tool <min_sensitivity> <limit>`

For example: `./audit_tool 4 5`

You will need to install the SQLite3 C++ development libraries to compile your code. Once you have written and compiled the program, execute it with `<min_sensitivity> = 3` and `<limit> = 3`. 
Ensure the output file `/home/user/audit_report.csv` is correctly generated.