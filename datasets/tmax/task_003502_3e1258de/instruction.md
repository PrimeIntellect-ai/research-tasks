You are helping a data scientist debug a model fitting pipeline. They are trying to simulate a chemical reaction system using ordinary differential equations (ODEs), but the numerical integrator is failing. The integration takes forever or diverges because the explicit Runge-Kutta method (`RK45`) currently implemented cannot handle the stiffness of the system without an extremely fine step-size.

Your task is to fix the script and compute the final state.

1. Create a Python virtual environment at `/home/user/scienv`.
2. Install the necessary scientific libraries (`numpy` and `scipy`) within this virtual environment.
3. A script is located at `/home/user/stiff_model.py`. Modify this script so that:
   - It uses the `BDF` method (Backward Differentiation Formula) in `scipy.integrate.solve_ivp` to handle the stiff ODE.
   - It sets the relative tolerance (`rtol`) to `1e-6` and the absolute tolerance (`atol`) to `1e-10`.
4. Run the fixed script using the python interpreter from your newly created virtual environment.
5. The script must output the final state of the system at $t = 10^5$ into a JSON file located at `/home/user/results.json`. The JSON should have exactly the following structure containing the final values of the three state variables:
```json
{
  "y1_final": <float>,
  "y2_final": <float>,
  "y3_final": <float>
}
```

Do not change the system of equations, initial conditions, or the time span ($0$ to $10^5$).