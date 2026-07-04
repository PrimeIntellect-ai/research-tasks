I am a researcher studying chemical diffusion across molecular interaction networks. I have a custom Python package for simulating these dynamics, but my numerical integrator is currently diverging and crashing my simulations. 

I need you to fix the package, run the simulation, and perform a statistical analysis of the output.

Here are the details:
1. **The Broken Package**: I have vendored my simulation package at `/app/mol_sim`. It simulates reaction-diffusion ODEs on randomly generated graphs. Recently, I tried implementing an adaptive step-size Runge-Kutta integrator in `/app/mol_sim/mol_sim/integrator.py`, but it diverges or produces `NaN` values due to a wrong step-size adaptation formula. The correct formula for the step size multiplier in a 4th/5th order method should use the exponent `0.2` (i.e., `(tol/error)**0.2`), but I suspect there's a typo in the power. Fix the package and install it in the current environment.

2. **Run the Simulation**: Once fixed, run the provided script at `/home/user/run_sim.py`. It will use the `mol_sim` package to simulate the network and output the time-series data to `/home/user/sim_output.csv`. The CSV has columns `time` and `node_X` for various nodes.

3. **Data Analysis**: Write a script (in any language you prefer, such as Python or R) to process `/home/user/sim_output.csv`. You must:
   - Extract the concentration of `node_0` over time.
   - **Curve fitting**: Fit an exponential decay model: $y(t) = A \cdot \exp(-k \cdot t)$ to `node_0`'s data to estimate the decay rate $k$.
   - **Bootstrap confidence intervals**: Perform random resampling with replacement (bootstrap) of the residuals or the data points (at least 500 iterations) to calculate the 95% confidence interval for the parameter $k$.
   - **Statistical hypothesis comparison**: Fit a baseline linear model $y(t) = m \cdot t + b$ to the same data. Compare the two models using Mean Squared Error (MSE). Determine which model is the better fit (exponential or linear).

4. **Output Format**: Write your final results to `/home/user/analysis.json` exactly in this format:
   ```json
   {
       "estimated_k": 0.1234,
       "ci_95_lower": 0.1100,
       "ci_95_upper": 0.1300,
       "better_model": "exponential"
   }
   ```
   (Note: Use either `"exponential"` or `"linear"` for the `better_model` field).

Please execute the fix, run the simulation, and generate the JSON file. Ensure your estimated $k$ is highly accurate.