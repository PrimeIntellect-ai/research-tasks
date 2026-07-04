You are a data scientist working with a legacy data pipeline. A C program generates samples from a physical process, and you need to fit a statistical model to this data.

Your tasks are:
1. You will find a C source file at `/home/user/generator.c`. Compile it into an executable named `/home/user/generator` using `gcc`.
2. Run `/home/user/generator` and redirect its standard output to `/home/user/samples.txt`.
3. The data in `samples.txt` follows a custom probability density function:
   `p(x | a) = (1 / Z(a)) * exp(-x^4 - a * x^2)`
   where `Z(a)` is the normalizing constant defined as the integral of `exp(-x^4 - a * x^2)` from negative infinity to positive infinity.
4. Write a Python script `/home/user/fit.py` that reads `samples.txt` and computes the Maximum Likelihood Estimate (MLE) for the parameter `a`. 
   - The parameter `a` is known to be in the range `[-5.0, 5.0]`.
   - Use `scipy.integrate.quad` to numerically evaluate `Z(a)`.
   - Use numerical optimization (e.g., `scipy.optimize.minimize_scalar` or `scipy.optimize.minimize`) to find the best `a` that maximizes the log-likelihood (or minimizes the negative log-likelihood).
   - Ensure your optimization is numerically stable.
5. Save the optimal parameter `a` to a file `/home/user/result.txt` in the exact format:
   `a=X.XXX` (rounded to exactly 3 decimal places).

Ensure all code handles numerical integration accurately and uses appropriate scientific computing practices. Do not use external libraries other than `numpy` and `scipy`.