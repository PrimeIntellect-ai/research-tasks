You are tasked with fixing a broken MCMC (Markov Chain Monte Carlo) automated validation pipeline for a data science team. The team is running Bayesian matrix factorization models, but due to near-singular inputs, many of the sampled chains fail to converge and get stuck in local optima.

We have a set of MCMC trace files. We need a filter that automatically accepts converged (good) traces and rejects unconverged (degenerate) traces based on the standard Gelman-Rubin diagnostic ($\hat{R}$).

However, the specific strictness threshold for $\hat{R}$ was handed down by the senior statistician in a screenshot of a presentation, located at `/app/mcmc_spec.png`.

Your objectives:
1. Extract the maximum allowed $\hat{R}$ threshold from the image `/app/mcmc_spec.png` (using standard OCR tools like `tesseract`, which is preinstalled).
2. Create a Bash script at `/home/user/validate_trace.sh` that takes a single argument: the path to an MCMC trace CSV file.
3. The script must compute the Gelman-Rubin $\hat{R}$ statistic for the `value` column across the chains.
4. The script must exit with code `0` (accept) if the calculated $\hat{R}$ is strictly less than or equal to the threshold found in the image.
5. The script must exit with code `1` (reject) if the calculated $\hat{R}$ is greater than the threshold, or if the variance is near-singular (0 variance).

**Data Format:**
Each CSV trace file has a header and three columns: `chain,step,value`. There are exactly 2 chains (chain `1` and chain `2`), each with the same number of steps.
You may use Python (via `python3`), `awk`, or any other standard Linux tool inside your Bash script to perform the calculations.

To test your script, you can use the sample corpora located in:
- `/app/traces/clean/` (all these traces have good mixing and should be accepted)
- `/app/traces/evil/` (these traces have bad mixing, stuck chains, or near-singular behavior and should be rejected)

Ensure `/home/user/validate_trace.sh` is executable.