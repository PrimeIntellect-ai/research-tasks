You are assisting a compliance officer who is auditing an internal corporate network. We have an undocumented SQLite database located at `/home/user/audit.db` which contains access logs, but the original schema documentation has been lost. The compliance team suspects there are anomalous access patterns and needs you to analyze the data.

Your task consists of three phases:

1. **Schema Analysis & Data Model Reverse Engineering**
   Explore the SQLite database `/home/user/audit.db`. You will need to identify the tables and infer the relationships between employees, systems, and access events. Look for primary keys and foreign key relationships (even if they are only implied by column names like `e_id` or `sys_id`). 

2. **Graph Construction**
   Using Python, write a script to construct a bipartite directed graph representing the access patterns. 
   - Nodes should be the individual Employees and Systems.
   - Directed edges should go from an Employee to a System if there is at least one access event.
   - You may need to install standard graph analytics libraries (e.g., `networkx`) using `pip`.

3. **Graph Analytics**
   Calculate the following metrics on the network:
   - **Out-Degree Centrality** for Employees (to find who accesses the most unique systems).
   - **PageRank** for Systems (to identify the most central/critical systems based on who accesses them). Use the default parameters for PageRank in `networkx` (alpha=0.85).

**Final Output Requirement:**
Create a JSON file at `/home/user/compliance_report.json` containing exactly the IDs of the top employee (highest out-degree centrality) and the top system (highest PageRank). 

The JSON must exactly match this format:
```json
{
  "top_employee_id": <integer>,
  "top_system_id": <integer>
}
```
If there is a tie, pick the one with the lowest ID.