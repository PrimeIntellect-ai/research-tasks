I am preparing training data and building a classification model, but my pipeline has a few issues. I have a script located at `/home/user/pipeline.py` that reads `/home/user/train.csv` and `/home/user/test.csv`, trains a RandomForest model, and writes to `/home/user/predictions.csv`.

However, the downstream data engineering team is rejecting my output file. There is a silent bug in my pandas code: the `id` column and the `f2` feature column (which represents integer counts) are being converted to floats (e.g., `101.0`) because of how missing values are handled. Also, the pipeline predictions are not reproducible and change slightly on every run.

Please modify `/home/user/pipeline.py` to fix these issues and run it to produce the correct `/home/user/predictions.csv`. 

Your fixed pipeline must meet these strict requirements:
1. **Fix the Imputation & Data Leakage**: Currently, the script might be imputing NaNs incorrectly. You must impute missing values in the `f2` column using the **median of the `f2` column from the training set only** (apply this same learned median to the test set).
2. **Strict Data Types**: Ensure that `id` and `f2` are explicitly cast to and remain `int64` throughout the pipeline and in the final output. There should be no `.0` in the output file for the `id` column.
3. **Pipeline Reproducibility**: Ensure the `RandomForestClassifier` uses `random_state=42`. Do not change the `n_estimators=50` parameter.
4. **Output Format**: Save the test set predictions to `/home/user/predictions.csv` with exactly two columns: `id` and `target`. The `id` must be an integer.

Run the script to generate `/home/user/predictions.csv` once you have fixed it. Do not alter the raw CSV files.