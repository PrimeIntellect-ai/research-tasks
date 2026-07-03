I need you to write a C++ program to simulate the 2D diffusion of a pollutant and then estimate the resulting probability density parameters. I am running simulations on a server and need this to be highly reproducible and reasonably fast.

Here are the specific requirements for the simulation:
1. **Grid and Initial State:**
   - Create a 2D grid of size 1000x1000 (x from 0 to 999, y from 0 to 999).
   - The initial concentration `C` is `0.0` everywhere, except for a 10x10 block from `x = 400` to `409` (inclusive) and `y = 600` to `609` (inclusive), where `C = 100.0`.

2. **PDE Solving:**
   - Simulate the 2D diffusion equation: $\frac{\partial C}{\partial t} = D \left( \frac{\partial^2 C}{\partial x^2} + \frac{\partial^2 C}{\partial y^2} \right)$
   - Use a simple explicit finite difference method.
   - Set the diffusion coefficient `D = 0.1`.
   - Set spatial steps `dx = 1.0` and `dy = 1.0`.
   - Set the time step `dt = 1.0`.
   - Run the simulation for exactly `1000` time steps.
   - Use fixed boundary conditions `C = 0.0` at the edges of the grid (`x=0`, `x=999`, `y=0`, `y=999`).

3. **Parallel Computation:**
   - You must use OpenMP to parallelize the spatial grid updates to speed up the computation. Compile your code using `-fopenmp` and `-O3`.

4. **Density Estimation (Statistical Analysis):**
   - After the 1000 steps, treat the resulting 2D grid as an unnormalized 2D probability density function.
   - Calculate the following moments of the distribution:
     - Total Mass (`M`): The sum of all values in the grid.
     - Center of Mass / Mean (`mu_x`, `mu_y`): The expected value of `x` and `y`.
     - Variance (`var_x`, `var_y`): The population variance of `x` and `y` relative to the center of mass.
     - Covariance (`cov_xy`): The population covariance between `x` and `y`.

Write your code to `/home/user/diffusion.cpp`, compile it to an executable at `/home/user/diffusion`, and run it.

The program must output a file at `/home/user/results.log` exactly in this format (use 2 decimal places for all floating-point values):
```
M=...
mu_x=...
mu_y=...
var_x=...
var_y=...
cov_xy=...
```

Do not output any other text in the `results.log` file.