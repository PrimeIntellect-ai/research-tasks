You are a database administrator tasked with optimizing and extracting data from a backend system. We have an SQLite database at `/home/user/system.db` that represents a graph of services, but it stores properties as JSON documents within a relational schema.

Your task is to write a C++ program at `/home/user/query_tool.cpp` that queries this database to find specific dependency paths. 

The database contains two tables. You will need to reverse engineer their exact schema using the SQLite CLI, but conceptually:
1. An entity table containing nodes, their type, and a JSON string of metadata.
2. A link table representing directed edges between nodes with an associated cost.

Write a C++ program that meets the following requirements:
1. Connects to `/home/user/system.db`.
2. Executes a single, optimized SQL query to find all 'endpoint' nodes that are exactly 2 hops away from a given starting node (i.e., `StartNode -> IntermediateNode -> EndpointNode`).
3. Extracts the `"version"` string from the JSON metadata of the destination `EndpointNode`.
4. Calculates the total cost of the path (the sum of the cost of the two edges).
5. Orders the results by the total path cost in DESCENDING order, limiting the output to the top 5 results.
6. **Crucial:** Your C++ code MUST use a parameterized query for the starting node ID (bind the value using `sqlite3_bind_*`). Do not hardcode the starting node ID directly into the SQL string.
7. The starting node ID to bind for this run should be `10`.
8. The program should write the output to `/home/user/results.txt`. Each line must follow exactly this format:
   `<EndpointNodeID>,<Version>,<TotalCost>`
   (Format the TotalCost to exactly 1 decimal place, e.g., `25.0`).

You can compile your program using:
`g++ -O3 /home/user/query_tool.cpp -lsqlite3 -o /home/user/query_tool`

Execute your program so that `/home/user/results.txt` is populated correctly.