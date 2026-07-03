You are acting as a performance engineer investigating why a linear system solver fails on certain ill-conditioned inputs. Your team uses matrix factorization to solve $Ax = b$, but it behaves erratically when $A$ is nearly singular. To profile this, you need to study the error growth using a classic ill-conditioned matrix: the Hilbert matrix.

Your objective is to write a Python script that analyzes the numerical stability and error of solving $Hx = b$ for various matrix sizes, and visualizes the results.

Please perform the following steps:
1. Write a Python script at `/home/user/profile_hilbert.py`. You may need to install `numpy` and `matplotlib` first.
2. For each matrix size $N \in [2, 4, 6, 8, 10, 12]$:
   a. Generate an $N \times N$ Hilbert matrix $H$, where $H_{i,j} = \frac{1}{i + j + 1}$ for $i, j \in \{0, 1, \dots, N-1\}$.
   b. Define the analytical true solution $x_{true}$ as a vector of $N$ ones: $x_{true} = [1, 1, \dots, 1]^T$.
   c. Compute the right-hand side vector $b = H x_{true}$.
   d. Compute the 2-norm condition number of $H$ (using `numpy.linalg.cond`).
   e. Solve the system $Hx = b$ for $x$ using `numpy.linalg.solve`.
   f. Calculate the relative $L_2$ error of the solution: $\frac{||x - x_{true}||_2}{||x_{true}||_2}$.
3. Save the profiling data to `/home/user/hilbert_data.json`. The JSON file should be a dictionary where the keys are the string representation of $N$ (e.g., `"2"`, `"4"`, etc.), and the values are objects with keys `"condition_number"` and `"relative_error"`. Both values should be standard floats.
4. Generate a plot at `/home/user/hilbert_plot.png` with two side-by-side subplots (1 row, 2 columns):
   - Left subplot: $N$ (x-axis) vs. Condition Number (y-axis) on a logarithmic y-scale.
   - Right subplot: $N$ (x-axis) vs. Relative Error (y-axis) on a logarithmic y-scale.
5. Run your script to generate both the JSON file and the plot.

Ensure the final JSON is accurately computed as an automated test will check the values within a small floating-point tolerance.