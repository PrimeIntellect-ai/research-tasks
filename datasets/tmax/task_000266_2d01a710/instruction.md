You are a data engineer building an ETL pipeline that processes network interaction data. We need to implement a fast graph processing step in C.

You are provided with a raw edge list in `/home/user/raw_edges.txt`. This file represents directed interactions between nodes, with each line containing two integers separated by a space: `SourceID TargetID`. 

Your task is to write and execute a C program (`/home/user/process_graph.c`) that performs the following steps:
1. **Graph Projection & Centrality**: Treat the graph as an undirected multigraph (an interaction from A to B means both A and B are involved). Calculate the "interaction degree" (degree centrality) for every unique node. This is simply the total number of times a node appears in the file (either as a source or target).
2. **Filtering**: Discard all nodes that have an interaction degree of less than 3.
3. **Sorting**: Sort the remaining nodes by their interaction degree in descending order. If there is a tie, sort by the Node ID in ascending order.
4. **Pagination**: We need to extract a specific "page" of the sorted results. Assuming a page size of 5 records (Page 1 is records 1-5, Page 2 is records 6-10, etc.), extract the records for **Page 2**.

Your C program must output the results for Page 2 to `/home/user/page2_results.txt`. 
Each line in the output file should be formatted exactly as: `<NodeID> <Degree>`. 

For example, if the 6th record in the sorted filtered list is Node 99 with a degree of 4, the first line of the output file should be `99 4`.

Ensure your C program compiles cleanly with `gcc /home/user/process_graph.c -o /home/user/process_graph` and run it to produce the required output file.