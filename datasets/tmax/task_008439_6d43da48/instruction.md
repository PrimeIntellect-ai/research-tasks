You are a data scientist optimizing a Gaussian model to fit a set of observed spectral peaks. You have been provided with a model evaluation script, `/home/user/evaluate_fit.py`, which calculates the Mean Squared Error (MSE) for a given set of signal parameters. 

The evaluation script takes two positional arguments:
1. `center_freq` (float)
2. `bandwidth` (float)

It prints the resulting MSE to standard output. Because the full dataset is large, evaluating a single set of parameters has a small delay. 

Your task is to write a Bash script at `/home/user/run_optimization.sh` that performs a parallel grid search to find the optimal parameters that minimize the MSE. 

Requirements:
1. Search `center_freq` from `10.0` to `12.5` (inclusive) with a step size of `0.1`.
2. Search `bandwidth` from `1.5` to `2.5` (inclusive) with a step size of `0.1`.
3. You must use Bash to generate the multi-dimensional parameter grid.
4. You must evaluate the grid in parallel (e.g., using `xargs -P`, `parallel`, or background jobs) to ensure the optimization finishes quickly.
5. After evaluating all combinations, your script must identify the parameter pair with the absolute lowest MSE.
6. The script must write exactly one line to `/home/user/best_fit.txt` containing the best parameters and their MSE in the following comma-separated format: `center_freq,bandwidth,mse` (e.g., `10.5,2.1,0.4567`).

Ensure your script is executable (`chmod +x /home/user/run_optimization.sh`) and run it so that `/home/user/best_fit.txt` is generated.