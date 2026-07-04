You are an applied computational researcher investigating a stochastic particle transport model. The core simulation engine for this model was written in C years ago, but the source code has been lost. You only have access to the compiled, stripped binary located at `/app/oracle_sim`. 

This binary takes a single integer argument, `N` (the number of particles to simulate), and prints `N` floating-point numbers to standard output (one per line). These numbers represent the final 1D spatial coordinates of the simulated particles.

Your goal is to build a reproducible computation pipeline that analyzes the spatial distribution of these particles and computes a specific non-linear expectation using numerical integration.

Write a Python script at `/home/user/pipeline.py` that performs the following steps:
1. Executes `/app/oracle_sim 500000` to generate a large representative sample of particle coordinates.
2. Captures and parses the standard output into a numerical array.
3. Performs continuous density estimation to approximate the underlying Probability Density Function (PDF), $p(x)$, of the particle positions. You must use a Gaussian Kernel Density Estimator (KDE) with Scott's Rule for bandwidth selection.
4. Uses robust numerical integration (e.g., `scipy.integrate.quad`) over your estimated PDF to compute the expected value of the measurement function $g(x) = x^2 \cdot \cos(x)$ for particles that land strictly in the interval $[1.0, 4.0]$. 
   Mathematically, you are computing: 
   $$I = \int_{1.0}^{4.0} p(x) \cdot x^2 \cdot \cos(x) dx$$
5. Writes the final computed integral $I$ as a single floating-point number (e.g., standard plain text, no extra characters or formatting) to `/home/user/integral_result.txt`.

Constraints:
- You must use Python as your primary language for the analysis.
- You may use standard scientific libraries (`numpy`, `scipy`, etc.). Ensure you install them via pip if they are missing in the environment.
- The pipeline must execute without human intervention when `python /home/user/pipeline.py` is run.