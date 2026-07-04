I am a researcher organizing a large batch of sensor datasets. I need you to set up a minimal machine learning environment, train an anomaly detection model on a baseline dataset, and use it to sort new incoming datasets into "normal" and "anomalies" directories.

Here are the exact steps I need you to follow:

1. **Environment Setup:** 
   Create a Python virtual environment at `/home/user/ml_env`.
   Activate it and install `pandas` and `scikit-learn`.

2. **Model Training:**
   Write a Python script at `/home/user/organize_datasets.py`. In this script, load the baseline dataset located at `/home/user/data/baseline.csv`. The dataset has two columns: `sensor_x` and `sensor_y`.
   Train an `IsolationForest` from `scikit-learn` on this baseline data. You must initialize it with `random_state=42` and leave all other parameters at their defaults.

3. **Evaluation and Organization:**
   The directory `/home/user/data/samples/` contains several CSV files with the same structure as the baseline.
   For each CSV file in this directory:
   - Use the trained `IsolationForest`'s `decision_function` to compute the anomaly scores for all rows in the file.
   - Calculate the mean of these scores.
   - If the mean score is **strictly less than 0**, the dataset is considered anomalous.
   - If anomalous, move the file to `/home/user/data/anomalies/`. If normal, move it to `/home/user/data/normal/`. (Create these directories if they don't exist).

4. **Reporting:**
   Generate a text file at `/home/user/summary.txt` that lists each evaluated sample file's name and its mean anomaly score. Format each line exactly like this:
   `filename.csv: <mean_score>`
   (Round the mean score to exactly 3 decimal places, e.g., `sample_1.csv: 0.123`).
   Sort the lines in `summary.txt` alphabetically by filename.

Run your script to complete the organization.