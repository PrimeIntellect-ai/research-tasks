You are an MLOps engineer taking over an old experiment. The previous engineer reported surprisingly good performance on a tabular dataset, but you suspect there is data leakage in their training pipeline—specifically, information from the test set is leaking into the training set during preprocessing.

Your task is to fix the pipeline, reproduce the predictions without the leak, and write a multi-language evaluation to compare the results.

Here is your workspace setup:
- `/home/user/experiment/data.csv`: The raw dataset (columns: `feature1`, `feature2`, `target`).
- `/home/user/experiment/train.py`: The original Python training script. It splits the data 80/20 (no shuffling), scales the features, trains a Linear Regression model, and outputs predictions to `/home/user/experiment/leaky_predictions.csv`.

**Step 1: Fix the Data Leak**
Analyze `/home/user/experiment/train.py`. Identify the data leakage related to feature scaling. Create a new file `/home/user/experiment/fixed_train.py` that corrects this leak. 
- You must keep the same model (`LinearRegression`), the same train/test split size (80/20, `shuffle=False`), and the same scaler class.
- Ensure the scaler is only fitted on the training data.
- The fixed script must output the test set predictions to `/home/user/experiment/fixed_predictions.csv` (one prediction per line, no header).

**Step 2: Compare Metrics using Bash/Awk**
Write a shell script at `/home/user/experiment/compare.sh` that calculates the Mean Absolute Error (MAE) for both the leaky and fixed models.
- The script must use `awk` (or pure `bash` math) to read the true target values of the test set from `data.csv`, the leaky predictions from `leaky_predictions.csv`, and the fixed predictions from `fixed_predictions.csv`.
- DO NOT use Python for this step; it must be done via standard Unix text processing utilities (`awk`, `bash`, `tail`, `paste`, etc.).
- The script should output the results to `/home/user/experiment/metrics.txt` in exactly this format (rounded to 2 decimal places):
  ```
  Leaky MAE: <value>
  Fixed MAE: <value>
  ```

Run your scripts to generate `fixed_predictions.csv` and `metrics.txt`.