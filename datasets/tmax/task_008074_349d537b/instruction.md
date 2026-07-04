You are a Machine Learning Engineer preparing synthetic training data for a Physics-Informed Neural Network (PINN). The network models a damped harmonic oscillator, but your Python environment is currently broken. You need to build a reproducible data generation pipeline using only Bash and standard UNIX utilities (like `awk`).

Your task is to write a numerical integration pipeline in Bash that simulates the system, and then orchestrates the generation of a combined training dataset.

**System Equations (Damped Harmonic Oscillator):**
- $\frac{dx}{dt} = v$
- $\frac{dv}{dt} = -k \cdot x - c \cdot v$

**System Parameters:**
- Spring constant ($k$) = 1.5
- Damping coefficient ($c$) = 0.2
- Time step ($\Delta t$) = 0.1
- Number of steps = 50 (so $t$ goes from 0.0 to 5.0 inclusive, yielding 51 rows per run)

**Step 1: The Integration Script**
Create a script at `/home/user/pipeline/generate.sh` that takes a single positional argument: the initial position $x_0$. 
The script should use `awk` to perform numerical integration using the **Forward Euler** method.
- Initial conditions at $t=0$: $x = x_0$, $v = 0.0$.
- Update rules for step $i+1$:
  $x_{i+1} = x_i + v_i \cdot \Delta t$
  $v_{i+1} = v_i + (-k \cdot x_i - c \cdot v_i) \cdot \Delta t$
  *(Note: calculate both new values using the previous step's values, don't use $x_{i+1}$ to find $v_{i+1}$)*
- The script should output CSV formatted data to standard output with the header `t,x,v`.
- Format numbers to 4 decimal places (e.g., using `printf "%.4f,%.4f,%.4f\n"`).

**Step 2: The Orchestration Script**
Create a pipeline script at `/home/user/pipeline/run_pipeline.sh`.
- This script should loop over the following initial conditions for $x_0$: `1.0`, `2.0`, and `3.0`.
- For each $x_0$, run `generate.sh`.
- Combine the results into a single dataset file at `/home/user/pipeline/training_data.csv`.
- The final `training_data.csv` must have the header `t,x,v,x0` (where `x0` is the initial condition used for that run).
- Do not duplicate the `t,x,v` header from `generate.sh` in the final rows; the final CSV should have exactly 1 header row, followed by 153 data rows.
- Ensure the file is sorted by $x_0$ (1.0, then 2.0, then 3.0), and then by time $t$ within each $x_0$ block.

Make sure both scripts are executable. Once you are done, run `/home/user/pipeline/run_pipeline.sh` so that `/home/user/pipeline/training_data.csv` is generated.