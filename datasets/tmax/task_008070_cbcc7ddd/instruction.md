You are an astrophysical researcher organizing a newly acquired dataset of exoplanet candidates. You need to validate the raw data, convert it to an efficient storage format, calculate confidence intervals using bootstrapping, and build predictive models.

The raw data is located at `/home/user/astro_data/raw_candidates.csv`. 

Perform the following tasks:

**Phase 1: Data Schema Enforcement & Storage**
1. Read the raw dataset.
2. Enforce the following schema and domain constraints. Drop any rows that do not strictly meet these criteria:
   - `id`: must be an integer.
   - `mass`: must be a positive float (`> 0`).
   - `radius`: must be a positive float (`> 0`).
   - `orbital_period`: must be a positive float (`> 0`).
   - `status`: must be exactly the string `"confirmed"` or `"false_positive"`.
3. Save the cleaned dataset as a Parquet file at `/home/user/astro_data/clean_data.parquet`. 

**Phase 2: Bootstrap Methods**
1. Read `clean_data.parquet`.
2. Filter the data to include only planets with `status == "confirmed"`.
3. Perform a bootstrap analysis to calculate the 95% confidence interval for the mean of the `radius` column. 
   - Use exactly `N=1000` bootstrap samples.
   - Use `numpy.random.seed(42)` immediately before generating your bootstrap indices to ensure reproducibility.
   - Sample with replacement (size of each sample equals the number of confirmed planets).
4. Calculate the 2.5th and 97.5th percentiles of the bootstrapped means.
5. Save these two values to `/home/user/astro_data/bootstrap_ci.txt` as a single comma-separated line, rounded to 4 decimal places. Example: `2.4152,2.5321`

**Phase 3: Model Training and Evaluation**
Using `clean_data.parquet`, perform the following:
1. **Regression Model**: 
   - Filter for `status == "confirmed"`.
   - Train a `RandomForestRegressor` (from `sklearn.ensemble`, with `random_state=42`) to predict `radius` using `mass` and `orbital_period` as features.
   - Evaluate the model using 5-fold cross-validation. Calculate the Root Mean Squared Error (RMSE) of the cross-validation scores (calculate the mean of the MSE scores across the 5 folds, then take the square root).
2. **Classification Model**:
   - Use the entire cleaned dataset (both statuses).
   - Train a `LogisticRegression` classifier (from `sklearn.linear_model`, with `random_state=42`) to predict `status` using `mass`, `radius`, and `orbital_period` as features.
   - Evaluate the model using 5-fold cross-validation. Calculate the mean macro F1-score across the 5 folds.
3. Save the results to `/home/user/astro_data/metrics.json` in the following exact JSON format (values rounded to 4 decimal places):
```json
{
  "rmse": 1.2345,
  "f1": 0.8765
}
```