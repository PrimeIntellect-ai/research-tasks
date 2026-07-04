You are a data scientist tasked with cleaning a dataset and performing hyperparameter tuning for a simple anomaly detection model. However, you are working on a restricted server where Python, R, and other high-level languages have been uninstalled. You must rely entirely on standard Linux command-line tools (like `bash`, `awk`, `sed`, `grep`, `sort`, etc.) to complete this task.

You have a dataset located at `/home/user/sensor_data.csv` with the following columns:
`id,timestamp,sensor_value,is_anomaly`

Your goal is to build a simple threshold-based classifier: if `sensor_value >= T`, predict `1` (anomaly), else `0`. You need to find the best threshold `T` using 3-fold cross-validation.

Perform the following steps using shell commands:
1. **Data Cleaning**: 
   - Skip the header row.
   - Remove any rows where `sensor_value` is empty, exactly the string `NA`, or strictly less than `0`.
2. **Fold Assignment**:
   - Sequentially assign the cleaned rows to folds `0`, `1`, and `2`. 
   - The 1st cleaned row belongs to fold 0, the 2nd to fold 1, the 3rd to fold 2, the 4th to fold 0, and so on.
3. **Cross-Validation & Hyperparameter Tuning**:
   - Test the following candidate thresholds `T`: `10, 20, 30, 40, 50, 60, 70, 80, 90, 100`.
   - For each threshold `T` and for each fold `i` in `{0, 1, 2}`:
     - Treat fold `i` as the validation set.
     - For every row in fold `i`, predict `1` if `sensor_value >= T`, else `0`.
     - Calculate the validation accuracy for fold `i`: `(number of correct predictions in fold i) / (total rows in fold i)`.
   - Calculate the average cross-validation accuracy for threshold `T` by averaging the 3 validation fold accuracies.
4. **Model Selection**:
   - Identify the threshold `T` that produces the highest average cross-validation accuracy. 
   - If there is a tie for the highest accuracy, choose the *lowest* threshold `T` among the tied values.
5. **Reporting**:
   - Write the best threshold and its corresponding average CV accuracy to `/home/user/best_model.csv` in the exact format: `T,accuracy`
   - Format the accuracy to exactly 4 decimal places (e.g., `40,0.8333`).

Do not install any external packages. Use the provided shell tools to complete the task.