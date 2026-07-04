You are a data scientist working on a high-performance anomaly detection system for sensor data. The data is noisy and contains missing values. Your task is to build a hybrid Bash/C++ pipeline that cleans the data, runs an algorithmic anomaly detector, and performs a hyperparameter grid search.

**Step 1: Data Cleaning (ETL)**
A raw dataset is located at `/home/user/raw_data.csv`. It has a header `id,value,label`. Some of the `value` entries are corrupted and say `NaN` or `ERROR`.
Write a Bash script named `/home/user/clean.sh` that:
1. Reads `/home/user/raw_data.csv`.
2. Keeps the header intact.
3. Performs a "forward fill" for the `value` column: if a `value` is not a valid floating-point number (e.g., `NaN`, `ERROR`), replace it with the last seen valid numeric `value`.
4. Outputs the cleaned data to `/home/user/clean_data.csv`.
*(Assume the first data row always has a valid numeric value).*

**Step 2: Algorithmic C++ Detector**
Write a C++ program at `/home/user/detector.cpp` that takes two command-line arguments: `W` (an integer window size) and `T` (a double precision threshold).
The program must:
1. Read `/home/user/clean_data.csv` (skip the header).
2. For each row at index $i$ (where $i \ge W$, with $i=0$ being the first data row), compute the arithmetic mean of the `value`s of the *strictly preceding* `W` rows.
3. If the absolute difference between the current row's `value` and the computed mean is strictly greater than `T`, the program predicts an anomaly (1), otherwise (0).
4. Rows with index $i < W$ cannot be evaluated and should be ignored (neither predicted nor counted in metrics).
5. Compare the predictions to the true `label` column (which contains 1 for anomaly, 0 for normal) for the evaluated rows.
6. Calculate the F1 score of your predictions. (F1 = 2 * TP / (2 * TP + FP + FN)). If TP is 0, F1 is 0.0.
7. Print ONLY the F1 score to standard output, formatted to exactly 4 decimal places (e.g., `0.7500`). Use `double` precision for all calculations to ensure numerical accuracy.

**Step 3: Experiment Tracking & Hyperparameter Tuning**
Write a Bash script at `/home/user/tune.sh` that:
1. Compiles `/home/user/detector.cpp` into an executable named `/home/user/detector` using `g++ -O3`.
2. Iterates over window sizes `W` in `[2, 3, 4]`.
3. Iterates over thresholds `T` in `[1.5, 2.0, 2.5]`.
4. Runs the compiled detector for each combination of `W` and `T`.
5. Appends the results to `/home/user/grid_results.csv` in the format `W,T,F1` (e.g., `2,1.5,0.8000`).
6. The file `/home/user/grid_results.csv` must include a header `W,T,F1` as its first line.

Run your pipeline so that `/home/user/clean_data.csv` and `/home/user/grid_results.csv` are fully generated.