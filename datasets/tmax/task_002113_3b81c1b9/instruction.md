You are a data scientist modeling a decay process. You have been given a proprietary stripped binary `/app/signal_model` which models the underlying deterministic signal given a spatial coordinate `x` and two parameters `alpha` and `beta`. 

Usage: `/app/signal_model <x> <alpha> <beta>` (outputs a single float `y`).

You also have a dataset of noisy experimental observations located at `/app/experimental_data.csv` (headers: `x,y`).

Your goals are:
1. **Reverse-engineer or black-box model the binary:** The binary is too slow to be called directly in an MCMC loop. Probe it or analyze it to deduce the simple, continuous mathematical function it computes.
2. **Implement MCMC in C++:** Write a C++ program `fit_model.cpp` (compiled to `/home/user/fit_model`) that implements a Metropolis-Hastings MCMC sampler from scratch. Use it to find the posterior distribution of `alpha` and `beta` given the experimental data. Assume a uniform prior for the parameters and a Gaussian likelihood for the noise (with an unknown or fixed standard deviation, your choice). 
3. **Calculate Posterior Means:** Output the posterior means of the parameters to `/home/user/posterior_means.txt` in the exact format: `alpha_mean,beta_mean`.
4. **Bootstrap Confidence Intervals:** Using your best-fit parameters, compute the residuals (difference between true `y` and predicted `y`). Implement a bootstrap method in your C++ program (or a separate script) to calculate the 95% confidence interval of the Mean Squared Error (MSE) of the fit. Output this to `/home/user/bootstrap_ci.txt` as `lower_bound,upper_bound`.
5. **Visualization:** Generate a plot `/home/user/fit_plot.png` (using Python, gnuplot, or similar) showing a scatter plot of the experimental data overlaid with the predicted signal curve using your posterior means.

Ensure your parameter estimation is accurate. Automated tests will evaluate the closeness of your posterior means to the true underlying parameters generating the noisy data.