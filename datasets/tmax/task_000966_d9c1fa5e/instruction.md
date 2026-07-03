You are a data analyst investigating a network topology. You've received a voice memo from a field engineer that dictates the connections in a newly discovered network cluster.

Your tasks are:
1. **Transcribe the Graph**: Listen to (or programmatically transcribe) the audio file located at `/app/network.wav`. The engineer dictates a series of directed edges as pairs of numbers (Source Destination). Convert this into a CSV file at `/home/user/network.csv` with the exact headers `Source,Destination`.
2. **Build a C++ Query Engine**: Write a C++ program at `/home/user/query.cpp` and compile it to `/home/user/query`.
3. **Program Specifications**:
   - The program must accept exactly one command-line argument: the path to the CSV file.
   - It should parse the CSV and build an in-memory graph. Even though the dictation implies directed edges, treat all connections as **undirected** for the purposes of querying.
   - It should then read pairs of integer node IDs from `stdin` (two space-separated integers per line) until `EOF`.
   - For each pair of nodes, compute the shortest path distance (number of edges) between them.
   - Print the resulting integer distance to `stdout` (one per line). If the nodes are the same, the distance is 0. If no path exists between them, print `-1`.

Ensure your C++ code is robust and handles standard edge cases. We will rigorously test your compiled `/home/user/query` binary against an automated test suite that feeds it hundreds of random node pairs.