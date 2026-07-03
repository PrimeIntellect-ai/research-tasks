You are a performance engineer profiling a numerical application. We need to build a deterministic Monte Carlo simulator to estimate the volume of a 3D unit sphere, store the coordinates in a multi-dimensional array, measure its accuracy across different sample sizes, and visualize the error convergence using standard bash tools.

Your task is to implement the C program and a bash script to automate the experiment.

**Phase 1: The Monte Carlo Simulator (C)**
Create a C program at `/home/user/mc_sphere.c`.
1. The program must accept a single command-line argument: the number of samples `N`.
2. To ensure determinism across different systems, do NOT use `rand()`. Implement this exact Linear Congruential Generator (LCG):
   - State variable: `unsigned long long seed = 42;`
   - Update rule: `seed = (1103515245 * seed + 12345) % 2147483648;`
   - Do this for every coordinate.
3. Allocate a multi-dimensional array (or a flat array treated as $N \times 3$) to hold the 3D coordinates.
4. For each sample $i$ from 0 to $N-1$:
   - Generate `x`, then `y`, then `z` sequentially.
   - For each coordinate, update the seed, then convert to a `double` in the range `[-1.0, 1.0)` using the formula: `(double)seed / 2147483648.0 * 2.0 - 1.0`.
   - Store the coordinates in the array.
5. Iterate through the array to count how many points fall strictly inside the unit sphere ($x^2 + y^2 + z^2 < 1.0$).
6. Calculate the estimated volume: $V = 8.0 \times \frac{\text{inside}}{N}$.
7. Calculate the absolute error: $E = |V - 4.188790204786|$.
8. Print the result to standard output in exactly this format: `[N] [Error]` formatted as `%d %.6f\n`.

**Phase 2: Experiment & Visualization (Bash)**
Create a bash script at `/home/user/run_experiment.sh`.
1. The script must compile `mc_sphere.c` into an executable named `mc_sphere` with `-O3` optimization.
2. It should run the executable for $N$ values starting from 10,000 to 100,000 in increments of 10,000.
3. Save the raw output of all runs into `/home/user/mc_errors.txt` (one run per line).
4. Using `awk`, read `/home/user/mc_errors.txt` and generate an ASCII plot saved to `/home/user/error_plot.txt`.
5. The plot format for each line must be: `N` formatted to exactly 6 characters wide (right-aligned), followed by ` | `, followed by a sequence of `*` characters. The number of `*` characters should be exactly equal to `floor(Error * 500)`.

**Constraints:**
- Use standard C libraries only (`stdio.h`, `stdlib.h`, `math.h`).
- Use only standard bash tools and coreutils.
- Ensure appropriate permissions for the bash script.