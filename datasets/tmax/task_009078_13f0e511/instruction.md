You are a data analyst tasked with building an automated data processing and machine learning pipeline. You have been provided with a raw transaction log file at `/home/user/raw_transactions.csv`.

Your goal is to build a pipeline using Bash and Python that extracts features, trains a prediction model, and logs the evaluation metrics.

Here are the specific requirements:

1. **Environment Setup**:
   - Create a Python virtual environment at `/home/user/venv`.
   - Install `pandas` and `scikit-learn` within this environment.

2. **Data Transformation (Bash/Awk)**:
   - Write a Bash script `/home/user/process_data.sh` that reads `/home/user/raw_transactions.csv`.
   - The input CSV has a header: `tx_id,user_id,amount,target`. (The `target` is 0 or 1, and is constant for any given `user_id`).
   - The script must aggregate the transactions per `user_id` and output a new CSV file at `/home/user/features.csv` with the following header: `user_id,total_amount,tx_count,avg_amount,target`.
   - Ensure the rows are sorted numerically by `user_id`.
   - Round `total_amount` and `avg_amount` to exactly 2 decimal places.

3. **Model Training (Python)**:
   - Write a Python script `/home/user/train.py` (which will be executed using the virtual environment you created) that reads `/home/user/features.csv`.
   - Define your feature matrix `X` using the columns `total_amount`, `tx_count`, and `avg_amount`. The target `y` is the `target` column.
   - Initialize a Logistic Regression model using `sklearn.linear_model.LogisticRegression(random_state=42, solver='lbfgs')`.
   - Fit the model on the *entire* dataset (do not perform train/test split).
   - Predict on the same dataset and calculate the accuracy score.
   - The script must write the accuracy score to `/home/user/metrics.txt` in exactly this format: `Accuracy: X.XXXX` (rounded to 4 decimal places).

4. **Pipeline Execution**:
   - Write a master pipeline script `/home/user/run_pipeline.sh` that activates the virtual environment, runs `process_data.sh`, and then runs `train.py`.
   - Execute your pipeline so that `/home/user/features.csv` and `/home/user/metrics.txt` are created.

Ensure all scripts have execute permissions where applicable, and run the pipeline to generate the final artifacts.