You are a data scientist tasked with fitting an epidemic model to observed data and creating a reproducible analysis pipeline. You have been provided with a noisy time-series dataset of infected individuals in `/home/user/observed_data.csv`.

Your goal is to compare two hypotheses for the epidemic parameters, select the best fit, and perform a Monte Carlo simulation to estimate the distribution of the peak infection count under the winning model.

**Model Specification:**
Use the deterministic SIR (Susceptible-Infected-Recovered) ODE model:
- dS/dt = -beta * S * I / N
- dI/dt = (beta * S * I / N) - gamma * I
- dR/dt = gamma * I

Initial conditions: N = 1000, S(0) = 995, I(0) = 5, R(0) = 0. 
Time span: t = 0 to 50 (inclusive), evaluated at integer time steps (51 points total).

**Hypotheses:**
- **H0**: beta = 0.25, gamma = 0.10
- **H1**: beta = 0.40, gamma = 0.20

**Task Steps:**
1. **ODE Numerical Solving & Hypothesis Comparison**: 
   Solve the ODE for both H0 and H1 using `scipy.integrate.solve_ivp` (use the default RK45 method, evaluate exactly at t=0, 1, ..., 50 using the `t_eval` argument). Calculate the Sum of Squared Errors (SSE) between the modeled `I(t)` and the observed `I_obs` from the CSV file. Select the hypothesis with the lower SSE.
   
2. **Monte Carlo Simulation**: 
   Using the deterministic `I(t)` trajectory of the *winning* hypothesis, perform 1000 Monte Carlo iterations to simulate observational noise. 
   - Before the loop, set the numpy random seed to `42`.
   - In each iteration, add independent Gaussian noise (mean = 0, standard deviation = 5) to the deterministic `I(t)` trajectory.
   - Clip any negative values in the noisy trajectory to 0.
   - Record the peak (maximum) infected count of this noisy trajectory.
   
3. **Statistical Summary**:
   Calculate the mean and standard deviation of the peak infected counts across the 1000 iterations.

4. **Reproducible Pipeline**:
   Write a Python script `/home/user/analysis.py` to perform the above steps.
   Create a bash script `/home/user/run_pipeline.sh` that:
   - Creates a Python virtual environment at `/home/user/venv`.
   - Activates it and installs `numpy`, `scipy`, and `pandas`.
   - Runs `analysis.py`.
   Make sure `run_pipeline.sh` is executable.

**Output Format:**
Your Python script must output a JSON file at `/home/user/results.json` with exactly the following structure (round all floats to 2 decimal places):
```json
{
  "best_hypothesis": "H0",
  "sse": 1234.56,
  "peak_mean": 150.00,
  "peak_std": 5.00
}
```