You are tasked with helping a data scientist fix a malfunctioning model fitting pipeline.

We have a dataset of 1D experimental measurements located at `/home/user/data.csv` (one value per line, with a header `value`). We believe this data comes from a Gaussian Mixture Model (GMM) with two components:
$P(x) = w \cdot \mathcal{N}(x | \mu_1, \sigma_1^2) + (1 - w) \cdot \mathcal{N}(x | \mu_2, \sigma_2^2)$

The previous data scientist tried to write a Python script to fit this model using standard gradient descent / Nelder-Mead optimization, but the step-size adaptation kept diverging into invalid parameter spaces (e.g., negative standard deviations) or getting stuck in terrible local minima. 

Your objective is to:
1. Write a robust optimization routine in Python (you may use `scipy.optimize`, such as genetic algorithms like `differential_evolution`, or any bounded optimizer) to find the Maximum Likelihood Estimation (MLE) for the parameters: `mu1`, `std1`, `mu2`, `std2`, and `weight` ($w \in [0, 1]$). Note: std1 and std2 must be strictly positive.
2. Evaluate the goodness of your fit by computing the 1-Wasserstein distance between the empirical data in `data.csv` and a set of 100,000 synthetic samples generated from your fitted theoretical model. Use `scipy.stats.wasserstein_distance`.
3. Create an experimental data visualization overlaying a normalized histogram of `data.csv` (using 50 bins) and the Probability Density Function (PDF) curve of your fitted model. Save this plot to `/home/user/fit_plot.png`.
4. Save your final fitted parameters and the computed Wasserstein distance to `/home/user/results.json` strictly using the following schema:
```json
{
  "mu1": float,
  "std1": float,
  "mu2": float,
  "std2": float,
  "weight": float,
  "wasserstein_distance": float
}
```

Constraints & Notes:
- Ensure $w$ corresponds to the component with the smaller mean (`mu1` < `mu2`). If your optimizer swaps them, correct the labels before saving the JSON.
- The optimizer must run without manual intervention and reliably converge to the global optimum.
- You must write the fitting script from scratch or use standard libraries; do not use `sklearn.mixture.GaussianMixture` (we need to test your custom optimization skills).