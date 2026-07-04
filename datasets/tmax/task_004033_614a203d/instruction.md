You are acting as an AI assistant to a compliance officer auditing an organization's IT access control systems. 

We suspect there is a critical compliance violation where a low-level employee has an unauthorized access path to a highly sensitive financial system due to a misconfigured role inheritance chain. 

I have exported the current access control list and identity matrix into two CSV files located at:
1. `/home/user/nodes.csv` (Columns: `node_id,node_type,name`)
2. `/home/user/edges.csv` (Columns: `source_id,target_id,edge_type`)

Your task is to:
1. Inspect these CSV files to understand the graph data model (identifying how Employees, Roles, and Systems are linked via `HAS_ROLE`, `ROLE_INHERITS`, and `CAN_ACCESS` edges).
2. Write a C++ program at `/home/user/audit.cpp` that parses these files, constructs a directed graph, and computes the shortest path from the Employee named "Intern_Bob" to the System named "Financial_DB_Prod".
3. Compile your program using standard C++17 (`g++ -std=c++17 /home/user/audit.cpp -o /home/user/audit`) and execute it.
4. Your C++ program must write the result to a log file at `/home/user/violation_path.txt`. The output must be exactly the comma-separated sequence of `node_id`s representing the shortest path, on a single line (e.g., `N1,N8,N12,N5`). If no path exists, write `NONE`.

Please identify the vulnerability path so we can patch the role definitions immediately.