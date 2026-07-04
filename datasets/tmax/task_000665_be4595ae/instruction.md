You are a researcher tasked with running a biological diffusion simulation. 

Write a C program at `/home/user/sim.c` that models the 1D diffusion of a custom oligonucleotide. 
The program must perform the following steps:
1. **Sequence Alignment**: Compute a simple alignment score between a primer sequence `ATGCGATCG` and a target sequence `ATGCGATCT`. The score is calculated by comparing characters at each position: +1 for a match, -1 for a mismatch (assume equal lengths, no gaps).
2. **PDE Setup**: Calculate the diffusion coefficient `D = score * 0.001`. 
3. **Simulation**: Solve the 1D Heat Equation (`du/dt = D * d^2u/dx^2`) on a domain `x \in [0, 1]` with `N = 101` points (so `dx = 0.01`). 
    - Initial condition: `u(x,0) = exp(-100 * (x - 0.5)^2)` for all points.
    - Boundary conditions: `u(0,t) = 0`, `u(1,t) = 0` (Dirichlet).
    - Use an explicit finite difference scheme with `dt = 0.001`.
    - Run the simulation for exactly 100 time steps.
4. **Probability Distribution Metric**: After 100 time steps, calculate the total mass (`sum` of `u` over all points) using a standard loop from `i=0` to `i=100`. 
    - Normalize the final concentration array `p_i = u_i / sum`.
    - Calculate the Kullback-Leibler (KL) divergence `D_KL(P || Q)` where `Q` is a uniform distribution over the 101 points (`q_i = 1.0 / 101`). Use the natural logarithm.

Compile your program and run it. Write the final outputs to `/home/user/result.txt` in exactly this format:
```
Score: <integer_score>
Total Mass: <float_with_6_decimal_places>
KL: <float_with_6_decimal_places>
```