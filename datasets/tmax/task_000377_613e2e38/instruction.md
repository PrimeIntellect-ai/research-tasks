You are assisting a bioinformatics researcher simulating isothermal DNA amplification. The lab has a model for continuous DNA amplification: the concentration $y(t)$ follows a logistic growth curve dictated by the ordinary differential equation (ODE):

$$ \frac{dy}{dt} = r y \left(1 - \frac{y}{K}\right) $$

where $K = 1000$ is the carrying capacity (maximum concentration) and $y(0) = 1$ is the initial concentration. 
The growth rate $r$ depends on the sequence being amplified. Specifically, $r = 2.0 \times \text{GC\_fraction}$, where the $\text{GC\_fraction}$ is the proportion of 'G' and 'C' bases in the target DNA sequence.

Previously, the researcher tried using a simple Euler method with a fixed time-step of $\Delta t = 1.5$, but the numerical integrator diverged due to wrong step-size adaptation (the step size was too large for the rate $r$, causing massive oscillations).

Your task is to create a robust, reproducible Python pipeline to solve this correctly:
1. Read the target DNA sequence from `/home/user/target.fasta`. Calculate the GC fraction and the resulting rate $r$.
2. Compute the exact analytical solution for logistic growth at integer time points $t = 0, 1, 2, \dots, 10$. The analytical solution is $y_{exact}(t) = \frac{K}{1 + (\frac{K}{y_0} - 1)e^{-rt}}$.
3. Compute the numerical solution using a stable approach (you can use `scipy.integrate.solve_ivp`, or a custom Euler/Runge-Kutta method with a small enough step size, e.g., $\Delta t \le 0.01$ to prevent divergence).
4. Extract the numerical results at the exact integer time points $t = 0, 1, \dots, 10$.
5. Save the parameters to `/home/user/params.json`. It must contain exactly two keys: `"gc_fraction"` (float) and `"r"` (float).
6. Save the time-series results to `/home/user/results.csv`. The CSV must have exactly three columns with headers: `t,y_num,y_exact`. The `y_num` and `y_exact` values should be the numerical and analytical concentrations, respectively, at those integer time points.

Ensure your numerical solution `y_num` closely matches `y_exact` (within a 1% error margin at all points). Write your pipeline in a script at `/home/user/simulate.py` and run it to produce the final outputs.