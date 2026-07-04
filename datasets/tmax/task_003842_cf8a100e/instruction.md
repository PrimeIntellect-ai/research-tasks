You are an expert data analyst and systems programmer. You need to process a dataset of network interactions and compute graph analytics using C.

You have been given a dataset containing graph edges in `/home/user/edges.csv`. The file has no header and contains comma-separated integer pairs representing directed edges (`source_node,target_node`). 

Additionally, you have received an audio memo from the lead data scientist at `/app/schema_instructions.wav`. You must transcribe this audio (you may use `ffmpeg` and `whisper` or any available speech-to-text tools in your environment) to retrieve the exact parameters required for the PageRank algorithm.

Your task is to:
1. Listen to / transcribe the audio file `/app/schema_instructions.wav` to find the required **damping factor** and the **number of iterations**.
2. Write a highly optimized C program (`/home/user/pagerank.c`) that:
   - Reads the `/home/user/edges.csv` file and constructs an efficient in-memory graph representation (e.g., adjacency list with index arrays).
   - Identifies the total number of unique nodes $N$ present in the edge list.
   - Initializes the PageRank of every node to $1.0 / N$.
   - Computes the PageRank for all nodes for the exact number of iterations specified in the audio, using the specified damping factor $d$.
   - **Crucially**, handles "dangling nodes" (nodes with an out-degree of 0). The PageRank mass of dangling nodes must be distributed evenly among all $N$ nodes in the network during each iteration.
   - The standard PageRank formula to apply per iteration is: 
     $PR(i) = \frac{1 - d}{N} + d \left( \sum_{j \in M(i)} \frac{PR(j)}{L(j)} \right) + d \frac{\sum_{k \in D} PR(k)}{N}$
     where $M(i)$ is the set of nodes linking to $i$, $L(j)$ is the out-degree of node $j$, and $D$ is the set of dangling nodes.
   - Writes the final PageRank values to `/home/user/pagerank_output.csv`.
3. The output file `/home/user/pagerank_output.csv` must contain the results sorted by `node_id` in ascending order. The format of each line must be `node_id,pagerank_value` (print floating-point values to 9 decimal places using `%.9f`).

Compile your C program with `gcc -O3 /home/user/pagerank.c -o /home/user/pagerank` and execute it. Your program must be efficient and run within a few seconds.

The automated verifier will calculate the Mean Squared Error (MSE) between your output and the true expected PageRank values. You must achieve an MSE of less than `1e-12`.