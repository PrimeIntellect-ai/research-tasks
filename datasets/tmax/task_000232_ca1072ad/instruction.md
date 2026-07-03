You are helping a data science researcher organize and debug their multi-source C++ inference pipeline. 

The researcher has written a script, `/home/user/pipeline.cpp`, which reads two datasets (`/home/user/dataset_A.csv` and `/home/user/dataset_B.csv`), joins them on the `id` column, performs a mean-centering feature transformation on a specific feature (`val1`), splits the data into a training set (first 80 rows) and test set (last 20 rows), and runs a simple linear inference model.

However, there is a severe data leakage bug: the feature `val1` is being mean-centered using the global mean of the *entire* joined dataset before the train/test split. This is artificially inflating inference performance by leaking test set distribution statistics into the training phase.

Your task is to:
1. Compile and run the original `pipeline.cpp` to generate the baseline predictions. Save its output to `/home/user/predictions_buggy.csv`.
2. Modify `/home/user/pipeline.cpp` to fix the data leak. The mean used to center `val1` must be calculated **only** using the training set (the first 80 rows of the joined data). This training mean should then be subtracted from `val1` for *both* the training and test sets.
3. Compile and run the fixed pipeline. Save its output to `/home/user/predictions_fixed.csv`.
4. Perform a paired t-test between the test set predictions in `predictions_buggy.csv` and `predictions_fixed.csv` to statistically quantify the impact of the data leak.
5. Create an experiment tracking file at `/home/user/experiment_log.json` with the exact following keys and your calculated numerical values (rounded to 4 decimal places):
   - `"train_mean_val1"`: The mean of `val1` from the training set (used for the fixed normalization).
   - `"buggy_test_mean"`: The mean of the predictions on the test set from `predictions_buggy.csv`.
   - `"fixed_test_mean"`: The mean of the predictions on the test set from `predictions_fixed.csv`.
   - `"p_value"`: The p-value from the paired t-test between the buggy and fixed test set predictions.

Ensure your modified C++ code still outputs the test set predictions in the format `id,prediction`.