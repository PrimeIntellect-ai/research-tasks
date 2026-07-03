Hi, I'm a researcher organizing some datasets. We have an old compiled data-processing pipeline step that cleans up missing values and finds the most similar records in a batch of data. Unfortunately, the original source code was lost, and we suspect it has a data leakage issue (it seems to compute imputation statistics across the entire batch instead of just the training split). 

I need you to write a Python script that perfectly replicates the behavior of this binary so we can analyze the leak and eventually fix it.

The old stripped binary is located at `/app/dataset_cleaner`. 
It reads a CSV of numerical data (with no header) from standard input. Some values are represented as the string `NaN`. 
It prints out the nearest neighbor for each row to standard output.

Your task:
1. Figure out exactly how `/app/dataset_cleaner` handles missing values, outliers, and computes similarity by running test inputs through it. (You may need to install standard data science packages like `numpy`, `pandas`, or `scikit-learn` via pip to build your replication).
2. Write a Python script at `/home/user/replicate.py` that reads the same CSV format from `sys.stdin` and outputs the exact same text format to `sys.stdout`.
3. Your script must be BIT-EXACT equivalent to the binary for any valid CSV input (e.g., handles the exact same imputation logic, distance metric, and tie-breaking behavior).

Please ensure your script can be invoked directly as `python3 /home/user/replicate.py`.