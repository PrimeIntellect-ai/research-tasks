You are acting as a data scientist evaluating a numerical integrator. We have a legacy simulation script, `/home/user/sim_euler.sh`, which integrates a simple system but is highly sensitive to the chosen step size (`dt`). Currently, it produces inaccurate results unless the step size is sufficiently refined.

Your task is to orchestrate a convergence testing workflow entirely in Bash. You need to write an orchestration script `/home/user/orchestrate.sh` that accomplishes the following:

1. **Mesh Refinement & Convergence Testing:** 
   - Start with an initial step size `dt=0.5`.
   - Run `/home/user/sim_euler.sh` with the current `dt` as its only argument.
   - The script outputs verbose logs. Parse the standard output to extract the numeric value of `y` from the line that reads: `Final Output: t=..., y=...`.
   - Halve the step size (`dt = dt / 2`) and repeat the simulation.
   - Calculate the absolute difference between the `y` value of the current run and the previous run.
   - Stop the loop *immediately* when this absolute difference is strictly less than `0.05` (i.e., `diff < 0.05`). Keep the results of the run that triggered the stopping condition. Use `bc -l` for all floating-point math.

2. **Observational Data Reshaping:**
   - Log the results of every executed run (including the final one that met the stopping criterion) into a CSV file named `/home/user/results.csv`.
   - The CSV must have the exact header: `iteration,dt,final_y`.
   - `iteration` should start at 1.

3. **Notebook-based Workflow Orchestration:**
   - Automatically generate a Markdown summary report of the experiment at `/home/user/report.md`.
   - The Markdown file must contain exactly the following line (replace X, Y, and Z with the correct values from the final run):
     `Convergence achieved at iteration X with step size Y and final value Z.`

Make sure your `/home/user/orchestrate.sh` script is executable and performs all of these actions when run. Do not use Python, Perl, or any other scripting language besides Bash, `awk`, `sed`, `grep`, `bc`, and standard coreutils.