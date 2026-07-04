You are a machine learning engineer tasked with preparing a training pipeline. We have a dataset at `/home/user/data.csv` containing 1000 rows. The first 10 columns are numerical features, and the last column is a binary label (0 or 1). The file has no header.

A previous engineer wrote a pipeline that suffered from data leakage because they applied Principal Component Analysis (PCA) to the entire dataset before splitting it into training and testing sets. 

Your task is to build a corrected, reproducible pipeline orchestrated primarily through Bash.

Create an executable Bash script at `/home/user/pipeline.sh` that performs the following steps in order:

1. **Environment Configuration**: Export the environment variables `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1` to ensure reproducible numerical operations.
2. **Data Splitting**: Use Bash commands (e.g., `head` and `tail`) to split `/home/user/data.csv` into `/home/user/train.csv` (the first 800 rows) and `/home/user/test.csv` (the remaining 200 rows).
3. **Dimensionality Reduction (Python)**: Write and execute a Python script `/home/user/pca.py` that takes four command-line arguments: train input, test input, train output, and test output.
   - It should read the train and test CSV files.
   - Separate the features (first 10 columns) from the labels (last column).
   - Fit a PCA model (`n_components=5`, `svd_solver='full'`) **only on the training features**.
   - Transform both the training and testing features using this fitted PCA model.
   - Save the transformed features along with their original labels to the specified train output and test output CSV files (no headers, comma-separated).
   - Run this script from your Bash pipeline to produce `/home/user/train_pca.csv` and `/home/user/test_pca.csv`.
4. **Model Training and Prediction (Python)**: Write and execute a Python script `/home/user/train.py` that takes three command-line arguments: train input, test input, and predictions output.
   - It should read the PCA-transformed train and test CSV files.
   - Train a Logistic Regression model (`random_state=42`) on the training data.
   - Predict the labels for the test data.
   - Save **only** the predicted labels (one per line, no headers) to the predictions output file.
   - Run this script from your Bash pipeline to produce `/home/user/predictions.txt`.
5. **Evaluation (Bash)**: Using Bash commands (e.g., `paste`, `awk`), compare the predictions in `/home/user/predictions.txt` with the true labels from the last column of `/home/user/test.csv`. Calculate the accuracy (number of correct predictions divided by total test samples) and write this single floating-point number to `/home/user/accuracy.txt`.

Ensure your `/home/user/pipeline.sh` is executable and successfully runs the entire process from start to finish when executed.