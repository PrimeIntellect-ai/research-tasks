You are a data analyst tasked with processing a dataset of customer profiles to build a simple predictive model and perform a similarity search. 

You have been provided with two files:
- `/home/user/train.csv` (Columns: `id`, `age`, `income`, `score`, `spend`)
- `/home/user/test.csv` (Columns: `id`, `age`, `income`, `score`)

Your goal is to complete the following pipeline and save your final results to `/home/user/results.json`:

1. **Schema Enforcement**: 
   Load both CSV files. The expected schema for both files is: `id` (integer), `age` (integer), `income` (float), `score` (float), and for train.csv `spend` (float). 
   Drop any rows that contain missing values (NaN/Null) or have values that cannot be cast to these exact numerical types.

2. **Correlation Analysis & Feature Selection**:
   On the cleaned `train.csv`, calculate the absolute Pearson correlation coefficient between each feature (`age`, `income`, `score`) and the target variable (`spend`). 
   Select the **top 2** features that have the highest absolute correlation with `spend`.

3. **Regression Model**:
   Using `scikit-learn`, train a standard `LinearRegression` model on the cleaned training data to predict `spend`. Use **only** the 2 features selected in the previous step as your inputs (X). Do not use any scaling or intercept modifications; use the default `LinearRegression()` parameters.

4. **Prediction**:
   Use your trained model to predict the `spend` for the cleaned `test.csv` dataset. Round the predictions to exactly 2 decimal places.

5. **Similarity Search**:
   Find the customer in the cleaned `train.csv` dataset that is most mathematically similar to the customer in `test.csv` with `id = 101`. 
   Similarity must be determined using the lowest **Euclidean distance** calculated using **only** the 2 selected features (unscaled).

Save your results in `/home/user/results.json` strictly matching this JSON schema:
```json
{
  "selected_features": ["feature_name_1", "feature_name_2"], 
  "predictions": {
    "100": 1234.56,
    "101": 2345.67
  },
  "most_similar_train_id_to_test_101": 42
}
```
*Note: Ensure the `selected_features` array contains the strings of the two feature names in alphabetical order. The `predictions` dictionary keys should be strings of the valid test `id`s, and the values should be the predicted spend (float rounded to 2 decimal places).*