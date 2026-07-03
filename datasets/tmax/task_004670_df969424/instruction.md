You are helping a machine learning engineer prepare training data for a Physics-Informed Neural Network (PINN). The engineer is trying to generate a dataset by simulating the Van der Pol oscillator (a stiff Ordinary Differential Equation), but the numerical integrator diverges and produces useless data (NaNs and Infinities) due to poor step-size adaptation and an inappropriate integration scheme for stiff problems.

Your workspace is in `/home/user/ml_data/`.

Here is what you need to do:
1. **Compile the Statistics Tool:** In `/home/user/ml_data/stats_tool/`, there is the source code for a C program (`stats.c`) and a `Makefile`. This tool reads a CSV file and calculates the maximum absolute value of the first column. Compile this software from source using the provided `Makefile` to produce the `calc_stats` executable.
2. **Fix the Data Generator:** The script `/home/user/ml_data/generate.py` currently uses a naive fixed-step Runge-Kutta 4 (RK4) implementation. Because the Van der Pol equation with $\mu=50$ is a stiff system, the manual RK4 integrator diverges violently at the given time step.
   - Modify `/home/user/ml_data/generate.py` to replace the manual RK4 loop with `scipy.integrate.solve_ivp`.
   - You must use a stiff solver method (e.g., `BDF` or `Radau`).
   - The initial conditions ($y_1=2.0, y_2=0.0$), the system parameters ($\mu=50$), and the exact evaluation times (`t_eval = np.linspace(0, 100, 1000)`) must remain exactly the same.
   - The output must still be saved to `/home/user/ml_data/dataset.csv` with the columns `y1` and `y2`.
3. **Generate and Verify:** 
   - Run your fixed `generate.py` script to generate a stable, accurate `dataset.csv`.
   - Run the compiled `calc_stats` tool on the newly generated `dataset.csv` and redirect its standard output to `/home/user/ml_data/stability_report.txt`.

The automated test will verify that `dataset.csv` is correctly formatted without NaNs, and that `stability_report.txt` contains the correct numerical maximum amplitude bounded by the stable limit cycle of the system.