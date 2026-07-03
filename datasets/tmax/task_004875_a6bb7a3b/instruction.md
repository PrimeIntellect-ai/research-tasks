You are an assistant helping a computational biology researcher analyze a two-protein interaction model and optimize its initial conditions for a synthetic biology application.

The interaction between Protein X and Protein Y is governed by the following system of non-linear ordinary differential equations (ODEs):
dx/dt = -a * x + b * y
dy/dt = c * x - d * y^2

You have been provided with experimental time-series data of these protein concentrations in `/home/user/experiment_data.csv`. 

Your task is to:
1. Set up a Python environment. You may install `numpy`, `scipy`, and `pandas` as needed.
2. **Curve Fitting:** Write a script to fit the parameters `a`, `b`, `c`, and `d` of the ODE system to the provided experimental data. Minimize the sum of squared errors (SSE) between the simulated and observed concentrations of both X and Y. Assume all parameters are bounded between 0.0 and 2.0. The initial conditions for the experimental data are x(0) = 1.0 and y(0) = 2.0.
3. **Optimization:** Using your fitted parameters (a, b, c, d), find the optimal initial conditions `x0` and `y0` that MAXIMIZE the total integral of (x(t) + y(t)) over the time period t = 0 to t = 10. 
   - The initial conditions are bounded: x0 in [0.0, 5.0] and y0 in [0.0, 5.0].
   - Use `scipy.integrate.odeint` or `solve_ivp` for the simulation.
   - Use `scipy.integrate.trapz` or `simpson` (or similar) to calculate the integral.
   - Use an optimization routine from `scipy.optimize` (e.g., differential_evolution, minimize) to find the maximum integral. (Hint: minimize the negative integral).

Finally, output your results to a JSON file at `/home/user/results.json` with exactly the following structure (round all floating point values to 3 decimal places):
```json
{
  "a": 0.000,
  "b": 0.000,
  "c": 0.000,
  "d": 0.000,
  "optimal_x0": 0.000,
  "optimal_y0": 0.000,
  "max_integral": 0.000
}
```