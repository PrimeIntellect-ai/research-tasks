You are helping a data scientist debug an ETL pipeline script that is currently experiencing a critical data leakage issue. 

There is a Python script located at `/home/user/clean_data.py` and a dataset at `/home/user/dataset.csv`. The script is supposed to scale the features and split the data into training and testing sets. However, the current implementation scales the entire dataset before splitting, causing information from the test set to leak into the training set.

Your task is to fix `/home/user/clean_data.py` so that:
1. The data is split into train and test sets FIRST.
2. The `StandardScaler` is fitted ONLY on the training set.
3. Both the training and test sets are then transformed using this fitted scaler.
4. The script must continue to output the mean of the first feature of the scaled test set to `/home/user/metrics.json`.

Do not change the `test_size=0.2` or `random_state=42` parameters in `train_test_split`.
Once you have modified the script, run it to generate the correct `/home/user/metrics.json` file.