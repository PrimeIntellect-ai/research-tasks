I am a researcher running statistical physics simulations, and I need your help setting up my environment and writing a Python script to compute a specific path integral. 

I need you to simulate the overdamped Langevin dynamics of a particle in a double-well potential and calculate the statistical properties of the path integral of its squared position.

Please perform the following steps:

1. **Environment Setup:**
   - Create a Python virtual environment at `/home/user/sim_env`.
   - Install `numpy` and `scipy` within this virtual environment.

2. **Simulation Script:**
   - Write a script at `/home/user/run_sim.py` that uses the virtual environment's Python.
   - The particle's position $x_t$ follows the Stochastic Differential Equation (Euler-Maruyama method):
     $x_{t+dt} = x_t + F(x_t)dt + \sqrt{2D \cdot dt} \cdot Z$
     where $Z \sim \mathcal{N}(0,1)$ is a standard normal random variable.
   - The potential is $V(x) = \frac{1}{4}x^4 - \frac{1}{2}x^2$.
   - The force $F(x) = -V'(x)$. **Constraint:** Do not calculate the derivative analytically. You must calculate $F(x)$ using a numerical central difference method with a step size of $h = 10^{-5}$: $V'(x) \approx \frac{V(x+h) - V(x-h)}{2h}$.
   - Simulation Parameters:
     - Number of paths (Monte Carlo samples): $N_{paths} = 5000$
     - Time step: $dt = 0.01$
     - Number of steps: $N_{steps} = 1000$ (Total time $T = 10$)
     - Diffusion coefficient: $D = 0.5$
     - Initial condition: $x_0 = -1.0$ for all paths.
   - **Randomness:** To ensure reproducibility, you MUST set the random seed globally using `numpy.random.seed(42)` at the very beginning of your simulation logic. Generate all the normal random variables for the entire simulation at once using `Z = numpy.random.standard_normal((N_paths, N_steps))` and use the slice `Z[:, i]` for the $i$-th time step ($0$-indexed).

3. **Numerical Integration:**
   - For each of the 5000 generated paths, compute the time integral of the squared position:
     $Y = \int_0^{10} (x_t)^2 dt$
   - You must use the Trapezoidal rule for this numerical integration (`scipy.integrate.trapezoid`, integrating along the time axis with `dx=dt`). Make sure your path arrays include the initial position at $t=0$, meaning each path has 1001 points.

4. **Statistical Output:**
   - Calculate the statistical mean ($\mu_Y$) and sample standard deviation ($\sigma_Y$) of the 5000 integral values (use `ddof=1` for the standard deviation).
   - The script should write exactly one line to `/home/user/results.txt` in the following format (rounded to 4 decimal places):
     `Mean: <mean_value>, StdDev: <std_value>`

Execute the script so the output file is generated. Let me know when you are done.