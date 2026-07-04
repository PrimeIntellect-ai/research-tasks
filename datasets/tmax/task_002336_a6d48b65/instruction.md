You are a data scientist working on fitting a 2-component Gaussian Mixture Model (GMM) to a dataset of 1D empirical measurements. The variances of both components are known to be exactly 1.0, so the parameters to estimate are the weight of the first component ($w$), the mean of the first component ($\mu_1$), and the mean of the second component ($\mu_2$).

Your predecessor decided to fit the model using the Method of Moments, matching the first three raw moments ($E[X], E[X^2], E[X^3]$) of the data. They wrote a script located at `/home/user/fit_gmm.py` that sets up a nonlinear system of equations and attempts to solve it using `scipy.optimize.root`. 

However, the script currently fails to converge because the initial guess `[0.5, 0.0, 0.0]` results in a near-singular Jacobian matrix. 

Your task is to:
1. Fix the nonlinear equation solver in `/home/user/fit_gmm.py` so it successfully finds the roots. You may modify the initial guess or the solver method. Enforce that $0 \le w \le 1$ and $\mu_1 < \mu_2$ (swap them if necessary to maintain this convention).
2. Evaluate the fit quality by calculating the 1-Wasserstein distance between the empirical data in `/home/user/data.txt` and the theoretical fitted distribution. Generate 100,000 random samples from your fitted GMM to compute this distance using `scipy.stats.wasserstein_distance`.
3. Save the final parameters as a single comma-separated line (`w,mu1,mu2`) in `/home/user/params.txt`.
4. Save the calculated Wasserstein distance as a single float in `/home/user/distance.txt`.
5. Create a regression test script at `/home/user/test_fit.py` that acts as a test suite. It should independently load `/home/user/data.txt` and `/home/user/params.txt`, compute the Wasserstein distance exactly as above, and raise an `AssertionError` if the distance is greater than 0.1, exiting with code 0 on success.

**Environment details:**
- The data is located at `/home/user/data.txt`.
- You can install any required standard Python scientific libraries (like `numpy`, `scipy`) via `pip` if they are missing.