You are a performance engineer working on a molecular dynamics simulation engine written in Rust. The engine models polymer chains as a graph of masses and springs. Recently, a critical bug was introduced in the adaptive ODE integrator (Runge-Kutta) which causes the simulation to diverge rapidly or produce NaN values due to incorrect step-size adaptation.

Your tasks are:

1. **Fix the Integrator Bug:**
   The Rust project is located at `/home/user/sim_engine`. The bug is in `src/integrator.rs`. The step-size adaptation logic is incorrectly scaling the time step `dt`. When the estimated error exceeds the tolerance, it is currently *increasing* the step size instead of decreasing it. Fix the mathematical logic so that the simulation converges.

2. **Run the Simulation:**
   Compile and run the fixed Rust simulation. The program will output CSV data to standard output. Redirect this output to `/home/user/sim_output.csv`. The output format will be `time,node1_x,node1_v`.

3. **Compare Against Reference Dataset:**
   A known-good trajectory is located at `/home/user/reference_data.csv`. Write a short script (Python or Bash/Awk) to calculate the Mean Squared Error (MSE) of `node1_x` between your `sim_output.csv` and the `reference_data.csv` at exactly matching time steps. Write the result to `/home/user/evaluation.log` in the exact format: `MSE: <value>` (e.g., `MSE: 0.000123`).

4. **Visualize the Experimental Data:**
   Create a Python script at `/home/user/plot_data.py` that reads both `sim_output.csv` and `reference_data.csv`, and generates an SVG plot comparing the `node1_x` trajectories. Save the plot as `/home/user/trajectory_plot.svg`.

Ensure all file paths and names match exactly. The system has `python3`, `matplotlib`, `pandas`, and standard Rust tools (`cargo`, `rustc`) installed.