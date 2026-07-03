You are assisting a compliance officer auditing an organization's IT infrastructure for unauthorized indirect access to restricted servers. You have been provided with materialized graph data representing access permissions and network reachability. 

Your task is to write a C program that builds an in-memory database, performs a recursive hierarchical query to map all direct and indirect access paths, and summarizes the findings.

**Inputs:**
1. `/home/user/access_graph.csv`: Contains the directed edges of the access graph. 
   Format: `source_node,target_node`
   (e.g., `USR_Alice,GRP_Admin` means Alice is in GRP_Admin. `GRP_Admin,SRV_DB` means the Admin group has access to SRV_DB).
2. `/home/user/restricted_systems.csv`: Contains a list of highly restricted systems.
   Format: `system_name`

**Requirements:**
1. Write a C program at `/home/user/audit_tool.c`.
2. The program must use the SQLite3 C API (`sqlite3.h`) to create an in-memory database (`:memory:`).
3. Read the two CSV files and populate appropriate tables.
4. Execute a `WITH RECURSIVE` SQL query to traverse the access graph starting from all nodes prefixed with `USR_`. 
5. Find all reachable nodes for each user.
6. Cross-reference the reachable nodes with the restricted systems list.
7. Aggregate the data: For each user, count the total number of *distinct* restricted systems they can reach (either directly or via multiple hops).
8. Write the results to `/home/user/compliance_report.csv` in the following format:
   `User,RestrictedAccessCount`
9. Only include users whose `RestrictedAccessCount` is greater than 0.
10. Order the output descending by `RestrictedAccessCount`, then alphabetically by `User`.
11. Compile your program to `/home/user/audit_tool` (e.g., using `gcc /home/user/audit_tool.c -o /home/user/audit_tool -lsqlite3`) and execute it to generate the report.

*Note: Ensure the standard `libsqlite3-dev` package is installed in your environment if it isn't already.*