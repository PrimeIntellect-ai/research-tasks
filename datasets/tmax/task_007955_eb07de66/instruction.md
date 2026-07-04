You are a data scientist working on an automated regression testing pipeline for a sensor calibration model. We have updated our modeling approach and need to ensure the new fits match our reference historical parameters within an acceptable tolerance.

Your task has three phases:
1. Environment Setup: Create a Python virtual environment at `/home/user/venv` and install the necessary packages for nonlinear equation solving and data arrays (e.g., `scipy`, `numpy`).
2. Fitter Implementation: Write a Python script `/home/user/fitter.py` that reads a data file containing comma-separated `t,y` values (with a header) and fits the nonlinear exponential decay model: 
   $y(t) = A \cdot \exp(-B \cdot t) + C$
   The script should take the file path as an argument and print the fitted parameters `A`, `B`, and `C` (in that order, space-separated).
3. Regression Tester: Write a Bash script `/home/user/run_tests.sh` that iterates over all `.txt` files in `/home/user/data/`. For each file, it should:
   - Run `fitter.py` using the virtual environment's Python.
   - Look up the reference parameters for that sensor in `/home/user/reference.csv` (format: `sensor_name,A_ref,B_ref,C_ref`). Note: the sensor name is the filename without the `.txt` extension.
   - Compare the fitted `A`, `B`, and `C` to the reference values.
   - If the absolute difference for **every** parameter is strictly less than `0.05`, the test passes. Otherwise, it fails.
   - Append the result to `/home/user/regression_report.log` in the exact format: `[sensor_name]: [PASS|FAIL]` (e.g., `sensor_1: PASS`).

Ensure your Bash script is executable and run it to generate the final `regression_report.log`.

The `/home/user/data/` directory and `/home/user/reference.csv` have already been provided to you. Sort the final output in `regression_report.log` alphabetically by sensor name.