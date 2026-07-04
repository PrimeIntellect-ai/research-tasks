I am a data scientist trying to fit a simple exponential decay model ($y' = -ky$) to some experimental data stored in `/home/user/data.csv`. I wrote a C program, `/home/user/fit_model.c`, that uses OpenMP to parallelize the Mean Squared Error (MSE) calculation and uses gradient descent to find the optimal parameter `k`. 

However, the numerical integrator inside the objective function is diverging due to a wrong step-size adaptation. My initial guess for `k` is somewhat stiff, and the Euler method step size (`dt = 1.0`) is too large, throwing the gradient descent into `NaN` values.

Please do the following:
1. Fix the step size in `/home/user/fit_model.c`: Inside the `simulate(double k, double t_end)` function, change the default integration step size `dt` to exactly `0.01`. Make sure `dt` is also correctly reset to `0.01` (not `1.0`) inside the `while` loop after adjusting for the final fractional step.
2. Compile the fixed C program using standard tools: output the binary to `/home/user/fit_model`. Remember to link the math library and enable OpenMP.
3. Run the compiled binary. It will automatically write the optimized parameter `k` to `/home/user/optimal_k.txt`.
4. Create a GNUplot script at `/home/user/plot.gp` that generates a PNG image at `/home/user/plot.png`. The plot should plot the experimental data from `data.csv` (Time on X axis, Value on Y axis) using points. You don't need to run gnuplot, just create the valid `.gp` script that sets the terminal to `png`, sets the output file, and plots the CSV data correctly.

Ensure your compiled program runs successfully and the output files exist.