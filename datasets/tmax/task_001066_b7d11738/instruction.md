You are an AI assistant helping a researcher organize and analyze a dataset of chemical compounds. The dataset is located at `/home/user/chemical_data.csv`. The target variable is `is_toxic` (binary). 

Your objective is to perform a specific data processing pipeline and output the results to a JSON file. Please write and execute Python code to perform the following steps:

1. **Correlation Analysis**:
   - Load the dataset `/home/user/chemical_data.csv`.
   - Calculate the Pearson correlation matrix for all features (excluding the `is_toxic` target).
   - Iterate through the feature columns from left to right (from the first feature to the last). Keep a column if it does NOT have an absolute correlation strictly greater than `0.85` with any of the *previously kept* feature columns. Drop the columns that are highly correlated with already-kept columns.

2. **Dimensionality Reduction**:
   - Using only the remaining (kept) features, standardize the data (zero mean, unit variance) using `sklearn.preprocessing.StandardScaler`.
   - Apply Principal Component Analysis (PCA) using `sklearn.decomposition.PCA` to reduce the feature space to exactly `5` components. Do not set a random state for PCA as it's deterministic.

3. **Hypothesis Testing**:
   - For each of the 5 PCA components (index 0 to 4), perform an independent two-sample Welch's t-test (assuming unequal variances, e.g., using `scipy.stats.ttest_ind` with `equal_var=False`) comparing the values of the component between the `is_toxic = 1` group and the `is_toxic = 0` group.
   - Select and keep only the PCA components that have a p-value strictly less than `0.05`.

4. **Classification**:
   - Using *only* the significant PCA components identified in Step 3, train a Logistic Regression model on the entire dataset to predict `is_toxic`.
   - Use `sklearn.linear_model.LogisticRegression(random_state=42)`. Do not change other default parameters.
   - Calculate the classification accuracy of this model on the training data.

5. **Reporting**:
   - Create a JSON file at `/home/user/results.json` containing the exact following structure:
     ```json
     {
       "dropped_features": ["F_X", "F_Y"], 
       "significant_components": [0, 1, 3],
       "model_accuracy": 0.8452
     }
     ```
   - `"dropped_features"`: A list of strings containing the exact names of the features dropped in Step 1, in the order they were evaluated.
   - `"significant_components"`: A list of integers (0-indexed) representing the indices of the PCA components kept in Step 3, sorted in ascending order.
   - `"model_accuracy"`: A float representing the accuracy of the Logistic Regression model, rounded to exactly 4 decimal places.

Ensure you install any necessary Python packages (like `pandas`, `numpy`, `scikit-learn`, `scipy`) using `pip`.