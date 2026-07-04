You are a Machine Learning Engineer responsible for preparing and evaluating training data. 

You have inherited a project with a script located at `/home/user/train.py`. The script reads a dataset from `/home/user/data.csv` and trains a Ridge regression model. However, you strongly suspect there is data leakage in the preprocessing pipeline—specifically, the features are scaled using `fit_transform` on the entire dataset *before* it is split into training and test sets.

Your task is to fix the pipeline, evaluate the corrected model, perform statistical analysis, and benchmark inference performance.

Write a new script, `/home/user/evaluate.py`, that performs the following steps:
1. Load `/home/user/data.csv`.
2. Split the data into features (`A`, `B`, `C`) and the `target` column.
3. Use `sklearn.model_selection.train_test_split` with `test_size=0.2` and `random_state=42`.
4. **Fix the Leakage:** Fit a `StandardScaler` *only* on the training set, and use it to transform both the training and test sets.
5. Train a `sklearn.linear_model.Ridge` model with default parameters on the scaled training data.
6. Generate predictions on the scaled test set and calculate the Mean Squared Error (MSE).
7. **Correlation Analysis:** Calculate the Pearson correlation coefficient between feature `A` and feature `B` exclusively using the *properly scaled test set*.
8. **Bootstrap Methods:** Calculate the standard error of the test MSE using a bootstrap approach. Set `numpy.random.seed(42)` immediately before the bootstrap loop. Perform 1000 iterations where you sample the test indices with replacement (sample size equal to the test set size), calculate the MSE for each bootstrap sample, and compute the standard deviation of these 1000 MSE values.
9. **Inference Benchmarking:** Measure the average time it takes to run `model.predict()` on a *single* sample from the test set. Run a loop over the first 1000 rows of the test set (or cycle through the test set if it's smaller than 1000) one by one, measure the time for each prediction, and compute the average in microseconds.

Finally, your script must save a JSON file to `/home/user/results.json` containing your findings. The JSON must exactly match this schema:
```json
{
  "fixed_mse": float,
  "mse_std_err": float,
  "corr_A_B": float,
  "avg_inference_us": float
}
```

Constraints:
- Use `random_state=42` for the train-test split.
- Use `np.random.seed(42)` right before bootstrapping.
- Do not round the metrics in the JSON file; output them at full floating-point precision.