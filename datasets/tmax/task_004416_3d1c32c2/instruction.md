You are tasked with analyzing an organization's communication and reporting structure to optimize information flow. You have been provided with an SQLite database at `/home/user/company.db` containing two tables: `employees` (id, name, manager_id) and `messages` (sender_id, receiver_id).

Information can flow between two employees through two types of connections:
1. **Hierarchy (Undirected):** An employee can communicate directly with their manager, and a manager can communicate directly with their direct reports.
2. **Messages (Directed):** An employee can send information to anyone they have previously sent a message to (represented in the `messages` table as sender to receiver).

Your task is to write a Python script at `/home/user/analyze_path.py` that maps this relational data into a graph representation and computes the shortest path length for information to flow from the employee named "Alice" to the employee named "Bob". 

Each valid connection (either a hierarchy link or a directed message link) counts as a distance of 1. 

Once your script calculates the shortest path length (an integer), it must write this integer to a file located at `/home/user/result.txt`.

Requirements:
- Use Python. The `networkx` library is available if you wish to use it.
- Your output file `/home/user/result.txt` must contain only the integer representing the shortest path length.
- Ensure your script reads from `/home/user/company.db`.