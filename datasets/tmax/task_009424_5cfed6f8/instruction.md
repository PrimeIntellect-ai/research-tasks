You are a Data Engineer building a lightweight ETL and anomaly detection pipeline using purely shell utilities (Bash, awk, sed, coreutils). You cannot use Python, R, or any other higher-level languages.

You have a dataset located at `/home/user/sensor_data.csv`. It contains a header row and 60 rows of data. 
The columns are: `id,sensor_1,sensor_2,sensor_3,is_anomaly`.

Your objective is to write and execute a Bash script named `/home/user/pipeline.sh` that performs the following steps:

1. **Numerical Configuration & Setup**: 
   Ensure your script strictly uses the `C` locale for numeric operations to avoid comma/period decimal confusion. 

2. **Dimensionality Reduction (Variance Thresholding)**:
   Process `sensor_data.csv` to drop any sensor columns (`sensor_1`, `sensor_2`, `sensor_3`) that have zero variance (i.e., the maximum value equals the minimum value across all data rows). Keep the `id` and `is_anomaly` columns, plus any sensor columns that vary. Save this intermediate dataset as `/home/user/reduced_data.csv`.

3. **Cross-Validation & Hyperparameter Tuning**:
   Implement a 3-fold cross-validation routine from scratch in Bash/awk.
   - Split the 60 data rows into 3 contiguous folds (Fold 1: rows 1-20, Fold 2: rows 21-40, Fold 3: rows 41-60). 
   - You are tuning a simple threshold-based anomaly detection model on the remaining sensor column. The model logic is: `if sensor_value > THRESHOLD then prediction = 1 else prediction = 0`.
   - Your hyperparameter grid for `THRESHOLD` is: `30, 40, 42, 50`.
   - For each fold acting as the validation set (with the other two as training, though for a fixed threshold, you just evaluate on the validation set), calculate the accuracy of the threshold.
   - Calculate the average validation accuracy across all 3 folds for each threshold.

4. **Reporting**:
   Identify the `THRESHOLD` that yields the highest average cross-validation accuracy. 
   Write the result to `/home/user/best_model.txt` exactly in this format:
   `Best Threshold: <THRESHOLD_VALUE>`

Constraints:
- Do not use Python, Perl, Ruby, or external compiled programs outside of standard POSIX utilities and GNU coreutils/awk.
- `/home/user/pipeline.sh` must be executable and run successfully.