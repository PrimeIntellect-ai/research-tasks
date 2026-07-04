You are a data engineer building a lightweight, high-performance ETL pipeline in C to process user interaction logs. The goal is to aggregate user features, perform dimensionality reduction via a fixed projection matrix, and validate the output.

Your workspace is `/home/user/etl_task/`. I have placed two files there:
1. `/home/user/etl_task/data.csv`: A raw log file containing multiple records per user. The columns are `UserID,F1,F2,F3,F4,F5`. Values are integers.
2. `/home/user/etl_task/matrix.csv`: A 5x2 random projection matrix (comma-separated floats).

Your task has two parts:

**Part 1: The ETL C Program**
Write a C program at `/home/user/etl_task/etl.c` that only uses standard C libraries. It must:
1. Read `data.csv` and aggregate the data: For each unique `UserID`, calculate the sum of each feature `F1` through `F5`.
2. Perform dimensionality reduction: Multiply the aggregated 1x5 feature vector for each user by the 5x2 projection matrix from `matrix.csv`. This reduces the 5 features to 2 projected features (`P1` and `P2`).
3. Sort the resulting data by `UserID` in ascending order.
4. Write the results to `/home/user/etl_task/reduced_data.csv`. The format must be exactly `UserID,P1,P2` where `P1` and `P2` are floats formatted to exactly two decimal places (e.g., `%.2f`). Include a header row: `UserID,P1,P2`.

Compile your C program to `/home/user/etl_task/etl` and execute it.

**Part 2: Model Output Validation**
Write a bash script at `/home/user/etl_task/validate.sh` that validates `reduced_data.csv`. The script should:
1. Verify that the file has exactly 3 columns.
2. Verify that there are no blank values or `NaN`s in the `P1` or `P2` columns.
3. If the file is perfectly valid, the script should print "VALID" to standard output and exit with code 0. Otherwise, print "INVALID" and exit with code 1.

Ensure you run your `etl` binary and that `reduced_data.csv` is generated successfully before finishing.