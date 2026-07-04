You are a data analyst tasked with processing some raw logistics network data using only Bash shell tools (like `awk`, `join`, `sort`, `grep`, etc.). 

In the `/home/user/data` directory, there are two raw text files: `fileA.txt` and `fileB.txt`. They contain CSV-formatted data (with headers) representing a graph of warehouses and the shipping routes between them. However, the exact data model is unknown, and you must reverse engineer it by examining the files. One file contains warehouse node information (including IDs and Names), and the other contains directed edge information (source ID, destination ID, and shipping cost).

Your tasks are:
1. **Index Creation**: Create an optimized index file at `/home/user/warehouse_index.csv`. This file must contain exactly two columns: `name,id` (extracted from the nodes file), and it must be sorted alphabetically by the warehouse `name`. Do not include a header row in this file. This index strategy is designed to allow fast prefix lookups using tools like `look`.
2. **Graph Traversal Pipeline**: Using pipeline chaining, find all shipping paths of *exactly two hops* (i.e., Source -> Intermediate -> Destination) starting from the warehouse named "Alpha". 
3. **Data Aggregation**: For each 2-hop path found, calculate the total shipping cost (the sum of the costs of the two individual hops).
4. **Formatting Output**: Save your final 2-hop traversal results in `/home/user/two_hop_Alpha.csv`. The file must contain a header `Destination_Name,Total_Cost`. Each subsequent line should list the name of the destination warehouse and the total shipping cost for that specific 2-hop path.
5. **Sorting**: The results in `/home/user/two_hop_Alpha.csv` (excluding the header) must be sorted primarily by `Total_Cost` in descending order (numerically), and secondarily by `Destination_Name` in ascending order (alphabetically).

Ensure your pipeline correctly resolves the warehouse names by cross-referencing the node data. Only standard Linux CLI tools (Bash built-ins, coreutils, `awk`, etc.) are permitted. Do not use Python, Perl, or other external scripting languages.