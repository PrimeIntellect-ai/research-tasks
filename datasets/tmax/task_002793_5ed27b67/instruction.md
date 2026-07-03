You are an ML Engineer tasked with building a high-performance, reproducible data preparation and baseline evaluation pipeline using Go. 

You have been given a raw dataset at `/home/user/dataset.csv`. This dataset contains server telemetry data with the following columns: `timestamp`, `server_role`, `cpu_usage`, `memory_usage`, `crashed`.

Your objective is to write a Go program (`/home/user/pipeline.go`) that performs tabular data transformation, feature engineering, a deterministic train/test split, and a baseline algorithmic evaluation.

Requirements for your Go program:

1. **Feature Engineering**:
   - Read `/home/user/dataset.csv`.
   - **One-Hot Encoding**: Convert `server_role` (which contains values `web`, `db`, `cache`) into three binary columns: `role_web`, `role_db`, `role_cache`.
   - **Min-Max Scaling**: Scale the `memory_usage` column to a 0.0 - 1.0 range, calculated across the entire dataset. (Formula: `(x - min) / (max - min)`).
   - **Rolling Average**: Calculate a 3-row rolling average for `cpu_usage`. For row $i$, the `cpu_rolling_avg` should be the average of `cpu_usage` at $i-2$, $i-1$, and $i$. For the first two rows (where $i-2$ or $i-1$ is out of bounds), use only the available rows (e.g., row 0 is just row 0's value; row 1 is the average of row 0 and row 1). Assume the dataset is strictly ordered by `timestamp` as provided.

2. **Deterministic Split**:
   - For pipeline reproducibility, split the transformed data into a training set and a testing set.
   - For each row, calculate the MD5 hash of its string `timestamp`. Take the first byte of the MD5 hash.
   - If `(first_byte % 10) < 8`, assign the row to the training set. Otherwise, assign it to the testing set.
   - Save the engineered datasets as `/home/user/train.csv` and `/home/user/test.csv`. The columns must be in this exact order: `timestamp`, `role_web`, `role_db`, `role_cache`, `cpu_rolling_avg`, `memory_scaled`, `crashed`. Output floats to 4 decimal places.

3. **Baseline Model Evaluation**:
   - Write an algorithmic baseline model that predicts `crashed = 1` if `cpu_rolling_avg > 80.0000` OR `memory_scaled > 0.8500`. Otherwise, it predicts `0`.
   - Evaluate this baseline exclusively on the testing set (`/home/user/test.csv`).
   - Calculate the accuracy (correct predictions / total test instances).
   - Write the final accuracy to `/home/user/model_eval.txt` in the exact format: `Accuracy: 0.XXXX` (rounded to 4 decimal places).

Run your Go program to generate `train.csv`, `test.csv`, and `model_eval.txt`.