You are acting as a data analyst and C developer tasked with processing a dataset of network routing logs. 

We have a network dataset located at `/home/user/network.csv`. The file is a CSV without a header, containing millions of edges in the format:
`SourceNodeID,TargetNodeID,LatencyMS`
(All values are non-negative integers. The graph is directed).

Your senior engineer left a voicemail at `/app/voicemail.wav` detailing a specific custom aggregation and filtering logic that must be applied to the edge weights before routing queries are processed. You will need to transcribe this audio file to find out what the business rules are.

Your goal is to build an extremely fast in-memory query engine in C that implements these rules.

Create a C program at `/home/user/query_engine.c` and compile it to `/home/user/query_engine`.
The program must behave as follows:
1. Accept the CSV file path as its first command-line argument (e.g., `./query_engine /home/user/network.csv`).
2. Load the graph into memory, applying the exact filtering and weight-adjustment rules specified in the voicemail.
3. Build an efficient index/adjacency list for fast graph traversal.
4. Listen on standard input (`stdin`) for query pairs. Each line of input will contain two integers separated by a space: `StartNode EndNode`.
5. For each query, calculate the shortest path based on the adjusted latencies using Dijkstra's algorithm.
6. Print the total shortest path latency to standard output (`stdout`), followed by a newline. If no path exists, print `-1`. 

Your program must process `stdin` until EOF. Performance is critical. Do not print any debug information or prompts to `stdout`—only the integer results.

Note: You may need to install transcription tools (like Python's `SpeechRecognition` or `whisper`) to process the audio file. You have sudo-less root in this environment or can install user packages.