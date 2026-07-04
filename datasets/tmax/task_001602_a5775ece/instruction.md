You are an ML Engineer working on a headless Linux server. You need to benchmark the inference speed of two different regression models, perform statistical tests on the results, and generate a visualization. 

First, look for the dataset at `/home/user/data.csv`. (It contains columns `f1`, `f2`, `f3`, `f4`, `f5` and a `target` column).

Write a Python script at `/home/user/benchmark.py` that performs the following steps:
1. Load the dataset using pandas.
2. Train two models on the entire dataset: a `Ridge` regressor (`sklearn.linear_model.Ridge`) and a `DecisionTreeRegressor` (`sklearn.tree.DecisionTreeRegressor`). Use default hyperparameters for both.
3. Benchmark inference performance: For each model, call `.predict()` on the *entire dataset*, and record the time it takes. Repeat this 100 times per model to collect an array of 100 execution times for Ridge and 100 execution times for Decision Tree.
4. Perform an independent two-sample t-test (`scipy.stats.ttest_ind`) to compare the inference times of the Ridge model vs the Decision Tree model.
5. Save the summary statistics to a JSON file at `/home/user/results.json`. The JSON must contain exactly these keys (with float values):
   - `mean_time_ridge`: the mean inference time for Ridge
   - `mean_time_tree`: the mean inference time for the Decision Tree
   - `t_statistic`: the calculated t-statistic
   - `p_value`: the calculated p-value
6. Create a boxplot visualizing the distribution of the 100 inference times for each model (two boxes side-by-side). Save this plot as a PNG image to `/home/user/benchmark_plot.png`. 
*Note on the plot:* You are running on a headless server without a display manager. Standard matplotlib configurations might attempt to open a window and fail or produce blank plots. You must configure your script to avoid this (e.g., using the appropriate backend).

Run your script to ensure `/home/user/results.json` and `/home/user/benchmark_plot.png` are generated successfully.