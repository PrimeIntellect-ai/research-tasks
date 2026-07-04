I am a researcher studying the structural robustness of molecular networks. I am analyzing how a "near-disconnected" component (similar to a near-singular input in matrix factorization) affects the diffusion of a signal across the network. 

I have two network topologies represented as undirected weighted graphs in edge-list format:
- `/home/user/graph_A.txt` (Wild-type)
- `/home/user/graph_B.txt` (Mutated, containing a near-disconnected bridge)

Each file has the format: `node_1 node_2 weight`. The nodes are numbered continuously from `0` to `N-1`. The graph is undirected, meaning an edge from `u` to `v` also implies an edge from `v` to `u` with the same weight.

I need you to write a C program that simulates a random walk (diffusion) on both graphs and compares their final state distributions. 

Here are the specific requirements for your C program:
1. **Graph Parsing & Matrix Setup**: Read the edge lists to determine the number of nodes `N` (it is the same for both graphs). Construct the row-stochastic transition matrix `M` for each graph. For a node `i`, the transition probability to neighbor `j` is `weight(i, j) / sum(weights of all edges incident to i)`.
2. **Parallel Diffusion**: Start with an initial probability distribution `P_0` where node 0 has probability 1.0, and all other nodes have 0.0. Simulate `T = 100` steps of the random walk: `P_{t+1} = P_t * M`. You **must** use OpenMP (`#pragma omp parallel for`) to parallelize the matrix-vector multiplication at each step.
3. **Smoothing**: Some nodes might have zero probability, which breaks logarithmic comparisons. After 100 steps, add a small epsilon `e = 1e-9` to the probability of every node, and then strictly re-normalize the distribution so that the sum of all probabilities exactly equals 1.0. Do this for both graph A's final distribution (`P_A`) and graph B's final distribution (`P_B`).
4. **Distribution Distance**: Compute the Kullback-Leibler (KL) divergence from `P_B` to `P_A`, defined as: `KL(P_A || P_B) = sum_i [ P_A[i] * log( P_A[i] / P_B[i] ) ]`, where `log` is the natural logarithm.
5. **Output**: Your C program must write the single computed KL divergence value to `/home/user/kl_result.txt` formatted to exactly 6 decimal places (e.g., `0.123456`).

Please write the code to `/home/user/simulate.c`, compile it using `gcc -fopenmp -O2 simulate.c -o simulate -lm`, and run it to produce the output file.