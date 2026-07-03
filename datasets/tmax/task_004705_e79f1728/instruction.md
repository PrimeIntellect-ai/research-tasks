You are an AI assistant helping a Machine Learning Engineer prepare synthetic training data for a physics-informed neural network. The neural network needs to learn the manifold of a complex scalar field defined by a nonlinear implicit equation.

Your task is to write and execute a Python script that generates this dataset, normalizes it, and visualizes the manifold. 

Follow these exact steps:
1. **Grid Generation (Array Manipulation):** Generate a uniform 2D meshgrid of `x` and `y` coordinates. Both `x` and `y` should be linearly spaced from `-5.0` to `5.0` (inclusive) with exactly `25` points each. This will create a total of 625 `(x, y)` pairs.
2. **Nonlinear Equation Solving:** For every `(x, y)` pair in the grid, solve for the real value `z` that satisfies the following nonlinear equation:
   `z^3 + sin(z) - (x * y) = 0`
   *(Hint: You can use `scipy.optimize.fsolve` with an initial guess of 0.0 for each point).*
3. **Data Formatting:** Combine your results into a single, two-dimensional NumPy array of shape `(625, 3)`, where each row contains `[x, y, z]`. 
4. **Data Normalization:** Create a new normalized version of this array using standard z-score normalization. Calculate the mean and standard deviation for each column (X, Y, and Z) independently, and transform the data so each column has a mean of 0.0 and a standard deviation of 1.0 (using the population standard deviation, i.e., `ddof=0`).
5. **Output Data:** Save the *normalized* array to disk as a binary NumPy file at `/home/user/normalized_dataset.npy`.
6. **Data Visualization:** Using `matplotlib`, create a 3D scatter plot of the *unnormalized* `(x, y, z)` points. Label the axes 'X', 'Y', and 'Z' respectively. Save this figure as an image file at `/home/user/dataset_visualization.png`.
7. **Logging:** Find the maximum unnormalized `z` value across all calculated points. Create a text file at `/home/user/dataset_stats.txt` and write this single line to it, rounding the value to exactly 4 decimal places:
   `Max Z: <value>`

Ensure all files are saved in `/home/user/`. Use Python to accomplish all of these requirements.