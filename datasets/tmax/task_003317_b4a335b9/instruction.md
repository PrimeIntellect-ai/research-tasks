Can you help me process a high-dimensional sensor dataset? I am a data analyst trying to build a probabilistic clustering pipeline, but I need you to write the code and track the experiment results. 

Here is what I need you to do:
1. First, create a Python virtual environment at `/home/user/venv` and install `pandas` and `scikit-learn==1.3.2`.
2. I have a dataset located at `/home/user/sensor_data.csv`. It has 500 rows and 50 feature columns (named `f0` to `f49`).
3. Write and run a Python script at `/home/user/run_analysis.py` that does the following:
   - Loads the CSV data.
   - Standardizes the features using `StandardScaler`.
   - Performs dimensionality reduction using `PCA` to reduce the dataset down to exactly 3 components (use `random_state=42`).
   - Fits a `BayesianGaussianMixture` model (from `sklearn.mixture`) on these 3 principal components to perform probabilistic clustering. Use `n_components=5`, `max_iter=500`, and `random_state=42` for the Bayesian model.
4. Finally, implement simple experiment tracking by having your script output a JSON file at `/home/user/experiment_log.json` with exactly this structure:
```json
{
  "pca_explained_variance_ratio_sum": <float>,
  "bgm_lower_bound": <float>,
  "bgm_converged": <boolean>
}
```

Please make sure you run the script so the `experiment_log.json` file is generated.