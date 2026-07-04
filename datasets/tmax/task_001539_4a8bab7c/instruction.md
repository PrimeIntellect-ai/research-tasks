You are a data analyst tasked with processing an append-only CSV event log representing the evolving topology of a communication network. 

The file is located at `/home/user/network_events.csv`. 
Because of a bug in the logging system, the file contains unordered events representing edge additions and removals. The schema of the CSV is unknown, but you can reverse engineer it by inspecting the file. We know it contains a timestamp, two node IDs, and an event type indicating whether the connection was established or broken.

Your goal is to determine the current, active state of the network graph and identify the most critical nodes.
The graph is undirected (an edge between A and B is the same as B and A). 
An edge is considered "active" if the chronologically latest event (by timestamp) between those two nodes is a connection establishment, rather than a disconnection.

Write a C++ program at `/home/user/analyze_graph.cpp` that reads the CSV, reconstructs the active graph, and calculates the degree centrality (number of active edges) for each node.

Then, output the top 5 nodes with the highest degree centrality into a file at `/home/user/top_nodes.txt`.
The file should contain exactly 5 lines, formatted as:
`<node_id>,<degree>`

Requirements:
- Sort the top 5 nodes by degree in descending order.
- If there is a tie in degree, break the tie by sorting the `node_id` in ascending order.
- You must write and compile a C++ program (`g++`) to perform the core logic. 
- You can use standard bash tools to inspect the data and assist in the pipeline.