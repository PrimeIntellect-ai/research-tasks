You are a Database Reliability Engineer investigating a performance and data correctness issue in our backup validation pipeline. 

Our system uses a PostgreSQL database to store network topology data (nodes and edges). As part of a nightly job, a SQL query extracts the network graph to a CSV, which is then processed by a C++ analytics engine to compute the Closeness Centrality of all nodes. 

Recently, the job has been timing out and producing incorrect results. We suspect two issues:
1. The extraction query (`/home/user/app/query.sql`) has an implicit cross join that is exploding the number of edges and returning duplicate/invalid paths.
2. The C++ analytics engine (`/home/user/app/analyze_graph.cpp`) is using a highly inefficient algorithm (currently O(V^3) or worse) to compute closeness centrality.

Your tasks are:
1. **Start the services**: We have a multi-service setup (PostgreSQL and Redis). Start them using the provided `docker-compose.yml` or startup script in `/home/user/app/`. 
2. **Fix the SQL Query**: Modify `/home/user/app/query.sql`. It is supposed to select `source_id` and `target_id` for all active edges in the `network_edges` table, joining with `network_nodes` to ensure both the source and target nodes are marked as `is_active = true`. Fix the cross join so it only returns valid, active edges without duplicates.
3. **Optimize the C++ Graph Processing**: Rewrite the Closeness Centrality calculation in `/home/user/app/analyze_graph.cpp`. It currently parses the CSV output of the SQL query. You need to implement an efficient O(V(V+E)) algorithm using Breadth-First Search (BFS) for unweighted shortest paths.
4. **Integration**: The C++ program should output the node ID and its centrality score to a file named `/home/user/results.csv`, formatted as `node_id,centrality_score`.

**Constraints & Requirements:**
- The graph is unweighted and directed.
- Closeness Centrality for a node `u` is defined as `(N-1) / sum(d(u, v))` where `N` is the number of reachable nodes (including `u`) and `d(u,v)` is the shortest path distance. If a node cannot reach any other nodes, its centrality is 0.
- The C++ program must be compiled to an executable at `/home/user/app/analyze`.
- The execution time of your C++ program on the extracted data must be strictly less than 1.5 seconds.