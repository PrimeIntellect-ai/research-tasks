You are a data analyst investigating a series of pipeline failures. A downstream analytical service is crashing because certain input CSV files contain "malicious" edge lists. These edge lists contain structures that result in an implicit cross-join during downstream graph materialization (specifically, dense bipartite subgraphs where the number of cross-edges exceeds 50).

Your task is to create a robust data querying and filtering pipeline in Rust that acts as a middleware service. 

First, look in `/home/user/app/`. You will find:
- A `clean_corpus/` directory containing valid CSV edge lists (`source,target,weight`).
- An `evil_corpus/` directory containing CSV edge lists designed to trigger combinatorial explosions (implicit cross-joins).
- A `start_services.sh` script that brings up two background services:
  1. A Data Emitter (TCP port 8001): Sends file paths to process.
  2. A Data Sink (TCP port 8002): Expects to receive JSON lines of processed graph analytics.

You must build a Rust application in `/home/user/app/filter_service/` (initialize it with `cargo init`) that does the following:
1. Connects to port 8001 to read CSV file paths (one per line).
2. For each file, parses the edge list and projects it into a graph in memory.
3. Analyzes the graph for implicit cross-joins. Specifically, if the graph contains any node that shares outgoing edges to the exact same set of 10 or more target nodes as 5 or more other source nodes (a bipartite subgraph $K_{m,n}$ where $m \ge 5$ and $n \ge 10$), the file is deemed "evil" and must be completely REJECTED (do not send anything to the sink, print "REJECTED: <filepath>" to stdout).
4. If the graph is clean, compute the shortest path from node ID "0" (if it exists) to all other nodes. 
5. Calculate a windowed aggregation: Rank the reachable nodes based on their shortest path distance from node "0" (dense rank).
6. Send the accepted results to the Data Sink on port 8002 in the following JSON Lines format:
   `{"file": "<filepath>", "node": "<id>", "distance": <dist>, "rank": <rank>}`

To complete the task:
- Write the Rust tool.
- Run `start_services.sh`.
- Execute your Rust service so it bridges port 8001 and 8002.
- The verifier will automatically test your tool against both the clean and evil corpora. Your tool must successfully preserve 100% of the clean corpus and reject 100% of the evil corpus.