You are an environmental data scientist modeling the concentration of a contaminant along a 1D pipe system. The raw sensor data is located at `/home/user/spatial_data.csv` with columns `x` (distance) and `y` (concentration).

Your task is to write and execute a Python script that analyzes this data by performing curve fitting, domain refinement, and root finding.

Follow these steps exactly:
1. **Environment Setup:** Create a Python virtual environment at `/home/user/fit_env`. Activate it and install `numpy`, `scipy`, and `pandas`.
2. **Curve Fitting:** Fit the data to the following nonlinear Gaussian-plus-background model:
   $y(x) = A \cdot \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right) + C$
   Extract the best-fit parameters for $A$ (amplitude), $\mu$ (center/peak), $\sigma$ (standard deviation), and $C$ (background). Constrain or absolute-value your results such that $A > 0$ and $\sigma > 0$.
3. **Mesh Refinement:** The sensor data is sparse. Define a refined 1D computational mesh (using `numpy.linspace`) consisting of exactly 500 evenly spaced points from $\mu - 2\sigma$ to $\mu + 2\sigma$ (inclusive).
4. **Nonlinear Equation Solving:** We need to find the exact location on the right side of the contaminant plume (where $x > \mu$) where the concentration drops to exactly $y(x) = 3.0$. Use a root-finding method (e.g., `scipy.optimize.fsolve` or `root_scalar`) with your fitted model to find this specific $x$ value. Call this `x_target`.
5. **Output:** Save your final results to `/home/user/solution.json`. The JSON must contain the exact keys below, with all values rounded to exactly 4 decimal places:
   ```json
   {
     "A": 0.0000,
     "mu": 0.0000,
     "sigma": 0.0000,
     "C": 0.0000,
     "x_target": 0.0000
   }
   ```

Do not modify the original data file. Only output the `solution.json` file once you have computed the correct values.