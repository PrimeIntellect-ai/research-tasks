You are acting as a data engineer to fix a broken data pipeline. 

We have a multi-service architecture running locally:
1. **Graph API (Flask)** running on `127.0.0.1:5000`. It serves graph adjacency lists. Endpoint `/neighbors/<node_id>` returns a JSON list of neighbor integer IDs.
2. **Event Stream (TCP Service)** running on `127.0.0.1:5001`. When connected, it streams CSV data representing events: `event_id,node_id,value,timestamp`.

Currently, we have a C++ program located at `/home/user/pipeline/aggregator.cpp`. This program reads node IDs from `stdin` (one per line). For each node ID, it is supposed to:
1. Fetch the node's neighbors from the Graph API.
2. Fetch the latest events from the Event Stream (by sending a `PULL` command and reading the CSVs).
3. Compute a rolling sum (window function) of the `value` field for events belonging to the *neighbors* of the queried node, sorted by timestamp.

**The Problem:** 
The current C++ implementation contains a critical logical bug. Instead of joining the events correctly to the specific neighbors, it performs an implicit cross-join in its internal processing loop, causing the rolling sums to be massively inflated and duplicated.

**Your Objectives:**
1. Fix the bug in `/home/user/pipeline/aggregator.cpp`. The rolling sum must correctly partition by `node_id` and order by `timestamp`, only including events for the neighbors of the queried node.
2. Compile the fixed program to `/home/user/pipeline/aggregator`. (Use `g++ -O2 -std=c++17 -lcurl -lpthread`)
3. Write a shell script `/home/user/pipeline/start_services.sh` that starts the two services (their source code is in `/app/services/graph_api.py` and `/app/services/event_tcp.py`) and waits for them to be healthy.

**Output Format:**
For each node ID provided on `stdin`, your compiled C++ program must output to `stdout`:
`Query: <node_id> | Rolling Sums: [val1, val2, ...]`

A reference binary is available at `/app/oracle_aggregator`. Your compiled program must produce **bit-exact identical** output to the oracle for any sequence of node IDs. Do not modify the oracle.