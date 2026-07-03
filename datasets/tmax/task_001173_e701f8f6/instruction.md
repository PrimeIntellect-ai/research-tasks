You are assisting a data researcher in organizing a fragmented network of academic datasets and publications. The data is currently split across two legacy microservices that you need to integrate and analyze. 

Your objective is to build a unified C++ API server that ingests data from these services, reverse-engineers the graph schema, computes essential graph analytics, and serves results via a custom HTTP API.

### Environment & Setup
A startup script is available at `/app/services/start_services.sh`. When executed, it brings up two local data sources:
1. **Metadata Service (HTTP, port 9001)**: 
   Exposes `GET /metadata`. Returns a JSON array of nodes. Each node has an `"id"` (integer) and a `"type"` (string: "Dataset", "Paper", or "Author").
2. **Topology Service (Raw TCP, port 9002)**: 
   When you connect via TCP, it streams the graph edges as plain text: `source_id,target_id\n`, then closes the connection. All edges are undirected and unweighted.

Single-header C++ libraries for HTTP and JSON are pre-installed in `/home/user/deps/`:
- `httplib.h` (cpp-httplib)
- `json.hpp` (nlohmann/json)

### Your Tasks

**1. Data Ingestion & Model Reverse Engineering**
Write a C++ program that fetches the node metadata from port 9001 and the edge topology from port 9002. Construct an undirected in-memory graph. 

**2. Graph Analytics**
Your C++ server must compute:
- **Degree Centrality:** The number of edges connected to a node.
- **Connected Components:** Identify which connected component each node belongs to, and compute the size of that component.

**3. API Implementation**
Your C++ program must run an HTTP server listening on `127.0.0.1:8080`. It must expose the following endpoints:

- `GET /analytics/degree?node=<id>`
  Returns JSON: `{"node": <id>, "degree": <int>}`

- `GET /analytics/component_size?node=<id>`
  Returns JSON: `{"node": <id>, "component_size": <int>}` (The total number of nodes in the connected component that contains this node).

- `POST /query`
  Accepts a JSON payload representing a simplified graph query:
  `{"query": "MATCH (a)-[]-(b) WHERE a.id = <id> AND b.type = '<type>' RETURN b.id"}`
  *Example:* `{"query": "MATCH (a)-[]-(b) WHERE a.id = 42 AND b.type = 'Dataset' RETURN b.id"}`
  
  Parse this exact string format. Find all neighbors (`b`) of the specified node (`a`) that have the specified `type`.
  Returns JSON: `{"results": [<b.id_1>, <b.id_2>, ...]}` (sorted in ascending order).

Compile your C++ server to `/home/user/graph_server` and ensure it is running in the background when you complete your task.