You are a scientific computing researcher investigating the numerical stability of Euler's method for a stiff Ordinary Differential Equation (ODE). 

You have been provided with a Python solver at `/home/user/euler_ode.py`. This script takes a single argument, the time step `dt`, and prints the final simulated value of the system at time t=10.0. 
You also have a regression baseline file at `/home/user/baseline.txt` containing the expected final value for `dt=0.2` from a trusted previous run.

Your objective is to write and execute a Bash script (`/home/user/run_tests.sh`) that automates numerical stability and regression testing.

Your Bash script must perform the following exactly:
1. Iterate over the following `dt` values: `0.2`, `0.8`, `1.2`, `2.0`.
2. For each `dt`, execute `/home/user/euler_ode.py <dt>` and capture the output.
3. Determine the numerical stability of the run. A run is considered `STABLE` if the absolute final value is less than `10.0`. If the absolute final value is `10.0` or greater, it is considered `UNSTABLE`.
4. Output the results to a CSV file at `/home/user/stability_report.csv` with the exact header `dt,final_value,status`. Each row should contain the step size, the exact string output from the Python script, and the status (`STABLE` or `UNSTABLE`).
5. After processing all `dt` values, perform a regression check. Compare the captured output for `dt=0.2` strictly against the contents of `/home/user/baseline.txt`. If they match exactly, append a final line `REGRESSION_CHECK:PASS` to `/home/user/stability_report.csv`. If they do not match, append `REGRESSION_CHECK:FAIL`.

Requirements:
- Ensure the Bash script is executable and run it so the CSV is generated.
- Use tools like `bc` or `awk` within your Bash script to handle floating-point absolute value comparisons.
- Do not modify `/home/user/euler_ode.py` or `/home/user/baseline.txt`.
- The final output must be precisely written to `/home/user/stability_report.csv`.