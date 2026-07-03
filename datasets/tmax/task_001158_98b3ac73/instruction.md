You are acting as a research assistant in computational chemistry. We are modeling the diffusion of a particle on a molecular mesh network. The mesh is represented as an undirected graph.

Your task is to build a reproducible computation pipeline in C that simulates a random walk on this network, computes the empirical stationary distribution of the particle, and compares it to the theoretical distribution using the Kullback-Leibler (KL) divergence.

Please follow these specific instructions:

1. Create a directory `/home/user/mesh_simulation` and do all your work inside it.

2. Create a file named `graph.txt` representing our molecular mesh with the following space-separated edges (one per line):
```
0 1
0 2
1 2
1 3
2 3
```

3. Write a C program named `simulate.c` that does the following:
   - Reads the `graph.txt` file and builds an adjacency list. For consistency, the neighbors for any given node must be sorted in ascending numerical order (e.g., node 1's neighbors are 0, 2, 3 in that order).
   - Simulates a random walk of `10000` steps starting at node `0`.
   - To ensure reproducibility across different environments, you MUST implement and use the following Linear Congruential Generator (LCG) instead of `rand()`:
     ```c
     unsigned int lcg_seed = 42; // Initial seed
     unsigned int lcg_rand() {
         lcg_seed = (lcg_seed * 1103515245 + 12345) & 0x7fffffff;
         return lcg_seed;
     }
     ```
   - At each step, if the current node has $d$ neighbors, the next node is chosen by taking `lcg_rand() % d` and indexing into the sorted neighbor array.
   - Count the number of times each node is visited (do not count the initial placement at node 0 at step 0; only count the destinations of the 10000 steps). Calculate the empirical probability distribution $P$ of the visits.
   - Calculate the theoretical stationary distribution $Q$. For a random walk on a connected undirected graph, the theoretical probability of being at node $i$ is proportional to its degree: $Q(i) = \text{degree}(i) / (2 \times \text{total\_edges})$.
   - Compute the Kullback-Leibler divergence from $Q$ to $P$: $D_{KL}(P \parallel Q) = \sum_{i} P(i) \ln\left(\frac{P(i)}{Q(i)}\right)$. Use natural logarithm (`log` in `math.h`).

4. Create a `Makefile` with a `default` target that compiles `simulate.c` (producing an executable named `simulate`, linking the math library `-lm`) and a `run` target that executes it and redirects the standard output to `results.txt`.

5. The output printed to `results.txt` must be exactly in this format:
   ```
   P(0)=0.xxxxxx
   P(1)=0.xxxxxx
   P(2)=0.xxxxxx
   P(3)=0.xxxxxx
   KL=0.xxxxxx
   ```
   (Print exactly 6 decimal places for all floating point numbers).

6. Build and run the pipeline so that `results.txt` is populated.