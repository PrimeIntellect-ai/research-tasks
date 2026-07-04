You are acting as a bioinformatics systems analyst. We need to build a reproducible computation pipeline that parses a FASTA file of DNA sequences, constructs a sequence similarity graph using parallel computation, and analyzes the graph components.

Your task is to implement this pipeline in C++ and Bash.

Here are the requirements:

1. **C++ Implementation (`/home/user/sequence_graph.cpp`)**
   Write a C++ program that:
   - Parses the FASTA file located at `/home/user/input.fasta`. You must implement your own simple FASTA parser. Each sequence in the file becomes a node in a graph.
   - Computes an adjacency matrix or list using **OpenMP** to parallelize the pairwise comparisons.
   - Edge criteria: An undirected edge exists between Node A and Node B (where A != B) if their corresponding sequences share at least one exact overlapping 3-mer (a contiguous substring of length 3). Comparisons should be case-sensitive.
   - Uses a graph algorithm (e.g., BFS or DFS) to find all disconnected connected components in the graph.
   - Writes the results to `/home/user/graph_stats.txt` in exactly this format:
     ```
     Components: <N>
     Largest_Component_Size: <M>
     ```
     (Where `<N>` is the number of connected components, and `<M>` is the number of nodes in the largest component).

2. **Reproducible Pipeline & Regression Test (`/home/user/run_pipeline.sh`)**
   Write a Bash script that:
   - Compiles the C++ code with OpenMP support (e.g., using `g++` with `-fopenmp` and `-O3`).
   - Runs the compiled executable.
   - Compares the generated `/home/user/graph_stats.txt` against a regression test expected output file located at `/home/user/expected_stats.txt`.
   - If the file contents match exactly, the script should print "PASS" and exit with code 0.
   - If they do not match, or if compilation/execution fails, the script should print "FAIL" and exit with code 1.
   - Make sure the script is executable (`chmod +x`).

The input files (`/home/user/input.fasta` and `/home/user/expected_stats.txt`) already exist on the system. You just need to create the C++ program and the pipeline script, and ensure running `/home/user/run_pipeline.sh` succeeds.