You are a data scientist tasked with fitting a first-order kinetic decay model to some noisy experimental data, evaluating the stability of numerical solvers for this model, and performing a Monte Carlo uncertainty quantification.

You have been provided with a dataset at `/home/user/observations.csv` containing 1,000 independent measurements of a chemical concentration taken at time $t=5$ seconds. The initial concentration at $t=0$ was exactly 100 for all these measurements.

The underlying process is modeled by the ordinary differential equation (ODE):
$dC/dt = -k \cdot C$

Please complete the following workflow:

1. **Bootstrap Confidence Interval**: Compute the sample mean of the observations in `/home/user/observations.csv`. Then, use the percentile bootstrap method to calculate the 95% confidence interval for this mean. Use exactly 10,000 bootstrap resamples. Let $C_{mean}$ be the sample mean of the original data. 
*(Note: To ensure reproducible results, use Python 3 and `numpy.random.seed(42)` for generating your bootstrap resamples. Draw samples of the same size as the dataset with replacement).*

2. **Parameter Fitting**: Using the exact analytical solution to the ODE, calculate the decay rate constant $k$ such that an initial concentration $C(0) = 100$ yields exactly $C(5) = C_{mean}$. 

3. **Monte Carlo Simulation**: The initial concentration in real-world scenarios is not exactly 100, but rather uniformly distributed: $C(0) \sim U(90, 110)$. Using the parameter $k$ calculated in Step 2, run a Monte Carlo simulation with 100,000 samples to find the expected (mean) concentration at $t=5$. Use the exact analytical solution for $C(5)$ in this simulation. 
*(Note: Use `numpy.random.seed(42)` and `numpy.random.uniform` to generate the initial concentrations).*

4. **Numerical Stability Testing**: Analytical solutions are not always available. Implement the Forward Euler method to solve $dC/dt = -k \cdot C$ from $t=0$ to $t=5$ with $C(0)=100$. Use the $k$ calculated in Step 2. 
Calculate the final concentration $C(5)$ using two different time steps: $\Delta t = 0.5$ and $\Delta t = 0.01$. Compute the absolute difference between these two numerical estimates: $|C_{Euler\_0.5}(5) - C_{Euler\_0.01}(5)|$.

Output your final results into a JSON file located at `/home/user/solution.json` with the following keys, rounding all values to 4 decimal places:
- `"bootstrap_lower"`: The lower bound of the 95% CI from Step 1.
- `"bootstrap_upper"`: The upper bound of the 95% CI from Step 1.
- `"k_value"`: The calculated rate constant $k$ from Step 2.
- `"mc_mean_c5"`: The mean concentration at $t=5$ from the Monte Carlo simulation in Step 3.
- `"euler_diff"`: The absolute difference from the stability test in Step 4.