You are a Machine Learning Engineer preparing synthetic training data for a physics-informed neural network. To ensure your custom data generator is properly calibrated, you need to validate its output against an analytical distribution using Monte Carlo simulation, convergence testing, and parallel computing in Go.

The target probability density function (PDF) is:
$f(x) = \frac{3}{4}(1 - x^2)$ for $x \in [-1, 1]$

Your task is to write a Go program (`/home/user/mc_sampler.go`) that does the following:
1. **Parallel Monte Carlo Simulation**: Use Go's goroutines to implement Rejection Sampling to draw $N$ independent samples from this PDF. Since random number generation in parallel can cause race conditions or bottlenecks, ensure each worker goroutine uses its own local random number generator (e.g., `rand.New(rand.NewSource(...))`). Use 4 concurrent workers.
2. **Analytical Validation**: Calculate the empirical Cumulative Distribution Function (CDF) of your generated samples evaluated at 201 evenly spaced points between -1.0 and 1.0 (inclusive, step size 0.01). Compare this to the analytical CDF. You will need to derive the analytical CDF yourself based on the PDF provided.
3. **Probability Distribution Distance**: Compute the Kolmogorov-Smirnov (KS) distance, which is the maximum absolute difference between the empirical CDF and the analytical CDF across the 201 evaluation points.
4. **Convergence Testing**: Run this sampling and evaluation pipeline for three different sample sizes: $N = 10^4, 10^5,$ and $10^6$. 

Your Go program must output the results to a CSV file located exactly at `/home/user/convergence.log`. The file should contain exactly three lines (no headers), one for each $N$, in ascending order of $N$, formatted exactly like this:
```
10000,0.01452
100000,0.00318
1000000,0.00092
```
(Note: the distance values will vary depending on your random seed, but should properly reflect the KS distance and demonstrate statistical convergence).

Finally, execute your Go program to generate the `/home/user/convergence.log` file.