You are a data scientist tasked with resolving a reproducibility issue in a statistical physics model used for sequence alignment thermodynamics. 

We need to estimate a thermodynamic parameter $\theta$ using MCMC. The likelihood depends on calculating a partition function $Z(\theta)$ via numerical integration:
$Z(\theta) = \int_{0}^{10} e^{-x \cdot \theta} dx$

Previously, naive floating-point summation during the numerical integration led to non-reproducible likelihood evaluations across different machines due to floating-point reduction order and precision loss.

Your task is to write a reproducible C program that performs this integration robustly and runs a short MCMC chain.

1. Create a C program at `/home/user/mcmc_Z.c`.
2. Implement a function `double integrate_Z(double theta)` that numerically computes the integral above using the **Trapezoidal rule** with exactly $N = 1,000,000$ intervals (step size $\Delta x = 10^{-5}$). 
3. **Crucial:** To prevent precision loss and ensure reproducibility regardless of compiler optimization flags, you **must** implement **Kahan summation** inside the integration loop.
4. In the `main` function, calculate $Z$ for $\theta = 1.995$.
5. Write the output to a file `/home/user/result.txt` exactly in this format:
   `Z_val: 0.XXXXXX` (rounded to 6 decimal places).
6. Create a build script `/home/user/build_and_run.sh` that compiles `mcmc_Z.c` using `gcc -O3 -o mcmc_Z mcmc_Z.c` and runs it.

Ensure the output file is created successfully.