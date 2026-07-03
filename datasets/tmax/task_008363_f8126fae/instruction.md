You are acting as a bioinformatics software engineer. We are modeling the concentration of a specific metabolite across a population of 500 synthetic cells, where each cell's base production rate is determined by its genetic sequence. 

However, we are running into precision and convergence issues. Our current naive summation of concentrations leads to floating-point truncation errors (reduction order artifacts), and we aren't sure what integration step size is optimal.

Your task is to write a C program that calculates the final total concentration across all cells and solves these numerical issues.

**Model details:**
For each cell's sequence in `/home/user/data/sequences.fasta`:
1. Calculate the GC-content: $k = \frac{\text{count of G and C}}{\text{total sequence length}}$.
2. Simulate the metabolite concentration $y(t)$ using the ODE:
   $$\frac{dy}{dt} = k \cdot y - 0.05 \cdot y^2$$
3. The initial condition for all cells is $y(0) = 2.0$.
4. The simulation runs from $t = 0$ to $t = 100$.

**Requirements for your C program (`/home/user/simulate.c`):**
1. **ODE Numerical Solving:** Implement the standard 4th-order Runge-Kutta (RK4) method to solve the ODE.
2. **Convergence Testing:** Your program must dynamically determine the optimal step size $dt$. Start with $dt = 1.0$. Halve the step size ($1.0, 0.5, 0.25, 0.125 \dots$) and re-run the *entire* population simulation until the absolute difference in the **total final population concentration** (sum of $y(100)$ for all cells) between step $dt$ and $dt/2$ is strictly less than $1 \times 10^{-5}$.
3. **Precision Summation:** Because we are summing hundreds of floating-point values and need high precision, you must use **Kahan summation** to aggregate the final concentrations $y(100)$ across the 500 cells. Standard `+=` accumulation is not acceptable. Use `double` precision for all calculations.

**Outputs:**
Compile your C program (you may need to install `gcc` and link the math library). Run it and produce two output files:
1. `/home/user/dt_chosen.txt`: containing only the chosen step size $dt$ (the larger of the two $dt$ values that satisfied the convergence threshold), formatted to 4 decimal places (e.g., `0.2500`).
2. `/home/user/result.txt`: containing the final Kahan-summed concentration for the population using the chosen $dt$, formatted to exactly 6 decimal places.

**Setup:**
The FASTA file is located at `/home/user/data/sequences.fasta`. You should write your code, compile it, and generate the required output files.