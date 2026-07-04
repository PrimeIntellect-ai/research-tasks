You are a data scientist analyzing pharmacokinetic data for a new drug. The drug undergoes a 2-compartment transformation in the body:
Compound A metabolizes into Compound B at rate $k_1$.
Compound B is eliminated from the body at rate $k_2$.

The Ordinary Differential Equations (ODEs) are:
$dA/dt = -k_1 A$
$dB/dt = k_1 A - k_2 B$
Initial conditions at $t=0$: $A(0) = 100$, $B(0) = 0$.

You have a file `/home/user/raw_obs.txt` containing observational data from clinical trials. 
Your task is to fit the parameters $k_1$ and $k_2$ using a Monte Carlo approach, validate the fit analytically, and classify the patient.

Step 1: Data Reshaping (Bash)
The file `/home/user/raw_obs.txt` is pipe-separated with columns: `timestamp_string | time_hours | subject_id | B_concentration | status`.
Write a shell command or bash script to extract only the rows where `subject_id` is exactly `42`. 
Save the `time_hours` and `B_concentration` columns as a comma-separated file at `/home/user/clean_obs.csv` (include a header `time,B_conc`).

Step 2: Monte Carlo ODE Fitting (Python)
Write a Python script `/home/user/mc_fit.py` that:
1. Reads `/home/user/clean_obs.csv`.
2. Uses Monte Carlo simulation to find the best $k_1$ and $k_2$ parameters. Specifically, set `numpy.random.seed(42)` and generate exactly 100,000 random parameter pairs where $k_1 \sim Uniform(0.1, 1.0)$ and $k_2 \sim Uniform(0.1, 1.0)$.
3. For each pair, numerically solve the ODE system at the time points in the CSV.
4. Find the pair that minimizes the Mean Squared Error (MSE) between the numerical $B(t)$ and the observed `B_conc`.
5. Save the best parameters to `/home/user/best_params.json` in the format `{"k1": 0.123, "k2": 0.456}` (keep 3 decimal places).
6. Save the numerical solution for $B(t)$ using the best parameters to `/home/user/best_fit_curve.csv` (header: `time,B_num`).

Step 3: Analytical Validation and Classification (R)
Write an R script `/home/user/validate.R` that:
1. Reads `/home/user/best_params.json` and `/home/user/best_fit_curve.csv`.
2. Calculates the exact analytical solution for $B(t)$ using the $k_1$ and $k_2$ values from the JSON. 
   *(Hint: $B(t) = \frac{k_1 A_0}{k_2 - k_1} (e^{-k_1 t} - e^{-k_2 t})$)*
3. Validates the numerical solution by checking if the maximum absolute difference between the numerical $B(t)$ (from the CSV) and the analytical $B(t)$ is strictly less than 0.05.
4. Reads `/home/user/reference.json` to get the `k2_threshold`.
5. Creates a file `/home/user/validation_result.txt` containing two lines:
   - Line 1: `VALID` if the max difference < 0.05, else `INVALID`
   - Line 2: `FAST` if best $k_2 >$ threshold, else `SLOW`

Execute all your scripts to generate the final output files.