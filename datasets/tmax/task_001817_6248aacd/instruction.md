You are a performance engineer tasked with implementing and profiling a new 2D thermal dissipation model for a chip architecture. 

Your objective is to write a C program that simulates heat diffusion using a 2D partial differential equation (PDE), extract the resulting temperature density distribution, and evaluate it against a reference profile.

Step 1: Write the Simulation in C
Create a file at `/home/user/heat_sim.c`. The program must simulate a 2D grid of temperatures over a series of time steps.
- Grid size: 50x50. Array elements are `double`.
- Initial State: All cells start at `0.0`, except for a central "hotspot" where `20 <= i <= 29` and `20 <= j <= 29`, which starts at `100.0` (inclusive bounds, 0-indexed).
- Boundary Conditions: The edges of the grid (`i=0`, `i=49`, `j=0`, `j=49`) are permanently fixed at `0.0`.
- Update Rule for inner cells: `u_next[i][j] = u[i][j] + alpha * (u[i+1][j] + u[i-1][j] + u[i][j+1] + u[i][j-1] - 4 * u[i][j])`
- Constants: `alpha = 0.1`. 
- Time Steps: Run the simulation for exactly `100` iterations (updates).
- Density Output: After 100 iterations, calculate the density distribution of the final temperatures across all 2500 grid points. Use 10 bins: [0, 10), [10, 20), ..., [90, 100]. A value exactly equal to 100.0 should go in the final bin (Bin 9).
- The program must write this distribution to `/home/user/temp_dist.txt` with exactly 10 lines, formatted as: `Bin X: Y` where `X` is the bin index (0-9) and `Y` is the integer count of cells in that bin.

Step 2: Compilation
Compile your program using GCC with optimizations enabled: `gcc -O3 -o /home/user/heat_sim /home/user/heat_sim.c`.

Step 3: Reference Comparison
A reference distribution is located at `/home/user/reference_profile.txt`. 
Write a bash script at `/home/user/evaluate.sh` that:
1. Runs `/home/user/heat_sim`.
2. Reads `/home/user/temp_dist.txt` and `/home/user/reference_profile.txt`.
3. Computes the L1 error (the sum of the absolute differences in counts for each of the 10 bins).
4. Writes the total L1 error as a single integer to `/home/user/error_metric.txt`.

Ensure all files are created in the correct locations and `evaluate.sh` is executable. You can run `./evaluate.sh` to test your end-to-end process.