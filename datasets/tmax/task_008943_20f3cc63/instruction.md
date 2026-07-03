You are a performance engineer tasked with profiling and optimizing a statistical analysis of an epidemiological model. We have observational data for an infectious disease spread, and we need to run a parameter sweep over an ODE (Ordinary Differential Equation) model to find the best-fitting parameters using parallel computing.

Your task is to create the following files in `/home/user/`:
1. `/home/user/run_analysis.sh`: A bash script that orchestrates the entire workflow.
2. `/home/user/sweep.py`: A Python script that solves the ODE, computes statistics, and uses multiprocessing.

### Step 1: Data Reshaping
A file named `/home/user/obs_data.txt` contains observational data in a wide format:
```
day,1,2,3,4,5
infected,10,25,50,80,110
```
Your `run_analysis.sh` script must first reshape this data into a standard CSV format and save it to `/home/user/obs_reshaped.csv` with the headers `day,infected` and one observation per line.

### Step 2: Parallel ODE Solving and Statistical Analysis
Write the Python script `/home/user/sweep.py` to do the following:
- Read `/home/user/obs_reshaped.csv`.
- Implement the standard SIR (Susceptible, Infected, Recovered) ODE model:
  - `dS/dt = -beta * S * I / N`
  - `dI/dt = beta * S * I / N - gamma * I`
  - `dR/dt = gamma * I`
- Total population `N = 1000`. Initial conditions at `t=1` are `S=990`, `I=10`, `R=0`.
- Use `scipy.integrate.odeint` to evaluate the model at `t = [1, 2, 3, 4, 5]`.
- Use Python's `multiprocessing` module to run the simulation in parallel for these four parameter combinations:
  - `beta=0.5, gamma=0.1`
  - `beta=0.6, gamma=0.1`
  - `beta=0.5, gamma=0.2`
  - `beta=0.6, gamma=0.2`
- Compute the Sum of Squared Errors (SSE) between the simulated `I` values and the observed `infected` values for the 5 days.
- Save the results of the parameter combination with the lowest SSE to `/home/user/best_params.json` in this exact format:
  `{"beta": <best_beta>, "gamma": <best_gamma>, "sse": <lowest_sse>}`
  (Round the SSE to 2 decimal places).

### Step 3: Profiling
In `run_analysis.sh`, after the data reshaping step, execute the Python script using `cProfile` to profile its execution time:
`python3 -m cProfile -s tottime /home/user/sweep.py > /home/user/profile.log`

Make sure `run_analysis.sh` is executable (`chmod +x`). All scripts must be fully automated.