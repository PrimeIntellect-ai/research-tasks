Hello, I need some help automating a parameter estimation task for a physical simulation. I am researching the aerodynamics of a falling object and need to find the optimal aerodynamic drag coefficient ($k$) that matches my experimental data. 

Since our cluster environment primarily relies on shell scripting, I need this implemented entirely using **Bash** and standard UNIX utilities (like `awk`, `bc`, `parallel`, `xargs`, etc.). 

Here is what you need to do:

1. **The Model**: The velocity $v$ of the falling object over time $t$ is described by the Ordinary Differential Equation (ODE):
   $dv/dt = 9.8 - k \cdot v \cdot |v|$
   Initial condition: $v(0) = 0$.

2. **The Data**: I have a file at `/home/user/target.txt` containing the experimental data. Each line has two space-separated columns: time ($t$) and velocity ($v$). The time goes from 0.0 to 10.0 in increments of $dt = 0.1$.

3. **The Simulation & Optimization**:
   Write a Bash workflow (you can create scripts in `/home/user/`) that performs a parallel grid search to find the optimal $k$.
   - You must evaluate $k$ from `0.01` to `0.50` in increments of `0.01` (i.e., 0.01, 0.02, ..., 0.50).
   - For each $k$, numerically integrate the ODE using the **Euler method** with $dt = 0.1$ from $t=0.0$ to $t=10.0$.
   - Calculate the Mean Squared Error (MSE) between the simulated velocities and the experimental velocities in `/home/user/target.txt`.
   - You must run the evaluations of different $k$ values in **parallel** to speed up the search (e.g., using `xargs -P` or GNU `parallel`).

4. **The Output**:
   Once your script finishes the parallel parameter sweep, it should identify the $k$ that minimizes the MSE. 
   Write the optimal value of $k$ (formatted to two decimal places, e.g., `0.23`) to a file named `/home/user/best_k.txt`.

Please write and execute the Bash scripts required to complete this task. Do not use Python, C++, or other higher-level languages for the ODE solving or optimization logic; restrict yourself to Bash, `awk`, `bc`, etc.