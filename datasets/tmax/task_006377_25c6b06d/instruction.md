You are a data analyst tasked with processing a raw network traffic log file to find the most critical nodes based on connection volume.

You have a CSV file located at `/home/user/network_traffic.csv` with the following columns: `timestamp,src_ip,dst_ip,bytes,protocol`.
This log implicitly represents a directed weighted graph where IP addresses are nodes, edges represent traffic from `src_ip` to `dst_ip`, and the edge weight is the total `bytes` transferred.

Your task is to:
1. Write a C program named `/home/user/graph_analyzer.c` that parses this CSV.
2. The program must reverse-engineer this log into a node-level representation (graph materialization). For every unique IP address (whether it appears as a source or destination), calculate its "total node strength". Total node strength is defined as the sum of all `bytes` sent (out-weight) plus all `bytes` received (in-weight) by that IP address.
3. The C program must accept exactly three command-line arguments in this order: `<input_csv_path> <min_strength_filter> <top_k_limit>` (parameterized query construction).
    - `input_csv_path`: The path to the input CSV file.
    - `min_strength_filter`: An integer. Nodes with a total strength strictly less than this value should be filtered out.
    - `top_k_limit`: An integer. The maximum number of nodes to output (pagination/limiting).
4. The C program must output the results to a file named `/home/user/top_nodes.csv`.
    - The output file must be a headerless CSV with the format: `ip_address,total_strength`.
    - The output must be sorted in descending order of `total_strength`.
    - If two nodes have the exact same `total_strength`, sort them alphabetically by `ip_address`.
    - Limit the output to at most `top_k_limit` rows.
5. Compile your C program using `gcc` into an executable named `/home/user/graph_analyzer`.
6. Finally, execute your program against `/home/user/network_traffic.csv` with a minimum strength filter of `1000` and a limit of `2`:
   `./graph_analyzer /home/user/network_traffic.csv 1000 2`

Ensure your C code handles the CSV parsing correctly (ignoring the header row if present, correctly summing the integer byte values, and properly managing memory).