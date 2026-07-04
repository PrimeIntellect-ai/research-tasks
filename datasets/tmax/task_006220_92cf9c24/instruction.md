You are a database administrator tasked with optimizing and analyzing a network routing database. A legacy application relies on finding high-bandwidth, 3-hop cyclic pipelines in our system, but the current implementation is too slow. You need to write a Python script to perform this analysis efficiently using database queries and data aggregation.

We have a SQLite database located at `/home/user/network.db`. It contains a single table named `links` with the following schema:
- `src` (INTEGER): The ID of the source node.
- `dst` (INTEGER): The ID of the destination node.
- `bandwidth` (INTEGER): The available bandwidth on this directed link.

Your objective is to write and execute a Python script (`/home/user/analyze_cycles.py`) that does the following:
1. Queries the database to find all unique directed 3-hop cycles. A 3-hop cycle is a path of exactly 3 nodes that loops back to the start (e.g., A -> B -> C -> A). 
2. Ensure that each unique cycle (the set of 3 nodes) is only processed once, regardless of which node is considered the "start" of the cycle.
3. Calculates the "bottleneck bandwidth" for each cycle, which is defined as the minimum `bandwidth` among the three links that make up the cycle.
4. Aggregates the data by calculating the total sum of bottleneck bandwidths for every node. If a node participates in multiple distinct cycles, its total is the sum of the bottleneck bandwidths of all cycles it is a part of.
5. Exports the final aggregated result to a JSON file at `/home/user/bottleneck_report.json`. The JSON should be a dictionary mapping the node IDs (as strings) to their total aggregated bottleneck bandwidth (as integers). Only include nodes that have a total aggregated bandwidth greater than 0.

Example of aggregation:
If node 1 is in a cycle (1->2->3->1) with a bottleneck of 5, and another cycle (1->4->5->1) with a bottleneck of 10, the output for node "1" should be 15.

Write the script, execute it, and ensure `/home/user/bottleneck_report.json` is generated correctly.