You are a machine learning engineer preparing physical simulation data to train a Physics-Informed Neural Network (PINN). You need to generate a trajectory for a damped pendulum, compute its numerical derivatives to use as training targets, and perform a regression test against an existing golden dataset.

A colleague has provided the core numerical integration routine in C, located at `/home/user/src/integrator.c`. The golden dataset from a previous validated version of the software is at `/home/user/data/golden_trajectory.csv`.

Your task is to:
1. Compile the C source code `/home/user/src/integrator.c` into a shared library named `/home/user/src/libintegrator.so`.
2. Write a Python script `/home/user/prepare_data.py` that interfaces with this shared library (e.g., using `ctypes`).
3. Using the compiled library, integrate the system for `1000` steps with a timestep of `dt = 0.05`. The initial conditions are `x0 = 3.0` and `v0 = 0.0`. The C function signature is:
   `void integrate(double x0, double v0, double dt, int steps, double* out_x, double* out_v)`
4. The neural network needs the acceleration `a` as a training target. Since the C code only outputs position (`x`) and velocity (`v`), numerically differentiate the resulting velocity array in Python to compute the acceleration `a`. Use `numpy.gradient` with `edge_order=2` and the correct `dt`.
5. Perform a regression test by comparing your generated `x`, `v`, and `a` arrays against the columns in `/home/user/data/golden_trajectory.csv`. Calculate the Mean Squared Error (MSE) for each of the three variables.
6. Save the regression test results in a JSON file at `/home/user/regression_metrics.json`. The file must have exactly this structure:
   ```json
   {
     "mse_x": <float>,
     "mse_v": <float>,
     "mse_a": <float>
   }
   ```

Ensure your Python script runs without errors and produces the correct JSON output.