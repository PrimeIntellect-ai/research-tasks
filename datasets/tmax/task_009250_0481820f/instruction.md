As a machine learning engineer, you are preparing a synthetic dataset to train a neural network that predicts aerodynamic drag coefficients from observed kinematics. Your current pipeline requires a Bash script to generate the target labels by simulating the physical system.

You need to write a Bash script at `/home/user/prepare_data.sh` that processes an input CSV and outputs a training data CSV.

**Physical System:**
An object falls under gravity with aerodynamic drag. The velocity $v(t)$ follows the Ordinary Differential Equation (ODE):
$dv/dt = 9.8 - k \cdot v^2$
where $k$ is the unknown drag coefficient. 
Initial conditions: at $t=0$, $v = v_0$.

**Requirements:**
1. Read `/home/user/input_data.csv` which has the header `sim_id,v0,target_v10` and comma-separated rows. `v0` is the initial velocity, and `target_v10` is the observed velocity at $t=10$ seconds.
2. For each row, numerically integrate the ODE using the **Euler method** from $t=0$ to $t=10$ with a time step of $dt = 0.1$ (exactly 100 steps).
3. Implement an optimization routine (e.g., binary search or grid search) to find the drag coefficient $k$ (restricted to the range $0.00 \le k \le 1.00$, rounded to exactly 2 decimal places) that minimizes the absolute difference between the simulated velocity at $t=10$ and the `target_v10`.
4. The output must be saved to `/home/user/training_data.csv`.
5. `/home/user/training_data.csv` must contain a header `sim_id,optimal_k` and the corresponding comma-separated values for each simulation.
6. Your script `/home/user/prepare_data.sh` must be executable and perform the entire process using Bash and standard Linux utilities (like `awk` or `bc`). Do not use Python, R, or other higher-level scripting languages for the core logic.

Run your script to generate `/home/user/training_data.csv` before finishing the task.