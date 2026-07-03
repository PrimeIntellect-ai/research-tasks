You are a Machine Learning Engineer preparing training data for a customer behavior model. You need to process raw transaction and search query data, compute simple text embeddings, apply bootstrapping to estimate revenue confidence intervals, and track your experiment metadata.

The data is located in `/home/user/raw_data/`:
1. `/home/user/raw_data/transactions.csv` - Contains columns `txn_id`, `user_id`, and `revenue`.
2. `/home/user/raw_data/queries.json` - Contains a JSON array of dictionaries, each with `user_id` and `user_query`.

Write a Python script at `/home/user/prepare_data.py` that performs the following steps:

1. **Multi-source joining**: Load both files into pandas DataFrames. Perform an inner join on `user_id`.
2. **Missing value handling**: Fill any missing (null) values in the `user_query` column with the exact string `"empty"`.
3. **Outlier handling**: Remove any rows where `revenue` is negative (`< 0`) or excessively high (`> 5000`).
4. **Embedding computation**: Use `sklearn.feature_extraction.text.HashingVectorizer(n_features=10)` to compute embeddings for the `user_query` column of the cleaned data. Sum the 10 features for each row to create a single float value, and store this in a new column called `query_embedding_sum`.
5. **Sampling and bootstrap**: We need to estimate the 95% confidence interval of the mean revenue of our cleaned dataset.
   - Set `numpy.random.seed(42)`.
   - Generate exactly 1000 bootstrap samples of the cleaned data's `revenue` array (each sample drawn with replacement, and size equal to the number of rows in the cleaned dataset).
   - Calculate the mean revenue for each of the 1000 samples.
   - Calculate the 2.5th and 97.5th percentiles of these 1000 means to form the 95% confidence interval using `numpy.percentile`.
6. **Experiment tracking**: Save the summary of your pipeline to a JSON file at `/home/user/experiment_summary.json` with the following exact keys:
   - `"initial_rows"`: Integer count of rows immediately after the inner join (before any cleaning).
   - `"outliers_removed"`: Integer count of rows removed due to the revenue outlier rules.
   - `"cleaned_rows"`: Integer count of rows remaining after outlier removal.
   - `"bootstrap_revenue_ci_lower"`: Float, lower bound (2.5th percentile) of the bootstrap revenue means, rounded to 2 decimal places.
   - `"bootstrap_revenue_ci_upper"`: Float, upper bound (97.5th percentile) of the bootstrap revenue means, rounded to 2 decimal places.
   - `"embedding_sum_mean"`: Float, the mean of the `query_embedding_sum` column across the cleaned dataset, rounded to 4 decimal places.

Run your script to ensure `/home/user/experiment_summary.json` is generated correctly.