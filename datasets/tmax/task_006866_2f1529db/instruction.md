You are a data engineer building an ETL pipeline to analyze network communication logs. 

You have been provided with a raw log file located at `/home/user/network_traffic.csv`. 
The file contains network traffic records with the following columns:
`timestamp,src_ip,dst_ip,bytes`

Your task is to process this raw data to extract graph-based metrics and materialize the results. Please perform the following steps:

1. **Graph Projection and Aggregation**: Convert the raw logs into an undirected, weighted graph. 
   - Nodes are individual IP addresses.
   - Edges represent communication between two IPs.
   - The graph must be undirected. If `IP_A` sends data to `IP_B` and `IP_B` sends data to `IP_A`, these should be treated as a single edge between `IP_A` and `IP_B`.
   - The weight of an edge should be the sum of all `bytes` transferred between the two IPs across all timestamps, regardless of direction.

2. **Graph Analytics**:
   - **Centrality**: Determine the top 3 nodes (IP addresses) by Weighted Degree Centrality. In this context, this means the total sum of bytes associated with all incident edges for each IP.
   - **Clustering**: Determine the number of isolated network clusters (connected components) in the graph, and specifically find the size (number of unique nodes) of the largest connected component.

3. **Materialization**: 
   - Output your final aggregated metrics to a JSON file located precisely at `/home/user/etl_summary.json`.
   - The JSON file must strictly follow this exact format:
     ```json
     {
       "top_3_ips_by_traffic": ["ip1", "ip2", "ip3"],
       "largest_component_size": <integer>
     }
     ```
   - *Note*: Ensure the list of top 3 IPs is ordered from highest traffic to lowest. If there is a tie, order alphabetically.

You may use any programming language or scripting tools of your choice to complete this task.