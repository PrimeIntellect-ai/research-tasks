You are an expert data engineer. We have a proprietary local graph database engine provided as a stripped binary at `/app/graph_daemon`. This daemon listens on a Unix domain socket `/tmp/graph.sock` when started. 

We need you to build a C++ ETL service that exposes an HTTP REST API to query this graph database and export the results. 

Your tasks are:
1. Figure out how to start the `/app/graph_daemon` binary so it listens on `/tmp/graph.sock` and initialize it with the graph dataset provided at `/home/user/data.csv` (an edge list).
2. The daemon accepts a custom binary protocol. You will need to reverse-engineer the query format. It supports recursive graph traversals but is prone to deadlocks if concurrent transactions query intersecting subgraphs in different orders.
3. Write a C++ HTTP server that listens on `127.0.0.1:9090`. It must accept `GET /traverse?start_node=<id>&depth=<d>` requests.
4. Your C++ service must construct the parameterized query, send it to the daemon over the Unix socket, and return the result as a JSON array of node IDs.
5. Implement a retry mechanism in your C++ service to handle the "DEADLOCK_DETECTED" response (which the daemon returns as the byte `0xFF`) by backing off and retrying.
6. The service must require a Bearer token `secret-etl-token` in the `Authorization` header.

Compile your C++ service to `/home/user/etl_service` and leave it running in the background. Write a bash script `/home/user/start.sh` that starts both the daemon and your service.