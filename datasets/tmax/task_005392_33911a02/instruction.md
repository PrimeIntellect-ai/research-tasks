You are a performance engineer tasked with profiling a numerical integration workflow that sometimes diverges due to faulty step-size adaptation. The entire workflow must be orchestrated using standard Linux shell tools and Bash.

In `/home/user/sim_project`, you will find:
1. `experiment_workflow.ipynb`: A Jupyter notebook file (JSON format) containing the simulation parameters.
2. `integrator.sh`: A Bash script that performs a mock numerical integration using `awk`. It takes one argument: the `initial_step_size`.

Your task involves several steps:

**Step 1: Orchestration & Extraction**
Parse `experiment_workflow.ipynb` using `jq`. Find the code cell that assigns a list of floating-point values to the variable `STEP_SIZES`. Extract these values.

**Step 2: Profiling & Filtering**
Write a Bash script `profile_runs.sh` that iterates over the extracted step sizes. For each step size, time the execution of `./integrator.sh <step_size>` in milliseconds. 
Some step sizes cause the numerical integrator to diverge, resulting in excessively long runtimes (e.g., > 200 ms) and an exit code of 1 or a "DIVERGENCE" output.
Record the execution times (in milliseconds) of ONLY the *successful, stable* runs (exit code 0) into a file named `stable_times.txt`.

**Step 3: Statistical Analysis (Bootstrap Confidence Intervals)**
Using only Bash, `awk`, and coreutils, write a script `bootstrap_ci.sh` that reads `stable_times.txt`.
Implement a bootstrap resampling algorithm (1,000 resamples) to estimate the 95% confidence interval of the **mean** execution time of the stable runs.
- For each of the 1,000 resamples, draw N times with replacement from `stable_times.txt` (where N is the number of stable runs).
- Calculate the mean of each resample.
- Sort the 1,000 means and extract the 2.5th percentile (25th value) and 97.5th percentile (975th value).

Save the final output to `/home/user/sim_project/ci_results.txt` in exactly this format:
```
Lower CI: <value>
Upper CI: <value>
```
(Round the values to 2 decimal places).

Do not install any external packages (like Python, R, or specialized profiling tools). Use `bash`, `awk`, `jq`, `sed`, `grep`, and standard coreutils.