You are a Database Administrator tasked with identifying communication bottlenecks within a company using a legacy SQLite database.

There is an SQLite database located at `/home/user/company.db`. You do not have documentation for the schema, so you must first reverse-engineer it by inspecting the tables. The database contains employee hierarchy information and an internal messaging log.

Your objective is to:
1. Identify the schema of the database.
2. Use a recursive SQL query (CTE) to extract the full reporting hierarchy under the root employee (the employee with no manager).
3. Project the messaging logs into a directed graph, where employees are nodes and a message sent represents a directed edge from the sender to the receiver.
4. Using Python and the `networkx` library, calculate the "betweenness centrality" for all employees in this messaging graph. (Treat the graph as directed, and use the default parameters for NetworkX's `betweenness_centrality` function).
5. Output the names of the top 3 employees with the highest betweenness centrality scores.

Write the names of these top 3 employees, in descending order of their centrality score, to `/home/user/bottlenecks.txt`. Each line should contain exactly one employee name.

You may write Python scripts and chain them with bash commands (e.g., using the `sqlite3` CLI tool) to accomplish this.