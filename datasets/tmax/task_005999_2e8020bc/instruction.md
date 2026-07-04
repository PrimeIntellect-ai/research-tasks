You are a performance engineer optimizing a bioinformatics pipeline. The current Python pipeline calculates a network-based "consensus score" for a set of DNA sequences, but the pairwise sequence comparison is too slow. You have been provided with a fast C implementation of the sequence comparison function.

Your task is to integrate this C code, compute the sequence graph, and solve a linear system to find the consensus scores.

Here are your specific instructions:

1. **Compile the C library**:
   You will find a C source file at `/home/user/src/seq_compare.c`. It contains a function `int sequence_distance(const char* s1, const char* s2, int len)` that calculates the Hamming distance between two DNA sequences of the same length.
   Compile this C file into a shared library named `/home/user/libseq.so`.

2. **Compute the Graph Adjacency Matrix**:
   Read the DNA sequences from `/home/user/data/sequences.txt`. Each line contains one sequence. All sequences have the same length $L$.
   Using Python's `ctypes` module, load `/home/user/libseq.so` and use it to compute the $N \times N$ distance matrix $D$, where $D_{ij}$ is the distance between the $i$-th and $j$-th sequences (0-indexed). 
   Let the adjacency matrix $A$ be defined as $A_{ij} = L - D_{ij}$ (this represents the number of matching bases).

3. **Solve the Network Equation**:
   To find the consensus score vector $x$, solve the following linear system:
   $(I + 0.05 A) x = b$
   where $I$ is the $N \times N$ identity matrix, $A$ is the adjacency matrix computed above, and $b$ is a column vector of ones ($[1, 1, \dots, 1]^T$). Use `scipy.linalg.solve` or `numpy.linalg.solve`.

4. **Output the Results**:
   Write a Python script `/home/user/run_pipeline.py` that performs steps 2 and 3.
   The script must create a JSON file at `/home/user/report.json` with the following exact structure:
   ```json
   {
       "adjacency_matrix": [
           [4, 3, 2, ...],
           ...
       ],
       "consensus_scores": [0.8523, 0.9124, ...]
   }
   ```
   *Note: `adjacency_matrix` must be a list of lists of integers. `consensus_scores` must be a list of floats, rounded to 4 decimal places.*