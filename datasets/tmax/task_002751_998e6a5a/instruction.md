You are a Machine Learning Engineer preparing a synthetic dataset to train a Physics-Informed Neural Network (PINN). You need to generate training data for a non-linear spring-mass-damper system, engineer specific features using numerical differentiation, and perform dimensionality reduction analysis.

The system is defined by the following second-order ordinary differential equation (ODE):
`m * x''(t) + c * x'(t) + k * x(t) + alpha * x(t)^3 = 0`

Where the parameters are:
- `m = 1.0` (mass)
- `c = 0.1` (damping coefficient)
- `k = 1.0` (linear stiffness)
- `alpha = 0.5` (non-linear stiffness)

Your tasks are:
1. **ODE Simulation:** Simulate the system for $t \in [0, 10]$ seconds. Evaluate the solution at exactly 1000 evenly spaced points (inclusive of 0 and 10). Use `scipy.integrate.solve_ivp` with `rtol=1e-6` and `atol=1e-8`.
   Generate simulations for 50 distinct initial conditions $(x_0, v_0)$. Construct these initial conditions using a nested loop where the outer loop iterates over $x_0$ and the inner loop iterates over $v_0$:
   - $x_0 \in \text{numpy.linspace}(-2, 2, 10)$
   - $v_0 \in \text{numpy.linspace}(-2, 2, 5)$

2. **Feature Engineering (Numerical Differentiation):** For each trajectory, the neural network requires the "jerk" (the rate of change of acceleration, $j(t) = a'(t)$) as an input feature.
   - First, compute the true acceleration $a(t)$ at each time step directly using the ODE formulation and the simulated $x(t)$ and $v(t)$.
   - Then, numerically differentiate this acceleration array with respect to the time array using `numpy.gradient` to approximate the jerk.
   - Keep track of the maximum absolute jerk value observed across all 50 trajectories and all time steps.

3. **Dimensionality Analysis (Matrix Decomposition):** Create a matrix $M$ of size $50 \times 1000$, where each row contains the position series $x(t)$ for one of the trajectories (ordered exactly as the loops described above).
   - Perform Singular Value Decomposition (SVD) on matrix $M$.
   - Extract the top 3 largest singular values to understand the dataset's intrinsic dimensionality.

Once you have computed these values, write a JSON file to `/home/user/ml_data_summary.json` with the following exact structure:
```json
{
  "top_3_singular_values": [val1, val2, val3],
  "max_abs_jerk": max_jerk_value
}
```

Ensure all your code is written in Python. Do not round the values in the JSON file; output them as standard high-precision floats.