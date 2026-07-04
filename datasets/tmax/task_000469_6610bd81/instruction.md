You are an AI assistant helping a data scientist debug and automate a model fitting workflow. The scientist is analyzing a chemical decay process where the concentration $y$ over time $t$ is governed by the differential equation:
$dy/dt = -0.5 \cdot y^2$

The previous manual Euler-based numerical integrator kept diverging due to wrong step-size adaptation. You need to create a robust, reproducible workflow using a notebook, bootstrap statistics, and virtual environments.

Follow these steps exactly:

1. Create a Python virtual environment at `/home/user/venv` and install `numpy`, `scipy`, `jupyter`, and `papermill`. 
2. Create a Jupyter Notebook named `/home/user/analysis.ipynb` that does the following:
   - Contains a parameter cell (tagged with `parameters`) that defines an integer variable `n_bootstrap` (default to 1000).
   - Reads initial concentrations ($y_0$) from `/home/user/y0.txt`.
   - Uses `scipy.integrate.solve_ivp` with the `Radau` method (to handle potentially stiff dynamics and avoid divergence) to integrate the ODE from $t=0$ to $t=5$ for each $y_0$.
   - Collects the final concentrations $y(5)$ for all initial conditions.
   - Sets the random seed explicitly using `numpy.random.seed(42)`.
   - Performs a bootstrap analysis (with replacement) on the collected $y(5)$ values using `n_bootstrap` iterations to estimate the 95% confidence interval of the **mean** of $y(5)$.
   - Uses `numpy.percentile` (at 2.5 and 97.5) to calculate the lower and upper bounds.
   - Saves the confidence interval to a file named `/home/user/ci_results.txt` as two comma-separated floats: `lower_bound,upper_bound`.

3. Write a bash script `/home/user/run_analysis.sh` that:
   - Activates the virtual environment at `/home/user/venv`.
   - Uses `papermill` to execute `/home/user/analysis.ipynb`, saving the output notebook to `/home/user/analysis_out.ipynb`.
   - Passes the parameter `n_bootstrap=5000` to the notebook via the `papermill` command.

Ensure that running `bash /home/user/run_analysis.sh` executes the full pipeline successfully from start to finish.