You are a data analyst working on a network analysis project. You have been given two headerless CSV files located in your home directory:
- `/home/user/entities.csv`
- `/home/user/connections.csv`

You need to reverse-engineer the data model to understand how these files relate, filter the network to a specific subset, and perform graph analytics.

Here is what you know about the data:
1. `entities.csv` contains information about network nodes. One column is an integer ID, another is a categorical string representing the entity type, and another is a string representing the entity's unique name.
2. `connections.csv` contains directed edges between entities. It includes the source ID, destination ID, and a numeric timestamp.
3. You must construct a directed graph where nodes are only those entities that have the category `'CORE'`. 
4. An edge should only be included in your graph if **both** its source and destination nodes are of category `'CORE'`.

Your task:
Write and execute a Python script that processes these CSV files, builds the directed graph using the `networkx` library, and calculates the PageRank of all nodes in this filtered graph using a damping factor (`alpha`) of `0.85`.

Find the name of the `'CORE'` entity with the highest PageRank score. 
Write exactly the **name** (just the string name, nothing else) of this entity to a file located at `/home/user/result.txt`.

Ensure your script is efficient. You may use standard libraries, `pandas`, and `networkx`.