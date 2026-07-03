I need you to write and execute a C program that performs a statistical Monte Carlo simulation on a protein interaction network derived from a FASTA file. 

Here is the scenario:
I have a dataset of protein sequences in a FASTA file located at `/home/user/proteins.fasta`. 
We want to model a network where each sequence is a node. An undirected edge exists between any two nodes if their protein sequences share an exact identical prefix of length 3 or more (e.g., "MKVLL" and "MKVXY" share "MKV", so they are connected).

Once the graph is built, we want to simulate random protein knockouts (deletions) and observe the robustness of the network by measuring the size of the Largest Connected Component (LCC).

Your task is to write a C program at `/home/user/simulate.c` that does the following:
1. **Parse the FASTA file:** Read `/home/user/proteins.fasta`. Each entry has a header starting with `>` and a subsequent sequence string (single line, upper case). Keep track of the nodes in the order they appear in the file (0-indexed).
2. **Build the Graph:** Construct an adjacency list or matrix based on the prefix rule (length >= 3).
3. **Monte Carlo Simulation:** Run exactly 10,000 iterations of a simulation.
    * In each iteration, start with the full graph.
    * Iterate through the nodes in their original parsing order (0 to N-1). For each node, determine if it is "knocked out" (deleted) with probability $p = 0.25$.
    * To ensure perfect reproducibility across different C libraries, **do NOT use `rand()`**. Implement the following specific Linear Congruential Generator (LCG):
      ```c
      unsigned long int seed = 12345;
      double get_rand() {
          seed = (seed * 1103515245 + 12345) % 2147483648;
          return (double)seed / 2147483648.0;
      }
      ```
    * A node is knocked out if `get_rand() < 0.25`.
    * After determining the active (non-deleted) nodes, find the size of the Largest Connected Component (LCC) among the active nodes. An LCC is the maximum number of connected active nodes. If all nodes are knocked out, the LCC size is 0. If a node is active but has no active neighbors, it forms a component of size 1.
4. **Statistical Output:** Calculate the mean LCC size across all 10,000 iterations. 

Write the final mean LCC size to a file named `/home/user/simulation_results.txt` in exactly this format:
`Mean LCC: [value rounded to 4 decimal places]` (e.g., `Mean LCC: 4.1234`).

Compile your code using standard `gcc` (e.g., `gcc -O3 /home/user/simulate.c -o /home/user/simulate`) and run it to produce the output file.