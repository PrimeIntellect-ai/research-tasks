You are an ML Engineer preparing training data for a Physics-Informed Neural Network (PINN) that learns fluid dynamics and heat transfer. You need to write a highly optimized Go program that simulates 2D heat diffusion over a grid, then automatically validates the numerical result against the known analytical solution to ensure the training data is physically accurate.

Your task:
1. Initialize a Go module in `/home/user/diffusion`.
2. Write a Go program in `/home/user/diffusion/simulate.go` that simulates the 2D heat equation using the explicit forward Euler finite difference method.

Simulation Parameters:
- **Grid size:** $50 \times 50$ (indices $0$ to $49$ for both $x$ and $y$).
- **Spatial resolution:** $\Delta x = 1.0$, $\Delta y = 1.0$.
- **Time step:** $\Delta t = 0.1$.
- **Thermal diffusivity:** $\alpha = 1.0$.
- **Number of time steps:** $100$ (Total simulation time $T = 10.0$).
- **Boundary conditions:** Dirichlet boundaries fixed at $0.0$ (i.e., the edges $x=0$, $x=49$, $y=0$, $y=49$ are always $0.0$).
- **Initial conditions ($t=0$):** $u(x,y) = 0.0$ for all cells, except the center cell at $(25, 25)$ which has an initial heat impulse of $u(25, 25) = 1000.0$.

The update rule for the interior cells is:
$u(x,y, t+\Delta t) = u(x,y, t) + \alpha \Delta t \left[ \frac{u(x+1,y, t) - 2u(x,y, t) + u(x-1,y, t)}{\Delta x^2} + \frac{u(x,y+1, t) - 2u(x,y, t) + u(x,y-1, t)}{\Delta y^2} \right]$

Validation:
After completing the $100$ time steps, validate your numerical grid against the exact analytical solution for a point source in an infinite 2D plane:
$u_{exact}(x,y,T) = \frac{Q}{4 \pi \alpha T} \exp\left(-\frac{(x - x_0)^2 + (y - y_0)^2}{4 \alpha T}\right)$
where $Q = 1000.0$, $x_0 = 25$, $y_0 = 25$, and $T = 10.0$.

Calculate the Mean Squared Error (MSE) between the numerical grid and the analytical solution ONLY for the central $10 \times 10$ subgrid (from $x=20$ to $x=29$ inclusive, and $y=20$ to $y=29$ inclusive). 

Output Requirement:
Your Go program must calculate this MSE and write it to a log file located exactly at `/home/user/mse_validation.log`.
The file should contain exactly one line formatted as follows:
`MSE: <value>`
(Replace `<value>` with the calculated MSE, formatted to exactly 6 decimal places).

Run your Go program to generate the log file.