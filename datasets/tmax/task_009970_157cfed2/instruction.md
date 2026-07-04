You are a data analyst working with a simple network routing dataset in CSV format. 

There is a dataset located at `/home/user/network.csv` with the header `source,target,weight`. This represents an **undirected** graph (an edge from A to B implies an edge from B to A with the same weight).

Your task is to write a Bash script at `/home/user/analyze_graph.sh` that does the following:
1. Identifies the node with the highest degree centrality (the node connected to the most unique other nodes). If there is a tie, choose the node that comes first alphabetically. Let's call this node `C_NODE`.
2. Computes the shortest path (lowest total weight) from `C_NODE` to `Node_Z`. 
3. Outputs the findings to a file named `/home/user/result.txt` in the exact following format:

```text
Central Node: <C_NODE>
Shortest Path: <C_NODE>-><intermediate_node1>->...->Node_Z
Total Weight: <total_weight>
```

Requirements:
- Your script must be self-contained and primarily executed via Bash, though you may embed Python (`python3`), `awk`, or other standard Linux utilities within your script to accomplish the graph analytics.
- Remember to treat all edges as undirected.
- Ensure the script has executable permissions and can be run directly as `/home/user/analyze_graph.sh`. Run the script to generate `/home/user/result.txt`.