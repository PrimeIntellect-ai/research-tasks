You are acting as a data analyst who needs to process a raw network log into a graph database import script. 

I have a CSV file located at `/home/user/network_edges.csv` with the following format:
```csv
source_node,target_node,data_transferred
NodeA,NodeB,50
NodeB,NodeC,20
NodeA,NodeB,30
NodeC,NodeA,100
NodeC,NodeA,50
NodeA,NodeC,10
```

Notice that there are multiple entries for the same directed edge. I need you to write a C program at `/home/user/graph_converter.c` that performs an aggregation (summing up the `data_transferred` for each unique `source_node` -> `target_node` pair) and converts this aggregated data into a Cypher script.

The compiled program should be executable as `/home/user/converter` and take two arguments: the input CSV file and the output Cypher file.
Example: `/home/user/converter /home/user/network_edges.csv /home/user/import.cypher`

The generated Cypher script (`/home/user/import.cypher`) must contain exactly one line per aggregated edge in the following format (sorted alphabetically by `source_node`, then by `target_node`):
`MERGE (a:Node {id: 'SOURCE'}) MERGE (b:Node {id: 'TARGET'}) MERGE (a)-[r:TRANSFERRED {total_data: WEIGHT}]->(b);`

For example, for NodeA to NodeB with a total of 80:
`MERGE (a:Node {id: 'NodeA'}) MERGE (b:Node {id: 'NodeB'}) MERGE (a)-[r:TRANSFERRED {total_data: 80}]->(b);`

Please write the C code, compile it, and run it to generate the `/home/user/import.cypher` file. Ensure the C code handles the CSV parsing, aggregation, sorting, and Cypher string formatting natively. Ignore the CSV header line during processing.