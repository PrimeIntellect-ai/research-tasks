You are a performance engineer profiling a numerical simulation. You've noticed that domain decomposition and the order of floating-point reduction are causing non-reproducible results. To understand how the floating-point roundoff error scales with the problem size, you need to perform a convergence test using Python.

Write and execute a Python script at `/home/user/error_analysis.py` that does the following:

1. For each $N \in \{10^3, 10^4, 10^5, 10^6, 10^7\}$:
2. Generate an array of terms $T_i = 1/i$ for $i = 1, 2, \dots, N$.
3. Compute the sum of these terms in two different ways to simulate different reduction orders:
   - **Ascending sum ($S_{asc}$)**: Add the terms starting from $i=1$ up to $N$.
   - **Descending sum ($S_{desc}$)**: Add the terms starting from $i=N$ down to $1$.
4. **Important constraint**: You must use strict single-precision floating-point arithmetic (`numpy.float32`) for both the terms and the running accumulator. Do **not** use `numpy.sum()` or `math.fsum()` because they use pairwise or extended-precision summation. You must use a standard iterative loop (e.g., `for` loop) to ensure naive left-to-right accumulation.
5. Compute the absolute error $E_N = |S_{asc} - S_{desc}|$.
6. Perform a linear regression (curve fitting) on $\log_{10}(E_N)$ versus $\log_{10}(N)$ to find the empirical scaling exponent (the slope of the best-fit line).

Save the computed slope, rounded to exactly two decimal places, to a file named `/home/user/slope.txt`. 

Your environment has `numpy` and `scipy` installed.