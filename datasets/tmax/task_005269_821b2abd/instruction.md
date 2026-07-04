You are a machine learning engineer preparing a synthetic data pipeline. You need to model the underlying density of a 1D dataset of noisy sensor readings, validate the analytical properties of your model, and ensure numerical stability when scoring extreme outliers.

The data is located at `/home/user/sensor_data.csv`, containing a single column `value` with no header.

Perform the following steps:
1. **Density Estimation:** Use `sklearn.mixture.GaussianMixture` to fit a 2-component Gaussian Mixture Model (GMM) to the data. 
   - Ensure you use `n_components=2`, `random_state=42`, and `max_iter=1000`.
   - Extract the weights, means, and variances (covariances) of the two components.

2. **Analytical Validation:** Define the probability density function (PDF) of your fitted GMM. Use `scipy.integrate.quad` to compute the definite integral of this PDF over the interval `[-1000, 1000]`. This serves as an analytical validation that your empirical density correctly integrates to approximately 1.

3. **Numerical Stability Testing:** You need to score the log-likelihood of extreme outlier values. The outliers are `x_extreme = [50.0, 100.0, 500.0, 1000.0]`.
   - **Method A (Naive):** Calculate the log-likelihood using `log( w1 * N(x|mu1, var1) + w2 * N(x|mu2, var2) )` where `N` is the normal PDF. Use standard `scipy.stats.norm.pdf` for `N`. 
   - **Method B (Stable):** Calculate the log-likelihood using the log-sum-exp trick to avoid underflow. Use `scipy.stats.norm.logpdf` and `scipy.special.logsumexp`.
   - Evaluate both methods on `x_extreme`.

4. **Output Generation:** Save your results to a JSON file at `/home/user/results.json`.
   The JSON file must have the exact following keys and format:
   - `"gmm_weights"`: List of 2 floats, sorted in **ascending** order of the weights.
   - `"gmm_means"`: List of 2 floats, representing the means corresponding to the sorted weights.
   - `"gmm_variances"`: List of 2 floats, representing the variances corresponding to the sorted weights. (Extract these from the GMM's `covariances_` attribute).
   - `"integral_value"`: Float, the result from `scipy.integrate.quad` (just the integral value, not the error estimate).
   - `"naive_log_likelihoods"`: List of 4 values. If an underflow causes a `-inf` value, represent it as the string `"-inf"`. Otherwise, output the float.
   - `"stable_log_likelihoods"`: List of 4 floats from Method B.

Ensure all float values in the JSON are rounded to 6 decimal places. Use Python to complete this task. You must install any required pip packages (like `scikit-learn`, `scipy`, `numpy`) yourself if they are missing.