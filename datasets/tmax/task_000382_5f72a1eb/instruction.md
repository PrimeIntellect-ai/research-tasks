You are tasked with building a data processing and modeling pipeline to analyze a set of CSV files. 

Your goals are:
1. Set up your Python environment by installing `pandas` and `scikit-learn`.
2. Read the datasets located at `/home/user/data/train.csv` and `/home/user/data/test.csv`. 
3. Perform ETL and feature engineering:
   - The dataset contains columns: `id`, `category`, `feature_A`, `feature_B`, and `target` (target is only in train.csv).
   - `feature_A` contains missing values. Impute missing values in `feature_A` (for both train and test sets) using the **median of `feature_A` from the training set** for the corresponding `category`.
   - **Crucial:** `feature_A` represents count data. Because of the missing values, it might be read as floats. After imputation, you must ensure that `feature_A` in both train and test sets is strictly of integer type (e.g., `int64`), not floats.
   - Save the cleaned test dataset to `/home/user/cleaned_test.csv`. It should have the same columns as the original test.csv, but with imputed and correctly typed `feature_A`.
4. Train a Ridge regression model (`sklearn.linear_model.Ridge` with default parameters) on the training set.
   - Features to use: `feature_A`, `feature_B`, and one-hot encoded `category` (using `pd.get_dummies` with `drop_first=False`, or `OneHotEncoder` without dropping). Make sure the columns match exactly between train and test.
   - Target: `target`
5. Generate predictions for the test set.
6. Save the predictions to `/home/user/predictions.csv` with exactly two columns: `id` and `target`.

Ensure your scripts are fully automated and that you leave the resulting CSV files at the specified paths.