I need you to act as a Machine Learning Engineer and prepare some training data while validating its schema, reducing its dimensionality, and tracking a baseline experiment.

I have generated a dataset at `/home/user/data.csv`. It contains 10 feature columns (`f1` to `f10`) and one `target` column. However, the data extraction was flawed, and some rows violate our schema by containing non-numeric strings or missing values (nulls) in the feature columns.

Please write a script in your preferred language to perform the following pipeline:

1. **Data Schema Enforcement:** Read `/home/user/data.csv`. Filter out and entirely drop any rows where any of the feature columns (`f1` through `f10`) or the `target` column contain null values, NaNs, or cannot be parsed as numeric values. 
2. **Dimensionality Reduction:** Extract the cleaned feature columns (`f1` to `f10`). Initialize a Principal Component Analysis (PCA) model configured to reduce the data to exactly **3 components**. Set the `random_state` parameter to `42` for reproducibility. Fit and transform the cleaned features.
3. **Model Training and Evaluation:** Train a standard Logistic Regression model (with default parameters, but set `random_state=42`) using the 3 PCA components as input features to predict the `target` column. Calculate the model's accuracy on this exact same training set (no train/test split is needed).
4. **Experiment Tracking:** Calculate the sum of the explained variance ratio of your 3 PCA components. Save this metric and the model's accuracy into a JSON file at `/home/user/run_metrics.json`. 

The JSON file must have exactly this format:
```json
{
  "variance_explained": <float>,
  "accuracy": <float>
}
```
*Note: Both float values must be rounded to exactly 4 decimal places.*

Execute your script so the JSON file is generated.