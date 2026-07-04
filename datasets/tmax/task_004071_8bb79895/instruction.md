You are acting as a research assistant for a computational physics lab. We are analyzing the spatial convergence rate of the Forward Time Centered Space (FTCS) finite difference scheme for the 1D Heat Equation.

Your task is to implement the simulation in C, orchestrate a mesh refinement study, perform a linear regression to find the convergence rate, and save the result.

**Physical and Numerical Setup:**
- **PDE:** $\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$
- **Domain:** $x \in [0, 1]$, time $t \in [0, T]$
- **Parameters:** $\alpha = 0.1$, $T = 0.5$
- **Initial Condition:** $u(x, 0) = \sin(\pi x)$
- **Boundary Conditions:** $u(0, t) = u(1, t) = 0$
- **Analytical Solution:** $u_{exact}(x, t) = \exp(-\alpha \pi^2 t) \sin(\pi x)$
- **Grid:** $N$ intervals, so $\Delta x = 1.0 / N$. There are $N+1$ spatial points: $x_0, x_1, \dots, x_N$.
- **Time Step:** To maintain stability, enforce exactly $\Delta t = \frac{\Delta x^2}{4\alpha}$. The number of time steps is $K = \frac{T}{\Delta t}$. (You may assume $T$ is perfectly divisible by $\Delta t$ for the given $N$).

**Step 1: Write the Simulation Code (`/home/user/heat.c`)**
Write a C program that takes a single command-line argument: the integer $N$.
1. Initialize the grid $u$ at $t=0$.
2. Step forward in time using the FTCS scheme: $u_i^{n+1} = u_i^n + \frac{\alpha \Delta t}{\Delta x^2} (u_{i+1}^n - 2u_i^n + u_{i-1}^n)$.
3. After reaching $t = T$, calculate the maximum absolute error over all spatial points compared to $u_{exact}(x, T)$.
4. Print ONLY the maximum absolute error to standard output (as a double, standard `printf("%f\n", error)` or scientific notation).

**Step 2: Write the Regression Code (`/home/user/regression.c`)**
Write a second C program that computes the spatial order of accuracy. 
1. It should read from standard input pairs of $(N, \text{Error})$ until EOF.
2. It must apply ordinary least squares (OLS) linear regression to the natural logarithms: $y = m x + c$, where $x = \ln(N)$ and $y = \ln(\text{Error})$.
3. Print the slope $m$ to standard output formatted exactly as: `Slope: %.3f\n`.
*Note: The theoretical order of accuracy for FTCS in space is $O(\Delta x^2)$, so expect a slope near -2.0.*

**Step 3: Orchestrate the Experiment (`/home/user/run_simulation.sh`)**
Write a bash script that:
1. Compiles both C programs using `gcc` (with `-lm` for the math library).
2. Runs `heat` for the following mesh sizes: $N = 10, 20, 40, 80$.
3. Collects the $N$ and corresponding maximum absolute errors.
4. Pipes this data into `regression` to compute the slope.
5. Saves the exact output of the regression program into `/home/user/convergence_rate.txt`.

Ensure `/home/user/run_simulation.sh` is executable and run it to produce the final `convergence_rate.txt` file. You may need to install `gcc` and `make` via the system package manager if they are missing.