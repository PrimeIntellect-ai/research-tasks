You are a Machine Learning Engineer preparing training data for a Graph Neural Network (GNN) that predicts molecular stability. You need to parse a molecular structure, convert it into a spatial graph representation, and compute statistically rigorous baseline features.

Your task is to write a C program that reads a Protein Data Bank (PDB) file, constructs a graph based on atomic distances, and calculates the 95% Bootstrap Confidence Interval of the mean bond length.

Write your C code in `/home/user/process_pdb.c`. 
Compile it to an executable named `/home/user/process_pdb` using `gcc -O2 -lm`, and then run it to generate the final output at `/home/user/graph_stats.txt`.

Requirements for your C program:
1. **Bioinformatics Parsing**: Read `/home/user/data.pdb`. Parse only the lines that start with the exact string `"ATOM  "`. Extract the X, Y, and Z coordinates (columns 31-38, 39-46, and 47-54 respectively, though standard `sscanf` or tokenization may suffice depending on the file spacing). Store these coordinates in a multi-dimensional array.
2. **Graph Construction**: Construct an undirected graph where each atom is a node. An edge (bond) exists between two distinct atoms if the Euclidean distance between them is strictly greater than 0.0 and less than or equal to `1.8` Angstroms. 
3. **Data Extraction**: Extract the lengths of all unique edges in the graph. Do not duplicate edges (e.g., if A connects to B, do not also count B connecting to A).
4. **Bootstrap Confidence Interval**:
   Calculate the mean of all extracted edge lengths.
   Generate 10,000 bootstrap samples of the mean edge length to estimate the 95% Confidence Interval.
   - For *each* of the 10,000 iterations, draw `E` samples with replacement from your pool of edges (where `E` is the total number of unique edges).
   - Calculate the mean of these `E` samples.
   - After computing all 10,000 means, sort them in ascending order.
   - The lower bound of the 95% CI is the value at index `250` (using 0-based indexing).
   - The upper bound of the 95% CI is the value at index `9749` (using 0-based indexing).
   - **Crucial**: To ensure reproducibility across environments, you *must* use the following deterministic random number generator to select edge indices, rather than `rand()`:

```c
unsigned int rng_state = 12345;
unsigned int next_rand() {
    rng_state = (rng_state * 1103515245 + 12345) & 0x7FFFFFFF;
    return rng_state;
}
```
   To select a random edge index in your bootstrap loop, use `next_rand() % E`.

Output Requirements:
Your program should write the results to `/home/user/graph_stats.txt` in exactly the following format (rounding floats to 4 decimal places):
```
Atoms: <number_of_atoms>
Edges: <number_of_edges>
Mean: <mean_edge_length>
CI_Lower: <lower_bound>
CI_Upper: <upper_bound>
```