You are an AI assistant helping a Machine Learning engineer prepare synthetic training data for a model that predicts percolation. 

We need a Rust program to perform a Monte Carlo simulation of grid percolation, which will be compared against a reference dataset of theoretical probabilities. 

You must write and execute a Rust script that does the following:

1. **Read Reference Data**: Parse `/home/user/reference.csv`, which contains two columns: `p` (the probability of a cell being occupied) and `P_theo` (the theoretical percolation probability).
2. **Monte Carlo Simulation**:
   - For each row (in the order they appear in the CSV), simulate $N = 100$ independent 2D grids of size $10 \times 10$.
   - **Random Number Generation**: To ensure exact reproducibility for our automated tests, you MUST implement a Linear Congruential Generator (LCG) with the following parameters:
     - $X_0 = 42$ (Initial seed, start this ONCE at the beginning of the program, do not reset it between grids or between `p` values).
     - $a = 1664525$
     - $c = 1013904223$
     - $m = 2^{32}$ (Use standard 32-bit wrapping arithmetic).
     - To generate a float in $[0, 1)$, compute $r = X_{n} / 2^{32}$ (using `f64`). Update the state for the next call.
   - **Grid Generation**: For a given grid and probability `p`, iterate through the 100 cells in row-major order (row 0 col 0, row 0 col 1, ..., row 9 col 9). For each cell, generate a random float $r$ using the LCG. If $r < p$, the cell is occupied (1); otherwise, it is empty (0).
   - **Percolation Check**: A grid "percolates" if there is a path of occupied cells from *any* cell in the top row (row 0) to *any* cell in the bottom row (row 9). Paths can only move horizontally and vertically (4-connectivity) through occupied cells.
3. **Comparison**: For each `p`, calculate your Monte Carlo estimate $\hat{P}(p) = (\text{number of percolating grids}) / 100$.
4. **Output**: Write the results to `/home/user/results.csv` with the headers `p,P_theo,P_sim,abs_error`. `abs_error` should be $|\hat{P}(p) - P_{theo}|$. Format the floats to 4 decimal places where applicable (e.g., `0.5000`).

The working directory `/home/user/` already contains `reference.csv`. 
You can use `rustc` to compile a single-file script (e.g., `percolation.rs`) without needing a full Cargo project, as no external crates (like `rand`) are allowed or necessary. 

Please write the script, run it, and ensure `/home/user/results.csv` is correctly created.