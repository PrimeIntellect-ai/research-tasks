You are a Machine Learning Engineer preparing synthetic training data for a neural network. The data generation process simulates a physical system governed by a nonlinear ordinary differential equation (ODE) - specifically, the Van der Pol oscillator. 

We have started writing a custom Rust-based numerical integrator with adaptive step-size control in `/home/user/data_gen`. Unfortunately, the solver currently diverges because the step-size adaptation logic is fundamentally flawed. 

Your task is to fix the integrator, implement a Monte Carlo sampling loop, and orchestrate the data preparation using a Jupyter Notebook.

1. **Fix the Integrator**: 
   Inspect `/home/user/data_gen/src/solver.rs`. The solver uses a custom Runge-Kutta-like method with adaptive step sizing. The step size `dt` update formula is inverted. Fix it so that the new step size is computed as `dt * (tol / error).powf(0.5)` (clamped between `1e-5` and `0.1`).

2. **Implement the Monte Carlo Simulation**:
   Modify `/home/user/data_gen/src/main.rs` to run exactly 100 independent simulations. 
   For each simulation (where `sim_id` goes from `0` to `99` inclusive), set the initial conditions to:
   - `y1 = 1.0 + (sim_id as f64) * 0.01`
   - `y2 = 0.0`
   - `t_end = 10.0`
   - `tol = 1e-4`
   The Rust program must output a CSV file at `/home/user/raw_data.csv` containing the final states at `t = 10.0`. The CSV must have exactly three columns with the header: `sim_id,y1,y2`.

3. **Notebook-based Workflow Orchestration & Data Reshaping**:
   Create a Jupyter Notebook at `/home/user/workflow.ipynb` (using Python 3) that orchestrates the entire pipeline. When executed, the notebook must:
   - Run a shell command to compile the Rust project (`cargo build --release` inside `/home/user/data_gen`).
   - Run a shell command to execute the compiled binary (`cargo run --release` or directly call the binary), generating `/home/user/raw_data.csv`.
   - Load the CSV using `pandas`.
   - Reshape the data into a JSON array of objects. Each object should represent one simulation with exactly these keys: `"id"` (integer `sim_id`), `"final_y1"` (float `y1`), and `"final_y2"` (float `y2`).
   - Save the resulting JSON structure to `/home/user/ml_training.json`.

4. **Execution**:
   Once your notebook is ready, execute it headlessly from the terminal using:
   `jupyter nbconvert --execute --to notebook --inplace /home/user/workflow.ipynb`

You have successfully completed the task when the bug is fixed, the notebook runs without errors, and `/home/user/ml_training.json` is accurately generated with all 100 entries.