You are a machine learning engineer preparing a small pipeline to analyze system logs. 

You have been provided with a dataset of system logs located at `/home/user/logs.csv`. The CSV has three columns: `id`, `label`, and `text`.

Your task is to build a minimal ETL and training pipeline by creating two files:
1. A Python script named `/home/user/train_model.py` that performs the following:
   - Reads `/home/user/logs.csv`.
   - Transforms the `text` column into a TF-IDF matrix using `sklearn.feature_extraction.text.TfidfVectorizer` with default parameters.
   - Calculates the numerical dot product (which represents cosine similarity for L2-normalized vectors) between the TF-IDF vector of the first document (row index 0) and the second document (row index 1). Save this single float value, rounded to 4 decimal places, to `/home/user/sim.txt`.
   - Trains a `sklearn.linear_model.LogisticRegression` model with `random_state=42` and default parameters, using the TF-IDF matrix as the features (X) and the `label` column as the target (y).
   - Evaluates the model's accuracy on the same training dataset. Save the accuracy, rounded to 4 decimal places, to `/home/user/metrics.txt`.

2. A Bash script named `/home/user/run.sh` that:
   - Ensures `pandas` and `scikit-learn` are installed via `pip`.
   - Executes the `/home/user/train_model.py` script.

Make sure `/home/user/run.sh` is executable and run it to produce the final output files (`sim.txt` and `metrics.txt`).