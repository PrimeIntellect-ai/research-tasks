You are an ML Engineer preparing a training dataset for a Physics-Informed Neural Network (PINN) that models steady-state heat distribution. 

Your task is to write a C++ program that generates spatial temperature data, solves a non-linear physical constraint, and statistically compares the results against a baseline dataset.

Please write a C++ program at `/home/user/pinns_data/generate_data.cpp` and run it to produce the required outputs.

**Task Requirements:**
1. **Mesh Refinement**: Generate a 1D spatial mesh for the domain parameter $S \in [0, 10]$. The baseline data used a uniform coarse mesh, but for training, we need a refined mesh in the upper half of the domain. 
   Generate exactly these 16 points for $S$: 
   `0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0`.

2. **Non-Linear Equation Solving**: For each point $S_i$, the physical temperature $T_i$ follows the non-linear relationship:
   $T_i^3 + 2T_i - S_i = 0$
   Implement the Newton-Raphson method in your C++ program to solve for $T_i$ for each $S_i$. 
   - Use an initial guess of $T = 1.0$.
   - Use a tolerance of $10^{-6}$.
   - Maximum iterations: 100.

3. **Statistical Hypothesis Comparison**: 
   Read the baseline temperature data from `/home/user/pinns_data/baseline.txt`. This file contains 16 floating-point values (one per line) corresponding to the baseline temperatures at the 16 mesh points.
   Compute the Mean Squared Error (MSE) between your calculated $T$ values and the baseline $T$ values.
   Our Null Hypothesis ($H_0$) is that the generated theoretical data does not significantly deviate from the experimental baseline. We define the threshold for significance as an MSE of `0.05`.
   - If MSE < 0.05, the hypothesis is accepted.
   - If MSE >= 0.05, the hypothesis is rejected.

4. **Outputs**:
   Your program must write a summary file to `/home/user/pinns_data/stats.txt` with exactly two lines:
   Line 1: `MSE: <calculated_mse_value>` (formatted to 4 decimal places)
   Line 2: `H0: Accepted` OR `H0: Rejected`

Compile your program using `g++ -O3 generate_data.cpp -o generate_data` and run it so that the `stats.txt` file is generated.