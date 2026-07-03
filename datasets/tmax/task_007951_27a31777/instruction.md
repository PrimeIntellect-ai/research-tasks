You are an AI assistant helping a data scientist orchestrate a workflow to find a stable parameter for a mathematical model. 

The file `/home/user/simulate.ipynb` is a Jupyter notebook that simulates a chemical kinetics system using Ordinary Differential Equations (ODEs) and performs Singular Value Decomposition (SVD) on the resulting state matrix. However, for many parameter values, the resulting matrix is near-singular, causing the decomposition to fail with an exception.

Your task is to write a Bash script `/home/user/run_search.sh` that orchestrates an automated search for the first parameter `k` that yields a stable matrix.

The notebook accepts a parameter named `k` (a float). 
Your bash script must:
1. Iterate over potential `k` values starting from `0.01` up to `0.50` in increments of `0.01` (e.g., 0.01, 0.02, 0.03...).
2. For each value, use `papermill` to execute `/home/user/simulate.ipynb`, passing the current `k` value. Save the output notebook to `/home/user/output.ipynb`.
3. If `papermill` succeeds (exit code 0), write the successful `k` value (formatted to two decimal places, e.g., `0.15`) to `/home/user/stable_k.txt` and immediately exit the loop/script.
4. If `papermill` fails, suppress the error output and continue to the next `k`.

Make sure your script is executable and run it so that `/home/user/stable_k.txt` is generated with the correct ground-truth value.