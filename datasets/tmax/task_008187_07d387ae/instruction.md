You are a machine learning engineer preparing training data for a predictive maintenance model. You have two raw data files from a chemical reactor:
1. `/home/user/sensor_data.csv`: Contains `time` and `temperature` columns representing primary sensor readings over time.
2. `/home/user/secondary_sensors.csv`: Contains 10 columns of secondary sensor readings (100 rows). No headers.

Your task is to create and execute a Jupyter Notebook `/home/user/prepare_data.ipynb` that processes this data and extracts specific features. You must execute the notebook from the command line (e.g., using `jupyter nbconvert --to notebook --execute`) so that it generates an output file `/home/user/results.json`.

Inside the notebook, implement the following steps:
1. **Curve Fitting & Calculus**: Fit a 3rd-degree polynomial to the `time` vs `temperature` data. Calculate the definite integral of this fitted polynomial from time = 0 to time = 10. Also calculate the exact derivative of this fitted polynomial at time = 5.
2. **Bootstrapping**: Calculate the 95% bootstrap confidence interval for the mean of the raw `temperature` data. Use exactly 10,000 resamples, the percentile method, and set the random seed to `42` for reproducibility (e.g., using `numpy.random.seed(42)` and `numpy.random.choice`).
3. **Matrix Decomposition**: Read the secondary sensor matrix. Mean-center the columns (subtract the mean of each column). Perform Singular Value Decomposition (SVD) on the centered matrix to compute Principal Components. Calculate the ratio of variance explained by the first principal component (first singular value squared divided by the sum of all singular values squared). Project the original mean-centered data onto the first two principal components.

The notebook must save a JSON file at `/home/user/results.json` containing the following structure:
```json
{
  "integral_0_10": <float>,
  "derivative_at_5": <float>,
  "bootstrap_ci_lower": <float>,
  "bootstrap_ci_upper": <float>,
  "pc1_variance_explained": <float>,
  "first_row_projected": [<float>, <float>]
}
```

Ensure your math and logic are correct, and use standard Python libraries (`numpy`, `pandas`, `json`). Execute the notebook to produce the JSON file.