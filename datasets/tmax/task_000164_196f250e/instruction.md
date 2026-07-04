You are a performance engineer tasked with profiling and fixing a multi-language optimization pipeline. The pipeline currently fails on extreme initial conditions due to numerical instability. 

Your workspace is located at `/home/user/sim_pipeline`. Inside it, you have two files:
1. `generate_data.c`: A C program that generates a reference dataset of initial starting conditions for the optimization.
2. `optimizer.py`: A Python script containing an objective function and an optimization routine (using `scipy.optimize.minimize` with the Nelder-Mead method).

Currently, `optimizer.py` uses a naive implementation of the objective function: 
$$f(x,y) = \log(e^{50(x - 3.14)^2} + e^{50(y + 2.71)^2})$$
When evaluated far from the minimum $(3.14, -2.71)$, the exponential terms overflow, resulting in `inf` and causing the optimizer to fail (returning `NaN` or incorrect results).

Your tasks:
1. **Compile and run the data generator**: Compile `generate_data.c` into an executable named `generate_data`. Run it and redirect its standard output to `/home/user/sim_pipeline/dataset.txt`. This file will contain space-separated pairs of initial coordinates `x0 y0`.
2. **Fix numerical instability**: Edit `optimizer.py` so that the objective function computes the exact same mathematical value but is numerically stable (e.g., using the log-sum-exp trick or `numpy.logaddexp`). Do not alter the underlying mathematical function, the global minimum, or the optimization method (Nelder-Mead).
3. **Make the script CLI-callable**: Modify `optimizer.py` to accept two command-line arguments representing the initial guess `x0` and `y0`. After optimization, the script must print *only* the final optimized `x` and `y` coordinates to standard output, separated by a space (e.g., `3.140023 -2.709981`).
4. **Create a reproducible evaluation pipeline**: Write a bash script at `/home/user/sim_pipeline/evaluate.sh` that:
   - Reads `dataset.txt` line by line.
   - For each `x0 y0` pair, calls your fixed `optimizer.py x0 y0`.
   - Collects the resulting optimized $(x, y)$ coordinates.
   - Computes the Mean Squared Error (MSE) across all points between the optimizer's final coordinates and the true analytical minimum $(3.14, -2.71)$. The MSE for a single point $(x, y)$ is defined as $\frac{(x - 3.14)^2 + (y - (-2.71))^2}{2}$. The overall MSE is the average of these individual point MSEs.
   - Writes the final average MSE to `/home/user/sim_pipeline/final_mse.txt` in the exact format: `MSE: <value>` (rounded to 6 decimal places).

Ensure all scripts are executable and that running `/home/user/sim_pipeline/evaluate.sh` seamlessly produces the `final_mse.txt` file.