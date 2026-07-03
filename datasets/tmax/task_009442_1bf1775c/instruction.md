You are an ML Engineer preparing synthetic 1D feature distributions for a generative neural network. You need to model the behavior of a transformed uniform random variable to create a baseline probability density function (PDF). 

Your objective is to write a C program that performs a Monte Carlo simulation, estimates the density, calculates numerical derivatives and integrals, and visualizes the result.

Perform the following steps:

1. **Monte Carlo Simulation in C**:
   Write a C program at `/home/user/generate_features.c`.
   To ensure cross-platform determinism, implement a custom Linear Congruential Generator (LCG) for your random numbers:
   - State variable: `uint32_t state = 12345;`
   - Update rule: `state = 1664525 * state + 1013904223;`
   - Uniform float in [0, 1): `float u = (float)state / 4294967296.0f;`

   Generate $N = 100,000$ samples of a variable $X \sim \text{Uniform}(0, 5)$ using `X = 5.0 * u`. 
   For each $X$, compute the transformed feature $Y = \sin(X) + \cos(2 \cdot X)$.

2. **Density Estimation**:
   Estimate the Probability Density Function (PDF) of $Y$ using a normalized histogram.
   - Use exactly 100 bins evenly spaced over the range $Y \in [-2.0, 2.0]$.
   - Bin $i$ (0 to 99) has a width of $\Delta Y = 0.04$.
   - Any $Y$ falling outside $[-2.0, 2.0]$ should be ignored.
   - Normalize the bin counts so that the area under the histogram equals 1.0. The PDF value for bin $i$ is `count[i] / (N_total_valid * delta_Y)`.

3. **Numerical Integration and Differentiation**:
   - Calculate the numerical integral of your estimated PDF using the left-Riemann sum (sum of `pdf[i] * delta_Y`).
   - Calculate the numerical derivative of the PDF with respect to $Y$ using the forward difference method: `derivative[i] = (pdf[i+1] - pdf[i]) / delta_Y`. (For the last bin, set the derivative to 0).

4. **Outputs**:
   The C program must output two files:
   - `/home/user/ml_features.csv`: A CSV with a header `y_bin_center,pdf,pdf_derivative`. Print floats to 6 decimal places (e.g., `%.6f`).
   - `/home/user/summary.txt`: A single line containing the integrated area of the PDF, formatted as `Integral: %.6f`.

5. **Visualization**:
   Install `gnuplot`. Create a gnuplot script at `/home/user/plot_features.gp` that reads `ml_features.csv` (ignoring the header) and plots the `pdf` (column 2) against `y_bin_center` (column 1) as a line graph. Save the output to a PNG file at `/home/user/features.png`.

Compile your C program with `gcc -o /home/user/generate_features /home/user/generate_features.c -lm`, run it, and then run your gnuplot script. Ensure all requested output files exist and are correctly formatted.