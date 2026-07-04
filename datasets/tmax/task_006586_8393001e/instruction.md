You are a data scientist working on an edge-computing project where a legacy graph diffusion model is implemented entirely in Bash. 

You have been provided with a model simulator located at `/home/user/simulate.sh`. This script takes a single numeric parameter, the diffusion coefficient `k`. When executed, it prints the simulation steps, the final state of several nodes, and the final `System Energy`.

Your task is to fit this model to a known target and perform a regression test against a golden baseline:
1. **Model Fitting:** The true diffusion coefficient `k` lies somewhere in the range `0.00` to `5.00` (inclusive). Using Bash command-line tools, find the value of `k` (formatted to exactly 2 decimal places, e.g., `1.23`) that produces a `System Energy` exactly equal to `50.00`. 
2. **Save Parameter:** Save this optimal value of `k` into `/home/user/optimal_k.txt`.
3. **Generate Output:** Run the simulation one last time with your optimal `k` and save the complete standard output to `/home/user/best_model.txt`.
4. **Regression Testing:** A verified baseline for this target energy state exists at `/home/user/golden.txt`. Perform a regression test by comparing your `/home/user/best_model.txt` against `/home/user/golden.txt` using the `diff -u` command. Save the output of this diff to `/home/user/regression.patch`.

Complete this using only standard Bash utilities (`seq`, `awk`, `bc`, `grep`, `while`, etc.).