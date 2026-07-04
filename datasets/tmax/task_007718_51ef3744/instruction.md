As a machine learning engineer preparing training data, you need to compute the probability density of a continuous feature using Kernel Density Estimation (KDE) to use as an auxiliary input for a new model. Since this operation will run in a high-performance data pipeline, the core estimation must be written in C.

You need to perform the following steps:

1. **Write the KDE program in C**: Create a C program at `/home/user/kde.c` that reads a list of floating-point numbers from `/home/user/features.txt` (one per line). The program should compute the Gaussian Kernel Density Estimation using a bandwidth of `h = 0.5` for query points `x` ranging from `-5.0` to `5.0` (inclusive) in increments of `0.1`.
   - The Gaussian KDE formula is $f(x) = \frac{1}{n h \sqrt{2\pi}} \sum_{i=1}^n \exp\left(-\frac{(x - x_i)^2}{2h^2}\right)$.
   - Output the results to `/home/user/density_output.txt`, with each line containing `x,density`. Use the format specifier `"%.1f,%.5f\n"` for printing.
   
2. **Visualize the distribution**: Create a Python script `/home/user/plot_kde.py` that reads `/home/user/density_output.txt` and generates a line plot of the density. Save the plot as `/home/user/density_plot.png`.

3. **Set up a regression test**: Create a Bash script `/home/user/test_kde.sh` that:
   - Compiles `kde.c` into an executable named `kde_bin` (remember to link the math library).
   - Runs `./kde_bin`.
   - Checks if the calculated density at `x = 0.0` in `density_output.txt` is exactly `0.33795` (i.e., searches for the exact string `0.0,0.33795`).
   - Exits with code `0` if the value is found, and `1` otherwise.

Ensure your scripts have the correct execute permissions where necessary.