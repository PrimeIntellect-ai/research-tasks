You are assisting a compliance officer in auditing system architecture to ensure Personally Identifiable Information (PII) is protected. 

The architecture is represented as a directed graph of data flows between system components. You are provided with two files in `/home/user/`:
1. `components.csv`: Contains component definitions. Format: `comp_id,comp_type`
   - Types can be: `Public`, `Internal`, `Encryption`, `PII`.
2. `data_flows.csv`: Contains the directed data flows. Format: `source_id,dest_id`

A "vulnerable" PII component is defined as any component of type `PII` that can be reached via a directed path from any component of type `Public`, such that the path **does not** pass through any component of type `Encryption`. (If the path reaches an `Encryption` component, that specific path is considered secure and cannot continue to compromise downstream components).

Your task is to:
1. Write a C program at `/home/user/audit.c` that parses these CSV files and models the architecture as a graph.
2. Implement a recursive or queue-based traversal to identify all vulnerable PII components.
3. The program must write the integer `comp_id`s of all vulnerable PII components to `/home/user/vulnerable_pii.txt`.
4. The output file must contain one `comp_id` per line, sorted in ascending numerical order.
5. Compile your C program to an executable named `/home/user/audit` and run it to produce the output file.

Assume maximum `comp_id` is less than 1000. Do not use external libraries other than the C standard library.