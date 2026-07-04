You are a Database Reliability Engineer managing a complex database backup infrastructure. Your backup strategy involves databases shipping backups to intermediate storage tiers, which then replicate to vault storage nodes.

You have a file at `/home/user/backup_topology.txt` representing this directed graph. Each line contains two node names separated by a space: `SourceNode DestinationNode`, indicating that data flows from the SourceNode to the DestinationNode.

Your task is to analyze this backup topology using purely Bash and standard Linux command-line utilities.

Perform the following operations:

1. **Calculate In-Degree Centrality**:
   Identify the node that receives data from the highest number of direct upstream neighbors (the highest in-degree). 
   Write ONLY the name of this node to `/home/user/highest_indegree.txt`.

2. **Bidirectional Replication (Clustering)**:
   Find all pairs of nodes that replicate to each other (i.e., there is an edge from A to B AND an edge from B to A).
   Write these pairs to `/home/user/bidirectional.txt`. Each line must contain the two node names separated by a space, with the alphabetically smaller node name first. Sort the final file alphabetically by the first column.

3. **Dependency Graph Pattern Matching (Parameterized Reachability)**:
   Write a Bash script at `/home/user/find_affected.sh` that takes exactly one argument (a target node name). The script must compute and print all unique nodes in the graph that eventually route their data to this target node (i.e., all nodes that have a directed path to the target node, regardless of depth). 
   - The output should exclude the target node itself.
   - The output must be a single column of node names, sorted alphabetically.
   - Using your script, determine all nodes that route to `vault-dr`. Run your script and redirect its output to `/home/user/affected_dbs.txt` (e.g., `./find_affected.sh vault-dr > /home/user/affected_dbs.txt`).

**Important Constraints**:
- You must use Bash and standard utilities (awk, grep, sed, etc.) to accomplish this. Do not write Python, Perl, or Ruby scripts.
- Make sure your script `/home/user/find_affected.sh` handles cyclic paths in the graph gracefully without infinite looping.