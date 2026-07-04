You are a data scientist evaluating two mathematical models for an observed physical process. You need to compare their fits using a bootstrap approach, leveraging parallel computing to speed up the numerical integration required for the models.

A dataset has been provided at `/home/user/dataset.csv` with two columns: `t` (time) and `y` (observed value).

The two models for the expected value of `y` given `t` are:
*   **Model A:** $y_A(t) = 2.0 \int_0^t e^{-x^2 / 2} dx$
*   **Model B:** $y_B(t) = 2.5 \int_0^t \frac{\sin(x)}{x} dx$ (assume the integrand is 1 at $x=0$)

Write and execute a Python script that does the following:
1.  Read the dataset.
2.  Set the global numpy random seed to `42` (`numpy.random.seed(42)`).
3.  Sequentially generate 50 bootstrap samples of the dataset. A bootstrap sample is created by sampling the row indices with replacement to create a new dataset of the same size as the original. (Do this in a loop 50 times, storing the index arrays or the sampled data).
4.  Use Python's `multiprocessing.Pool` with 4 worker processes to evaluate the models for these 50 bootstrap samples in parallel.
5.  For each bootstrap sample, calculate the Mean Squared Error (MSE) for both Model A and Model B. Use `scipy.integrate.quad` for the numerical integration.
6.  Once all 50 pairs of MSEs are computed, perform a paired t-test comparing the 50 MSEs of Model A against the 50 MSEs of Model B using `scipy.stats.ttest_rel(mse_A, mse_B)`.
7.  Save the results of the t-test to a JSON file at `/home/user/stats.json` with the exact keys `"statistic"` and `"p_value"`.

Ensure your script handles the integration correctly and uses parallel processing as requested.