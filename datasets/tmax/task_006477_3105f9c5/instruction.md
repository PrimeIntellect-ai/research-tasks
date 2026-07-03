I am a researcher running thermal simulations, and I need a Go program to solve the 1D Heat Equation using an implicit numerical method. The implicit method is unconditionally stable but requires solving a system of linear equations at each time step.

Please write a Go program at `/home/user/simulate_heat.go` that models the temperature distribution $u(x,t)$ in a 1D rod. 

Here are the specifications for the simulation:
- **Domain:** $x \in [0, 1.0]$ with spatial step $\Delta x = 0.1$ (This means 11 spatial points: $i=0, 1, ..., 10$).
- **Time:** $t \in [0, 5.0]$ with time step $\Delta t = 0.5$ (This means 11 time steps: $n=0, 1, ..., 10$).
- **Thermal diffusivity:** $\alpha = 0.01$.
- **Initial Condition:** $u(x, 0) = 0.0$ for all internal points ($0 < x < 1$).
- **Boundary Conditions:** Fixed temperatures at the ends, $u(0, t) = 0.0$ and $u(1, t) = 100.0$ for all $t$.

**Numerical Method (Backward Euler):**
The implicit discretization of the heat equation $\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$ leads to:
$-r u_{i-1}^{n+1} + (1 + 2r) u_i^{n+1} - r u_{i+1}^{n+1} = u_i^n$
where $r = \alpha \frac{\Delta t}{\Delta x^2}$.
For internal points ($i=1$ to $9$), you must construct and solve the resulting tridiagonal linear system $A u^{n+1} = b$ at each time step. 
*(Hint: Implement the Thomas Algorithm to solve the tridiagonal linear system efficiently).*

**Output Format:**
Your Go program must simulate the heat transfer over the specified time steps, storing the entire state as a 2D multi-dimensional array `[][]float64` where the outer index is the time step $n$ and the inner index is the spatial point $i$.
The program must then serialize this 2D array to a JSON file located precisely at `/home/user/heat_results.json`.

Compile and run your program so that the JSON file is generated.