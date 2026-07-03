You are a data engineer working on an ETL pipeline that processes data lineage graphs. The data extraction step occasionally pulls corrupted, stale records from a malfunctioning SQLite index, resulting in a dirty edge-list file.

Your task is to write a C program that parses this dirty data, filters out the corrupted records based on a strict schema, and computes the shortest path between two specific nodes.

**Input Data:**
There is a file at `/home/user/graph_data.csv` containing directed edges.
Each line is supposed to be in the format: `SourceNode,TargetNode,Weight`

**Corruption & Schema Rules (Pattern Matching & Validation):**
You must ignore any line that does not strictly match the following valid schema:
1.  `SourceNode` and `TargetNode` must start exactly with the uppercase letter 'N' followed immediately by one or more digits (e.g., `N0`, `N42`).
2.  `Weight` must be a strictly positive integer (greater than 0).
3.  The line must have exactly three comma-separated fields with no extra whitespace around the commas.
4.  Ignore lines with negative weights, zero weights, missing fields, or improperly formatted node names.

**Objective:**
Write a C program at `/home/user/compute_path.c`. 
When compiled and executed (e.g., `gcc -o compute_path compute_path.c && ./compute_path`), it must:
1. Read `/home/user/graph_data.csv`.
2. Filter the edges according to the schema rules.
3. Construct a directed graph from the valid edges.
4. Compute the shortest path from `N0` to `N10`.
5. Write the result to `/home/user/path_output.txt`.

**Output Format:**
The file `/home/user/path_output.txt` must contain exactly two lines:
Line 1: `Path: N0->...->N10` (listing the nodes in the shortest path)
Line 2: `Weight: <TotalWeight>`

If no path exists, the file should contain a single line: `No valid path found`