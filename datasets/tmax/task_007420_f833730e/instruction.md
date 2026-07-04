You are a data scientist tasked with fitting a diffusion model to observed spatial data. 

You have been provided a Python script `/home/user/simulate.py` that solves an ODE for diffusion on a 1D grid and outputs a 10x10 state matrix. It accepts two parameters: `--k` (diffusion coefficient) and `--d` (decay rate). You also have a target data file `/home/user/target_data.txt` containing a 10x10 matrix of observations.

Your task is to write a Bash script named `/home/user/fit_model.sh` that performs a grid search to find the parameters that best fit the target data.

Requirements for `/home/user/fit_model.sh`:
1. Iterate over `k` from 0.1 to 0.5 in steps of 0.1 (i.e., 0.1, 0.2, 0.3, 0.4, 0.5).
2. Iterate over `d` from 0.01 to 0.05 in steps of 0.01 (i.e., 0.01, 0.02, 0.03, 0.04, 0.05).
3. For each combination, run `/home/user/simulate.py --k <k> --d <d>`. The output will be a 10x10 grid of space-separated numbers.
4. Calculate the Mean Absolute Error (MAE) between the simulation output and `/home/user/target_data.txt`. You must implement this calculation natively in Bash (using standard tools like `awk`, `paste`, `bc`, etc. - do not write an external Python script for the MAE calculation).
5. Identify the combination of `k` and `d` that produces the minimum MAE.
6. Write the best parameters to `/home/user/best_fit.txt` exactly in this format: `k=0.X, d=0.0Y`.

Ensure your Bash script is executable (`chmod +x`).