You are a data analyst tasked with building a reproducible prediction pipeline. We have a set of observations in `/app/data.csv` containing two columns: `x` and `y`.

We are modeling this using Bayesian linear regression: $y = \beta x + \alpha + \epsilon$.
The prior distributions for $\alpha$ and $\beta$ are provided in an image located at `/app/equation_params.png`. 
You need to:
1. Extract the prior parameters from `/app/equation_params.png`. You can use `tesseract` for OCR.
2. Use these priors and the data in `/app/data.csv` to compute the exact Maximum A Posteriori (MAP) estimates for $\alpha$ and $\beta$. Assume $\epsilon \sim \mathcal{N}(0, 1)$.
3. Write a Python script at `/home/user/predict.py` that takes a single float argument `x` from the command line and prints the predicted `y` value using the computed MAP estimates, formatted to exactly 4 decimal places.

Your script must behave exactly like our reference implementation. It should be executable via `python3 /home/user/predict.py <x>`.

Ensure your pipeline is completely reproducible and does not rely on stochastic sampling (like MCMC) for the final parameters; you must calculate the exact analytical MAP estimates or use an optimizer with an extremely tight tolerance that matches the analytical solution.