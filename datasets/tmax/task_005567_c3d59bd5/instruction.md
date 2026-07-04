You are a Machine Learning Engineer preparing training data for a Physics-Informed Neural Network (PINN) that models 1D heat diffusion. You have received raw, noisy sensor data in a JSON format. Your task is to extract the data, smooth it by fitting a known physical model, and generate a refined, uniformly spaced dataset with corresponding analytical spatial and temporal derivatives for the neural network loss function.

Here are your instructions:

1. **Read Observational Data:**
   Read the file `/home/user/sensor_data.json`. It contains a list of dictionaries with keys `"time"`, `"position"`, and `"temperature"`. The data is irregularly sampled and contains noise.

2. **Optimization (Model Fitting):**
   The underlying physical process follows the analytical form:
   `T(x, t) = A * exp(-k * t) * sin(pi * x)`
   where `x` is position, `t` is time, `A` is the initial amplitude, and `k` is the decay constant.
   Write a Python script to fit this model to the raw observational data to find the optimal parameters `A` and `k` (using optimization methods like `scipy.optimize.curve_fit`).
   Save these fitted parameters in a JSON file at `/home/user/fitted_params.json` with the format:
   `{"A": <value_of_A>, "k": <value_of_k>}` (Do not round these values in the JSON).

3. **Mesh Refinement and Differentiation:**
   Using your fitted `A` and `k`, generate a dense, uniform 2D grid (mesh) for the PINN training:
   - Time `t` must range from `0.0` to `2.0` inclusive, with exactly 50 linearly spaced points.
   - Position `x` must range from `0.0` to `1.0` inclusive, with exactly 50 linearly spaced points.
   
   For every point `(t, x)` in this mesh, calculate:
   - `T`: The temperature using the fitted model.
   - `T_t`: The first analytical derivative of T with respect to time (`dT/dt`).
   - `T_xx`: The second analytical derivative of T with respect to position (`d^2T/dx^2`).

4. **Format Output for ML Training:**
   Export the calculated data to a CSV file at `/home/user/pinn_training.csv`.
   - The CSV must have exactly these columns in this order: `t,x,T,T_t,T_xx`
   - Sort the data primarily by `t` (ascending), and secondarily by `x` (ascending).
   - Round all floating-point values in the CSV to exactly 4 decimal places.

Your final deliverables are the files `/home/user/fitted_params.json` and `/home/user/pinn_training.csv`. You may create any intermediate Python scripts you need in `/home/user/`.