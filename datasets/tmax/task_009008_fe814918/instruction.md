You are a machine learning engineer tasked with generating high-quality synthetic training data based on a chaotic dynamical system (the Lorenz attractor). Before training, you must verify the numerical stability and convergence of the ODE solvers used to generate the data.

Please complete the following steps in the `/home/user` directory:

1. **Scientific Environment Management**:
   Create a Python virtual environment at `/home/user/env` and install `numpy`, `pandas`, and `matplotlib`. All your scripts must be run using this virtual environment's Python.

2. **Simulation & Numerical Implementation**:
   Write a Python script `/home/user/generate_data.py` that implements two numerical integration methods from scratch (do not use `scipy.integrate`):
   - Forward Euler method
   - 4th-order Runge-Kutta (RK4) method

   Use these methods to solve the Lorenz system:
   `dx/dt = sigma * (y - x)`
   `dy/dt = x * (rho - z) - y`
   `dz/dt = x * y - beta * z`

   Parameters: `sigma = 10.0`, `rho = 28.0`, `beta = 2.6666666666666665` (i.e., 8/3).
   Initial conditions at `t = 0.0`: `x = 1.0`, `y = 1.0`, `z = 1.0`.
   Integration time: `t = 0.0` to `t = 2.0`.

3. **Convergence and Numerical Stability Testing**:
   In your script, perform the following integrations:
   - Run RK4 with `dt = 0.01` (200 steps)
   - Run RK4 with `dt = 0.001` (2000 steps)
   - Run Forward Euler with `dt = 0.01` (200 steps)

   Calculate the final state `(x, y, z)` at `t = 2.0` for each of these three runs. 
   Save these final states to `/home/user/results.json` in the following exact format (round the coordinate values to 5 decimal places):
   ```json
   {
     "rk4_0.01": [x, y, z],
     "rk4_0.001": [x, y, z],
     "euler_0.01": [x, y, z]
   }
   ```

4. **Data Preparation**:
   Save the full trajectory of the most accurate run (RK4 with `dt = 0.001`) to `/home/user/training_data.csv`. The CSV should have columns exactly named `t,x,y,z` and include the initial condition as the first row.

5. **Experimental Data Visualization**:
   Generate a 3D line plot of the RK4 `dt = 0.001` trajectory. Save the plot as `/home/user/attractor.png`.

Run your script to produce all required outputs.