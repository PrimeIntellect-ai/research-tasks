You are a researcher organizing experiment datasets. You have several CSV files containing numerical logs from recent runs, and you need to perform a statistical check on their numerical accuracy relative to a baseline expectation. 

In `/home/user/datasets/`, there are three CSV files: `exp1.csv`, `exp2.csv`, and `exp3.csv`. Each file contains a single column of float64 values (representing measurement errors).

You also have an incomplete Go program at `/home/user/check_accuracy.go`. This program is supposed to read a dataset, compute its sample mean and standard deviation, and perform a hypothesis test to check if the theoretical mean of `10.0` falls within the 95% Confidence Interval (CI) of the dataset.

Your task is to:
1. Complete `/home/user/check_accuracy.go`. You need to calculate the 95% Confidence Interval. Use the formula:
   `lower_bound = mean - 1.96 * (std_dev / sqrt(N))`
   `upper_bound = mean + 1.96 * (std_dev / sqrt(N))`
   Where `N` is the number of data points.
   The program must print exactly `PASS` if `10.0` is strictly inside the interval `[lower_bound, upper_bound]`, and `FAIL` otherwise.

2. Run your completed Go program on all three CSV files in the `/home/user/datasets/` directory.

3. Track the results by creating a report file at `/home/user/report.txt`. The file should contain one line per dataset in the exact format:
   `<filename>: <RESULT>`
   (For example: `exp1.csv: PASS`)

Sort the output in `/home/user/report.txt` alphabetically by filename.