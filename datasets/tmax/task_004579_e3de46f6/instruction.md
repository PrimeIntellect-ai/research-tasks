You are a Machine Learning Engineer preparing a dataset for training a neural ODE model. You need to simulate the trajectories of the Van der Pol oscillator, a system that frequently becomes stiff and causes naive numerical integrators to diverge due to incorrect step-size adaptation. The previous custom integrator has failed, and you must build a robust data generation pipeline.

Your tasks are as follows:

1. **Environment Setup**:
   - Create a Python virtual environment at `/home/user/venv`.
   - Install `numpy`, `scipy`, and `pandas` into this virtual environment.

2. **Algorithm Implementation**:
   - The Van der Pol oscillator is defined by the system of ODEs:
     `dy1/dt = y2`
     `dy2/dt = mu * (1 - y1^2) * y2 - y1`
   - Use `mu = 3.0`.
   - Write a script at `/home/user/generate_data.py` that uses `scipy.integrate.solve_ivp` to integrate this system from `t = 0` to `t = 10.0`.
   - You must use a stiff solver (like `BDF` or `Radau`) with `rtol=1e-6` and `atol=1e-8` to ensure the integrator does not diverge.

3. **Reference Comparison (Validation)**:
   - There is a reference dataset of 5 verified trajectories at `/home/user/reference.csv` (columns: `y1_initial`, `y2_initial`, `y1_final`, `y2_final`).
   - Your script must first read this file, simulate the system for the given `y1_initial` and `y2_initial` values, and verify that your computed final states at `t = 10.0` match the reference `y1_final` and `y2_final` values with an absolute error of less than `1e-3`. If the validation fails, your script should raise an error.

4. **Monte Carlo Data Generation**:
   - Once validated, your script should perform a Monte Carlo simulation to generate the training data.
   - Set the random seed using `numpy.random.seed(42)`.
   - Uniformly sample 100 initial conditions for both `y1` and `y2` in the range `[-3.0, 3.0]`.
   - Integrate each initial condition from `t = 0` to `t = 10.0`.
   - Save the results to `/home/user/training_data.csv` with exactly these columns: `y1_initial`, `y2_initial`, `y1_final`, `y2_final`.

5. **Completion**:
   - Run your script using the virtual environment.
   - Upon successful generation of the verified dataset, write the text `DATASET_GENERATED` to `/home/user/success.log`.