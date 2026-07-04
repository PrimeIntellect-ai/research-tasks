You are a data analyst tasked with fixing a machine learning pipeline that suffers from data leakage, and then building an evaluation script to assess the corrected model.

Currently, we have a text classification pipeline in `/home/user/model_pipeline.py` that predicts sentiment from product reviews (found in `/home/user/reviews.csv`). 

However, there's a serious flaw: the script performs tokenization and TF-IDF vectorization on the *entire* dataset before splitting it into training and testing sets. This causes data leakage from the test set into the training phase.

Your task consists of the following steps:

1. **Environment Setup**: 
   Create a Python virtual environment at `/home/user/venv`.
   Install the necessary packages: `scikit-learn==1.3.0` and `pandas==2.0.3`.

2. **Fix the Python Pipeline**: 
   Modify `/home/user/model_pipeline.py` to prevent data leakage. You must split the data *before* fitting the `TfidfVectorizer`. 
   Ensure:
   - You use `train_test_split` with `test_size=0.2` and `random_state=42`.
   - The vectorizer is `fit` *only* on the training data, and then used to `transform` both the train and test data.
   - The Logistic Regression model uses `random_state=42`.
   - The script saves the test set predictions to `/home/user/predictions.csv` with exactly three columns: `id`, `predicted_sentiment`, and `true_sentiment`.

3. **Create a Shell Evaluation Script**: 
   Write a Bash script at `/home/user/evaluate.sh` (using tools like `awk` or `bash` built-ins, do NOT use Python for this step). 
   This script must:
   - Read `/home/user/predictions.csv`.
   - Calculate the overall accuracy (number of correct predictions divided by total predictions).
   - Output the result to `/home/user/metrics.txt` in the exact format: `Accuracy: 0.XXXX` (rounded or truncated to any precision, but must be the correct float value).

Make sure both the Python script and the Bash script execute without errors and produce the expected files.