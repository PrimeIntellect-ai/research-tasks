You are a Database Reliability Engineer handling a critical recovery operation. Our primary custom graph database crashed, and we only have a raw binary backup file located at `/app/backup.dat`. The original database software is lost, but we recovered a standalone, stripped query tool located at `/app/graph_engine`.

Your task is to reconstruct the graph data and prioritize which data fragments to restore first by calculating node importance.

1. **Data Model Extraction:** The `/app/graph_engine` binary is a stripped, black-box executable. By reverse-engineering its behavior or treating it as an oracle, extract the complete edge list of the graph from `/app/backup.dat`. It is known that the graph contains exactly 10,000 nodes, with IDs ranging from 0 to 9999.
2. **Query Pipeline:** Chain standard bash utilities to dump the entire graph topology into a plain text format (e.g., a standard edge list) that can be processed efficiently.
3. **Graph Analytics (C++):** Write a C++ program at `/home/user/analyze_graph.cpp` that reads your extracted edge list. The program must compute the PageRank centrality for every node in the graph. 
   - Use a damping factor (`d`) of 0.85.
   - Initialize all nodes with a PageRank of `1.0 / N` (where N is the total number of nodes).
   - Run exactly 20 iterations of the PageRank algorithm.
   - Handle dangling nodes (nodes with no outbound edges) by distributing their score evenly among all nodes in the graph.
4. **Integration:** Compile your C++ program to `/home/user/analyze_graph` using standard `g++`. Run it to produce a final output file at `/home/user/pagerank.csv`.
   - The CSV must have the header `NodeID,PageRank`.
   - Sort the output by `NodeID` in ascending order.
   - Print the PageRank values to 6 decimal places.

Ensure your pipeline is fully automated and that the final `/home/user/pagerank.csv` perfectly matches the required format. The accuracy of your graph analytics will be evaluated strictly.