I need your help fixing our simulation pipeline for molecular network analysis. We have a multi-service setup that streams observational data from molecular graphs, but the current pipeline is broken and the Python-based analysis step is too slow.

Your task has two main parts:

**Part 1: Service Configuration (Integration)**
We have a set of services located in `/app/services/`. 
1. `redis-server`: Should run on the default port 6379.
2. `api.py`: A Python Flask API that acts as our simulation job queue controller.

Currently, `api.py` is misconfigured. It attempts to connect to Redis on port 6380, but Redis is running on 6379. Fix the configuration in `/app/services/config.json` so that the API connects to Redis correctly. 
Once configured, start both Redis and the API in the background. The API will listen on port 5000.
To verify this part, you must trigger a test job by running:
`curl -X POST http://localhost:5000/trigger_test`
This will automatically invoke your C binary (once compiled) and write the results to `/home/user/integration_output.txt`.

**Part 2: High-Performance C Implementation**
The core bottleneck is the molecular graph analysis algorithm. I have a reference binary at `/app/oracle_mol_analyze` (a stripped binary) that represents the exact behavior we need. You must write a C program at `/home/user/mol_analyze.c` that produces *bit-exact identical* output to this oracle, and compile it to `/app/bin/mol_analyze` (the API expects it here).

The algorithm calculates the average observation value for specific structural motifs (nodes with degree >= 2) in a molecular graph.
Input specification (read from Standard Input as space-separated integers):
- `V`: The number of vertices ($1 \le V \le 50$)
- `E`: The number of edges ($0 \le E \le 100$)
- The next $2E$ integers represent the edges. Each pair $(u, v)$ means an undirected edge between vertex $u$ and vertex $v$ ($0 \le u, v < V$).
- The final $V$ integers are the observational values (weights) for each vertex (integers between 0 and 1000).

Output specification (print to Standard Output):
- Calculate the degree of every vertex.
- Find all vertices that have a degree of 2 or more.
- Compute the sum of the observational values of these vertices, divided by the number of such vertices.
- Print this average as a truncated integer (floor division).
- If no vertices have a degree >= 2, output `0`.
- Do not print any trailing spaces or newlines other than a single `\n` at the end.

Example:
Input: `4 3 0 1 1 2 1 3 10 20 30 40`
Graph has 4 vertices, 3 edges: (0,1), (1,2), (1,3).
Degrees: node 0: 1, node 1: 3, node 2: 1, node 3: 1.
Vertices with degree >= 2: Node 1.
Node 1's observation value is 20. Average is 20. Output: `20\n`.

Write the C code, compile it to `/app/bin/mol_analyze`, fix the services, start them, and trigger the curl command.