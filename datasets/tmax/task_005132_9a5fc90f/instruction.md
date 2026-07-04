As a compliance officer auditing our internal systems for data exfiltration, I need your help building an automated detection pipeline. Our network security team has provided a visual recording of network topology changes and a corpus of network transaction logs.

Your task is to build a Rust application that processes this data to classify transaction logs as either normal or suspicious.

Here are the requirements:

1. **Topology Extraction (Video processing)**
   There is a video at `/app/topology_scan.mp4`. The video is exactly 30 frames long at 1 fps. Each frame contains a 20x20 grid of black and white pixels in the top-left corner (from x=0,y=0 to x=19,y=19). This grid represents an evolving unweighted, undirected adjacency matrix of our 20 core network routers (Index 0 to 19). A black pixel `(R=0, G=0, B=0)` at `(x, y)` means an edge exists between router `x` and router `y`. 
   Extract the frames and accumulate all edges that appear in *any* frame to build the complete static graph.

2. **Graph Analytics**
   Using the accumulated graph, compute the Degree Centrality for all 20 nodes. Identify the "High-Risk Hubs", defined as the top 3 nodes with the highest degree centrality. If there is a tie, prioritize the lower node index.

3. **Transaction Filtering (Adversarial Corpus)**
   You need to write a Rust command-line tool that acts as a filter. It must accept a path to a JSON file containing a sequence of transactions (a NoSQL-like aggregation pipeline dump).
   The JSON is an array of objects: `[{"tx_id": "...", "timestamp_sec": 12345, "router_id": 5, "bytes": 1024}, ...]`
   
   A log file is classified as an **Exfiltration Attempt (REJECT)** if BOTH of the following are true:
   - At least one transaction in the file passes through a "High-Risk Hub" (from step 2).
   - Using a sliding window of 60 seconds (i.e., `[t, t+60)`), the total bytes routed through ANY High-Risk Hub exceeds `10,000` bytes.
   
   If neither or only one condition is met, the log is **Normal (ACCEPT)**.

4. **Integration & Deliverable**
   Create a Rust project at `/home/user/detector`. 
   The compiled binary `target/release/detector` must take two arguments:
   `./detector --video /app/topology_scan.mp4 --log <path_to_json>`
   
   It must output exactly one line to `stdout`:
   `REJECT` (if it's an exfiltration attempt)
   `ACCEPT` (if it's normal traffic)

We have a test suite that will run your binary against two directories: `/app/corpus/evil/` (which must all return `REJECT`) and `/app/corpus/clean/` (which must all return `ACCEPT`). 
Please write and compile the Rust application to meet these specifications.