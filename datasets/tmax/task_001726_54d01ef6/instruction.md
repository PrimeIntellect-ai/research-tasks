I am a researcher studying the biased diffusion of a particle on a small circular polymer (modeled as a directed cycle graph of 5 nodes, labeled 0 to 4). 

I need you to write a C program that simulates this diffusion, tests its convergence to the analytical stationary distribution, and compares the final results against a reference experimental dataset.

Here are the specific rules of the simulation:
1. The particle starts at node 0.
2. At each step, the particle either moves to the next node `(current + 1) % 5` with probability `p = 0.7`, or stays at the current node with probability `1 - p = 0.3`.
3. The analytical stationary distribution of this symmetric ring is uniform: `0.2` for each node.

To ensure strict cross-platform reproducibility, you **must** use the following custom pseudorandom number generator instead of C's `rand()`:
```c
unsigned int state;
void init_rand(unsigned int seed) {
    state = seed;
}
unsigned int my_rand() {
    state = (state * 1103515245 + 12345) % 2147483648;
    return state;
}
double my_drand() {
    return (double)my_rand() / 2147483648.0;
}
```
At each step, generate a random double `r = my_drand()`. If `r < 0.7`, the particle moves; otherwise, it stays.

**Your Tasks:**
1. Write a C program (save it as `/home/user/simulate.c`) that simulates this process.
2. Perform a **convergence test** by running the simulation for different total steps $N \in \{1000, 10000, 100000, 1000000\}$. 
   - **Crucial:** For *each* value of $N$, you must re-initialize the PRNG with `init_rand(42)` and start a fresh simulation from node 0.
   - For each $N$, calculate the empirical frequency of visits to each node (total visits to node $i$ / $N$).
   - Calculate the L2 norm of the error between the empirical distribution and the analytical stationary distribution (0.2). The L2 error is $\sqrt{\sum_{i=0}^4 (f_i - 0.2)^2}$.
3. Create a log file at `/home/user/convergence_log.csv` with exactly this header: `N,L2_error`. Add the results for your 4 runs, formatted to 6 decimal places for the error.
4. I have an experimental reference dataset at `/home/user/reference.csv` containing the expected frequencies for a $10^6$-step run. Calculate the absolute difference between your empirical frequencies for $N=1000000$ and the reference frequencies for each node. Find the maximum absolute difference among the 5 nodes, and write this single float value (formatted to 6 decimal places) to `/home/user/max_diff.txt`.

Please write the C code, compile it (e.g., using `gcc`), run it, and generate the required output files.