You are a data scientist cleaning a dataset of text embeddings. You have a bash script that is supposed to filter out outlier embeddings by calculating their L2 norm (distance from the origin) and dropping those that exceed a certain threshold. However, due to a numerical configuration issue, the script is currently failing to process the floating-point values correctly, effectively producing invalid or blank outputs.

Your tasks are to:
1. **Fix the Configuration Bug**: Examine and fix `/home/user/filter_outliers.sh`. The script relies on `awk` to compute the L2 norm of pre-computed embeddings. Due to a misconfigured environment variable inside the script, it misinterprets the decimal points in `/home/user/embeddings.csv`. Modify the script so it correctly computes the L2 norm and outputs the `ID`s of the embeddings whose L2 norm is strictly less than the provided threshold.
2. **Hyperparameter Tuning**: You have a validation set of labels in `/home/user/val_labels.csv` (Format: `ID,is_outlier`, where `1` means outlier and `0` means standard/keep). Using pure bash, write a loop to test the following thresholds: `0.5, 1.0, 1.5, 2.0, 2.5, 3.0`. For each threshold, use `filter_outliers.sh` to get the list of kept IDs, and compare it against `val_labels.csv` to calculate the accuracy (number of correctly classified samples, both outliers and non-outliers, divided by total validation samples).
3. **Clean the Dataset**: 
   - Write the single best threshold value you discovered (the one with the highest accuracy) into `/home/user/best_threshold.txt`. If there is a tie, pick the lowest threshold.
   - Run the fixed script with this optimal threshold on `/home/user/embeddings.csv`.
   - Save the resulting list of cleaned `ID`s (one ID per line) to `/home/user/cleaned_dataset.csv`.

Files provided:
- `/home/user/embeddings.csv`: Contains 5-dimensional embeddings. Format: `ID,v1,v2,v3,v4,v5`
- `/home/user/val_labels.csv`: Ground truth for the first 10 IDs. Format: `ID,is_outlier`
- `/home/user/filter_outliers.sh`: The buggy filtering script. Usage: `./filter_outliers.sh <threshold>`

All your operations must be done in Bash. Do not write Python or C++ scripts.