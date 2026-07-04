You are acting as an automated assistant for a compliance officer who is auditing system access logs. We need to detect potential data exfiltration paths by querying an access graph. 

The system access logs are provided as a CSV file at `/home/user/system_logs.csv`. The file has the following format:
`timestamp,src_node,dst_node,action`

We need to treat this log as an edge list representing a temporal graph. You must write a C program at `/home/user/graph_audit.c` that performs a specific graph query, similar to chaining in a graph or NoSQL pipeline.

Your C program must:
1. Parse the `/home/user/system_logs.csv` file.
2. Find all directed path sequences of length 2 matching this exact pattern:
   - Edge 1: A User (`src_node` starts with `U_`) accesses a Database (`dst_node` starts with `DB_`) with the action `READ`.
   - Edge 2: The *same* User (`src_node` starts with `U_`) accesses an External Endpoint (`dst_node` starts with `EXT_`) with the action `TRANSFER`.
   - The timestamp of Edge 2 must be strictly greater than the timestamp of Edge 1.
3. Combine these matches into result records of the format: `User,Database,ExternalEndpoint,Time1,Time2`.
4. Sort the result records in ascending order based on `Time1` (the timestamp of Edge 1). If `Time1` is identical, sort by `Time2` ascending.
5. Implement pagination. The program must accept command line arguments for limit and offset.

Usage: `./graph_audit <csv_file> <limit> <offset>`
Example: `./graph_audit /home/user/system_logs.csv 5 10`

Output the results directly to standard output (stdout), one record per line, in this exact format:
`U_123,DB_FIN,EXT_IP1,1620001000,1620001050`

Ensure your program compiles without warnings using `gcc -O2 -Wall -o /home/user/graph_audit /home/user/graph_audit.c`.
Once written and compiled, run the tool to fetch exactly 3 results, skipping the first 2 sorted results. Save the output of this specific query to `/home/user/audit_report.txt`.

**Note:** The timestamp is an integer. The node names and actions are strings up to 32 characters long. The number of logs will not exceed 1000.