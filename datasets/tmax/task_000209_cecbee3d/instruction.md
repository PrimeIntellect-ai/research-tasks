You are a data analyst working on a text classification project. You need to build a simple machine learning pipeline and prove that it is fully reproducible.

You have a dataset located at `/home/user/data.csv` containing two columns: `review` (text) and `sentiment` (integer, 0 or 1).

Your task is to write two Python scripts:

1. **The Pipeline Script (`/home/user/evaluate_model.py`)**:
   Write a Python script that performs the following steps:
   - Loads the dataset `/home/user/data.csv` using pandas.
   - Tokenizes the `review` column using `sklearn.feature_extraction.text.CountVectorizer`.
   - Splits the data into training and testing sets using `sklearn.model_selection.train_test_split`. Use a test size of 0.25 and set `random_state=42`.
   - Trains a `sklearn.linear_model.LogisticRegression` model on the training data. Set `random_state=42` for the model as well.
   - Evaluates the model on the testing data by calculating the accuracy score.
   - Writes only the accuracy score, rounded to exactly four decimal places (e.g., `0.8150`), to a file named `/home/user/accuracy.txt`.

2. **The Reproducibility Test Script (`/home/user/test_pipeline.py`)**:
   Write a test script that validates the reproducibility of your pipeline. The script must:
   - Execute `/home/user/evaluate_model.py` 5 separate times programmatically (e.g., using `subprocess` or by importing the main function, though `subprocess` is recommended to ensure clean state).
   - After each run, read the contents of `/home/user/accuracy.txt`.
   - Verify that all 5 runs produced the exact same accuracy value.
   - If the outputs are perfectly reproducible, create an empty file named `/home/user/test_pass.log`.

Execute your test script to generate the final logs and output files.