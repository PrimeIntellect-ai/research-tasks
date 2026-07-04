You are acting as a compliance officer auditing an internal corporate network. You need to verify if an employee, "Bob", has transitive access to sensitive systems through his team and network topology, and identify the most critical node in his accessible network.

You are provided with three files that represent different systems:
1. `/home/user/employees.csv` (Relational): Contains the corporate hierarchy. Columns are `emp_id, manager_id, name`. If `manager_id` is empty, they have no manager.
2. `/home/user/access.json` (Document): Contains direct server access mappings. Format: `[{"emp_id": 1, "servers": ["ServerA", "ServerB"]}, ...]`.
3. `/home/user/network.txt` (Graph edges): An adjacency list representing bidirectional network connections between servers. Each line contains two server names separated by a space (e.g., `ServerA ServerB`), meaning they can communicate with each other.

Your task is to write and execute a Python script (`/home/user/audit.py`) that performs the following:
1. **Hierarchical Resolution**: Recursively find "Bob" (emp_id=2) and all of his direct and indirect reports (anyone who rolls up to Bob in the hierarchy). Bob inherits "manager oversight" access, meaning his base access includes his own direct servers PLUS any servers accessible by all his recursive reports.
2. **Cross-Representation Mapping**: Use `access.json` to gather the complete initial set of servers Bob has base access to.
3. **Graph Traversal**: Using `network.txt` as an undirected graph, find the entire "reachable subgraph". A server is in the reachable subgraph if there is a path to it starting from ANY of Bob's base access servers.
4. **Graph Analytics**: Calculate the degree (number of connections) for each server *strictly within this reachable subgraph*.
5. **Output**: Find the server in the reachable subgraph with the highest degree. If there is a tie, pick the one that comes first alphabetically. 

Write the final result to `/home/user/audit_result.txt` in the exact format: `ServerName,Degree`. 
Do not include any other text or newlines in the file.