You are acting as a Data Scientist troubleshooting a model fitting pipeline.

In your workspace (`/home/user`), there is a Python script named `model_fit.py`. This script is designed to find a parameter `a` for the function `f(x) = a * sin(x) * exp(-x^2)` such that its integral over the interval `[0, 2]` equals exactly `1.5`. 

To ensure accuracy, the pipeline implements two integration methods:
1. A deterministic numerical integration using `scipy.integrate.quad` (the trusted baseline).
2. A Monte Carlo (MC) integration method, which is intended to be used for higher-dimensional generalizations later.

Currently, the script is failing its automated regression test. The Monte Carlo integration result does not match the numerical integration baseline, raising a `ValueError`. 

Your task is to:
1. Inspect `/home/user/model_fit.py` and identify why the Monte Carlo integration is yielding incorrect results.
2. Fix the mathematical or logical bug in the `integrate_mc` function. Do not change the random seed or the number of samples.
3. Run the script. When the regression test passes, it will automatically fit the parameter `a` and write the result to `/home/user/fit_result.txt`.

Ensure that `/home/user/fit_result.txt` is successfully created and contains the correct fitted parameter formatted to 4 decimal places.