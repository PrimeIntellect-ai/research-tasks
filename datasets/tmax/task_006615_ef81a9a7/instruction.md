You are a data scientist debugging a numerical instability issue. You are trying to fit a high-degree polynomial to a tightly clustered Monte Carlo dataset, but the design matrix is near-singular (highly collinear), leading to wild predictions in standard least-squares regression. 

To demonstrate and fix this, create a Python script at `/home/user/fit_models.py` that performs the following exact steps:

1. Set the random seed via `numpy.random.seed(42)`.
2. Generate an input array `x` of 1000 samples drawn from a uniform distribution between 0.99 and 1.01. Reshape `x` to be a 2D column vector `(1000, 1)`.
3. Generate noise `epsilon` of 1000 samples drawn from a normal distribution with mean 0.0 and standard deviation 0.001. Reshape it to `(1000, 1)`.
4. Generate the target variable `y` using the true underlying model: `y = 3*x**2 + 2*x + 1 + epsilon`.
5. Use `sklearn.preprocessing.PolynomialFeatures` to generate polynomial features up to `degree=10` for `x`. Set `include_bias=False`.
6. Fit a standard unregularized model using `sklearn.linear_model.LinearRegression` on the polynomial features.
7. Fit a regularized model using `sklearn.linear_model.Ridge` with `alpha=1.0` on the same polynomial features.
8. Create a test point `x_test = [[1.0]]`, transform it using the same `PolynomialFeatures` object, and predict `y` using both models.
9. Save the two scalar predictions as a single line of text in `/home/user/predictions.txt` in the format: `LinearPrediction, RidgePrediction`. (e.g., `5.9987, 6.0012`).

After writing the script, execute it so that `/home/user/predictions.txt` is created.