You are tasked with fixing a machine learning preprocessing pipeline for a similarity search recommendation system. 

In `/home/user/app/`, there is a dataset (`train_data.csv` and `query_data.csv`) and a Python script (`recommend.py`). The script is supposed to find the top 1 most similar item in `train_data.csv` for each item in `query_data.csv` using Cosine Similarity.

However, the previous data analyst introduced a critical data leakage bug. The script currently combines the training and query data to fit the `SimpleImputer` (mean strategy) and `StandardScaler`. This means information from the queries is leaking into the feature statistics used for the training data, and vice-versa. Furthermore, the analyst didn't handle an extreme outlier in the training data, which heavily skews the mean imputation and scaling.

Your task:
1. Modify `/home/user/app/recommend.py` to fix the data leakage. The imputer and scaler must be `fit` ONLY on the training data, and then used to `transform` both the training and query data.
2. Before fitting the imputer and scaler, remove any row in the training data where the value in the `feature_1` column is strictly greater than 1000 (this handles the outlier).
3. Run the corrected Python script.
4. The script generates a JSON file. Ensure your final output is written to `/home/user/app/recommendations.json` containing the exact mapping of `query_id` to the best matching `train_id`.
5. Use the provided `/home/user/app/track_experiment.sh` script to log your run. You must execute this bash script after generating your final `recommendations.json` file. It will append the results to `/home/user/app/experiment_log.json`.

Ensure your final `recommendations.json` uses the format:
```json
{
  "q1": "t2",
  "q2": "t1"
}
```