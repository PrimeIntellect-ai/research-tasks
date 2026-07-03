You are a data scientist tasked with fixing an ETL pipeline written in Go. 

In `/home/user/pipeline`, there is a SQLite database `data.db` containing a table `measurements` with the schema:
`id INTEGER, f1 REAL, f2 REAL, is_train INTEGER`

There is also a Go program `/home/user/pipeline/etl.go` that reads this database, standardizes (Z-score normalizes) the features `f1` and `f2`, and outputs the results to `train_clean.csv` and `test_clean.csv`. 

However, the current implementation has a critical data science bug: **Data Leakage**. The program computes the mean and sample standard deviation of the features using the *entire* dataset (both `is_train=1` and `is_train=0`). 

Your task:
1. Initialize a Go module in `/home/user/pipeline` and install any necessary dependencies.
2. Fix the bug in `etl.go`. You must compute the mean and sample standard deviation for `f1` and `f2` using **ONLY** the training set (`is_train=1`).
3. Apply these training-set parameters to standardize both the training set and the test set. (Use sample standard deviation).
4. Run the fixed Go program. It should generate `/home/user/pipeline/train_clean.csv` and `/home/user/pipeline/test_clean.csv`. 

The output CSVs must have the header `id,f1,f2` and the float values must be formatted to exactly 4 decimal places.