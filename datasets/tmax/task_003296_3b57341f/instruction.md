You are acting as a Database Reliability Engineer. We have just exported a backup from our production graph database, and we need to verify its structural integrity before we archive it. Bringing up a full graph database instance just to check the backup takes too long, so I need you to build a quick standalone C program to analyze the backup files.

The backup consists of two CSV files located in `/home/user/`:
1. `/home/user/backup_nodes.csv` (Format: `id,label`)
2. `/home/user/backup_edges.csv` (Format: `source,target,type`)

Task Requirements:
1. Write a C program named `/home/user/analyze_backup.c`.
2. The program must read the two CSV files and calculate the total degree centrality (in-degree + out-degree) for every node.
3. It must find the node with the highest total degree. If there is a tie, select the node with the lowest numeric ID.
4. The program should output this single most critical node to a file named `/home/user/critical_node.txt` in the exact format: `NodeID,TotalDegree`.
5. Compile the C program to `/home/user/analyze_backup` and run it to produce the output file.
6. Finally, to document how we would perform this same check in the actual graph database, write the equivalent Cypher query and save it in `/home/user/validation_query.cypher`. The query should return the `id` and `total_degree` of the highest degree node (resolving ties by lowest `id` ascending) assuming nodes have an `id` property and relationships are undirected for the purpose of the degree sum.

Please write the C code, compile it, run it, and provide the Cypher query.