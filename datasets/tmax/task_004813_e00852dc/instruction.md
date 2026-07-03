You are acting as a Machine Learning Engineer preparing synthetic training data for a complex Bayesian inference task. You need to compute the log-posterior densities for a dataset, but you are running into some pipeline issues.

First, your team uses a custom C-based Python extension for MCMC initialization called `fast-mcmc-utils`. The source code is vendored at `/app/fast-mcmc-utils-1.0/`. However, it currently fails to compile and install. You must identify the problem in its C source code, fix the bug, and install the package globally in the system python environment. 

Second, you need to write an executable Python script at `/home/user/generate_features.py` that calculates the log-posterior density of a single feature value. 

Your script `/home/user/generate_features.py` must:
1. Accept exactly one command-line argument: a float `x`.
2. Import the newly installed `fast_mcmc_utils` module and pass `x` into its `init_chain(x)` function, which will return a transformed float `y`.
3. Compute the log-posterior density of `y` assuming it comes from a 2-component Gaussian mixture model (ignoring the normalization constant $1/\sqrt{2\pi}$ for simplicity):
   Component 1: weight $w_1 = 0.3$, mean $\mu_1 = -5.0$, variance $\sigma^2_1 = 1.0$
   Component 2: weight $w_2 = 0.7$, mean $\mu_2 = 5.0$, variance $\sigma^2_2 = 1.0$
   
   The naive mathematical formula for the mixture likelihood (without the $\sqrt{2\pi}$ term) is:
   `L(y) = 0.3 * exp(-0.5 * (y - -5.0)^2) + 0.7 * exp(-0.5 * (y - 5.0)^2)`
   You must compute the natural logarithm of this likelihood: `log(L(y))`
4. Print the final log-posterior to `stdout` formatted to exactly 6 decimal places.

**Critical Requirement:** Your script will be tested against extreme values of `x` (which leads to extreme values of `y`). If you implement the mathematical formula naively, the `exp()` functions will underflow to 0, causing a `ValueError: math domain error` or `-inf` when taking the logarithm. You MUST use numerically stable methods (e.g., the Log-Sum-Exp trick) to ensure the script produces accurate, finite values even for very large positive or negative inputs. 

Make sure your script is executable (`chmod +x`).