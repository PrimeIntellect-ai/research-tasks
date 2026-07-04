You are a bioinformatics analyst trying to model how a theoretical morphogen diffuses along a 1D strand of cells represented by a DNA sequence. You need to write a C program to simulate this diffusion and calculate a final metric.

The DNA sequence is provided in `/home/user/sequence.txt`. Each character represents a spatial point (cell) in a 1D domain. 

Here are the rules for your numerical model:
1. **Domain & Discretization:** Let $N$ be the length of the sequence. The spatial indices are $i = 0, 1, \dots, N-1$. The spatial step is $\Delta x = 1.0$.
2. **Sources & Sinks ($S_i$):** If the character at index $i$ is 'G' or 'C', it acts as a constant morphogen source with $S_i = 1.0$. If the character is 'A' or 'T', it acts as a sink with $S_i = -1.0$.
3. **Governing Equation:** The diffusion follows the explicit finite-difference approximation of the heat equation with a source term:
   $u_i^{n+1} = u_i^n + \Delta t \left( \alpha \frac{u_{i+1}^n - 2u_i^n + u_{i-1}^n}{\Delta x^2} + S_i \right)$
4. **Parameters:** Set the diffusion coefficient $\alpha = 0.5$ and the time step $\Delta t = 0.1$.
5. **Initial & Boundary Conditions:** 
   - Initial concentration: $u_i^0 = 0.0$ for all $i$.
   - Dirichlet boundary conditions: The ends are strictly fixed at zero concentration for all time steps. That means $u_0^n = 0.0$ and $u_{N-1}^n = 0.0$ always, regardless of the sequence character at those positions. (Do not update the boundaries with the PDE equation).
6. **Time Integration:** Run the simulation for exactly 2 time steps (i.e., compute $u^1$, and then use it to compute $u^2$).
7. **Spatial Integration:** After computing $u^2$, compute the definite spatial integral of the morphogen concentration across the entire domain (from $i=0$ to $i=N-1$) using the standard Trapezoidal rule.

Write a C program to perform this simulation. Once your program calculates the final integral value, write this single floating-point number to `/home/user/integral.txt`, formatted to exactly 4 decimal places (e.g., `0.0000`).