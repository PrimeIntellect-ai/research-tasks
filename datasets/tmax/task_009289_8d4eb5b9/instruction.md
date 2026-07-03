You are a performance engineer tasked with optimizing and fixing a custom numerical integrator written entirely in Bash and `awk`. This tool is used to model sequence degradation rates in a biological simulation system.

The project is located at `/home/user/sim_project`.

### 1. Fix the Integrator (`integrator.sh`)
The file `integrator.sh` uses the Euler method to simulate the differential equation `dy/dt = -k * y`, starting from `y=100` at `t=0` to `t=10`. It takes `k` as the first positional argument. 
Currently, the step size `dt` is fixed at `2.0`, causing the simulation to diverge and oscillate wildly for large `k` values due to wrong step-size adaptation.
**Your task:** Modify `/home/user/sim_project/integrator.sh` to use an adaptive step size. Specifically, calculate the step size as `dt = 0.5 / k` (using `awk` for floating point math). Ensure the loop advances `t` by `dt` and `y` by `-k * y * dt` until `t >= 10`. The script must output ONLY the final value of `y` rounded to 4 decimal places.

### 2. Parallel Processing (`run_all.sh`)
You are provided with `/home/user/sim_project/k_values.txt`, which contains 100 different decay constants (`k`).
Create a script `/home/user/sim_project/run_all.sh` that reads these `k` values and runs `integrator.sh` for each of them. 
**Constraint:** You must parallelize this execution to run exactly 4 jobs concurrently using standard bash tools (e.g., `xargs -P`).
Save the output (just the final `y` values, one per line) to `/home/user/sim_project/results.txt`.

### 3. Bootstrap Confidence Intervals (`bootstrap.sh`)
Create a script `/home/user/sim_project/bootstrap.sh` that computes a 95% bootstrap confidence interval for the *mean* of the `y` values in `results.txt`.
- Perform exactly 1000 resampling iterations (with replacement) of the 100 values.
- Calculate the mean for each resampled dataset.
- Sort the 1000 means and extract the 2.5th percentile (25th value) and 97.5th percentile (975th value).
- Save the result to `/home/user/sim_project/ci.log` in the exact format: `lower_bound,upper_bound` (rounded to 4 decimal places).

### 4. Regression Test (`test.sh`)
Create a regression test script `/home/user/sim_project/test.sh` that checks if the generated `ci.log` contains two values that are both strictly between `0.0000` and `5.0000`. If they are, exit with code 0; otherwise, exit with code 1.

Ensure all scripts are executable and run correctly using bash-only commands and standard coreutils (`awk`, `shuf`, `sort`, `xargs`, etc.).