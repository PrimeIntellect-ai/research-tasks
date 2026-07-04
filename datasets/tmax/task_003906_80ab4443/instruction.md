You are tasked with fixing a broken ETL and model training pipeline. 

A previous data engineer wrote a script located at `/home/user/etl_pipeline.py` to merge text data with their corresponding integer labels, compute TF-IDF embeddings, and train a basic logistic regression classifier. Unfortunately, they assumed the data was perfectly aligned. In reality, the `texts.csv` file contains some records that are missing from `labels.csv`. 

Because of the `left` merge used in the script, Pandas introduces `NaN` values for the missing labels, which silently casts the entire integer label column to `float64`. When the script attempts to train the `LogisticRegression` model, it crashes because `scikit-learn` does not accept `NaN` values in the target variable `y`.

Your objectives are:
1. Set up your Python analysis environment. Create a virtual environment at `/home/user/venv` and install `pandas` and `scikit-learn`.
2. Modify `/home/user/etl_pipeline.py` to fix the bug. You must handle the missing data properly: drop any rows from the merged DataFrame where the `label` is missing, and ensure the `label` column is strictly cast back to integers (not floats) before model training.
3. Run the pipeline. The script is designed to track the experiment by outputting the model's training accuracy to `/home/user/metrics.json` in the format `{"accuracy": <float>}`.

Ensure that after your fixes, running `python /home/user/etl_pipeline.py` successfully creates `/home/user/metrics.json` with the correct accuracy metric.