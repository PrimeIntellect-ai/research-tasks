You are a researcher studying the population dynamics of a viral infection using the classic Susceptible-Infected (SI) epidemic model. You need to simulate the epidemic under two different sets of transmission parameters, compare the maximum infection loads using a probability distribution distance metric, and estimate the confidence interval of this distance.

Perform the following tasks in the Linux terminal:

1. **Environment Setup**: 
   Create a Python virtual environment at `/home/user/sim_env`. Activate it and install `numpy` and `scipy`. All subsequent Python executions should use this environment.

2. **Simulation and Analysis Script**:
   Write a Python script at `/home/user/analyze_epidemic.py` that does the following:

   **A. ODE System**:
   Define the SI model as a system of Ordinary Differential Equations (ODEs):
   - $dS/dt = -\beta \cdot S \cdot I$
   - $dI/dt = \beta \cdot S \cdot I - \gamma \cdot I$
   
   Where $S$ is the susceptible population, $I$ is the infected population, $\beta$ is the transmission rate, and $\gamma$ is the recovery rate.

   **B. Parameter Sampling**:
   - Set $\gamma = 0.15$.
   - Initial conditions: $S(0) = 99.0$, $I(0) = 1.0$.
   - Time span for integration: $t \in [0, 50]$. Evaluate the solution at exactly 100 evenly spaced time points from 0 to 50 (inclusive). Use `scipy.integrate.solve_ivp` with the default `RK45` method.
   - Initialize `numpy.random.seed(42)`.
   - Sample 500 values for $\beta$ for **Group 1** from a Normal distribution with $\mu = 0.30$ and $\sigma = 0.02$.
   - Sample 500 values for $\beta$ for **Group 2** from a Normal distribution with $\mu = 0.28$ and $\sigma = 0.02$.

   **C. Simulation**:
   For each sampled $\beta$ in Group 1, solve the ODE and find the *maximum* value of the infected population $I(t)$ over the evaluated time points. Store these 500 maximum values in an array $D_1$. 
   Repeat the process for Group 2 to create an array $D_2$.

   **D. Distance Metric**:
   Calculate the 1-D Wasserstein distance between the distributions $D_1$ and $D_2$ using `scipy.stats.wasserstein_distance`.

   **E. Bootstrap Confidence Interval**:
   Calculate the 95% bootstrap confidence interval for this Wasserstein distance:
   - Set `numpy.random.seed(100)` specifically before the bootstrap loop begins.
   - Perform 1000 bootstrap iterations. In each iteration:
     - Resample 500 indices with replacement from Group 1.
     - Resample 500 indices with replacement from Group 2.
     - Calculate the Wasserstein distance between the resampled $D_1$ and resampled $D_2$.
   - Calculate the 2.5th and 97.5th percentiles of these 1000 bootstrap distances using `numpy.percentile` to get the lower and upper bounds of the 95% confidence interval.

3. **Output Generation**:
   The script must save the results to a JSON file at `/home/user/results.json` with exactly the following structure (round all floats to 4 decimal places):
   ```json
   {
     "wasserstein_distance": 0.0000,
     "ci_lower": 0.0000,
     "ci_upper": 0.0000
   }
   ```

Execute your script to generate the final `results.json` file.