You are a data analyst verifying the reproducibility of a legacy data pipeline. Two pipeline runs have generated two output files: `/home/user/run1.csv` and `/home/user/run2.csv`. Both files have a header `id,value` and contain 100 rows of numerical data. 

To test the numerical accuracy and pipeline reproducibility, you need to calculate the Mean Absolute Error (MAE) between the `value` columns of the two files for matching `id`s. 

Using only standard Linux command-line tools (like `awk`, `join`, `sort`, `bc`), perform the following steps:
1. Join the two files by the `id` column.
2. Calculate the absolute difference between the `value` in run1 and run2 for each `id`.
3. Compute the mean of these absolute differences (the MAE).
4. If the MAE is strictly less than 0.05, the pipeline is reproducible. Otherwise, it is not.
5. Create a file named `/home/user/report.txt`. The file should contain exactly one line with the format:
`[STATUS] MAE: [VALUE]`
where `[STATUS]` is either `PASS` (if MAE < 0.05) or `FAIL` (if MAE >= 0.05), and `[VALUE]` is the MAE rounded to exactly 4 decimal places.

Example output format in `/home/user/report.txt`:
`PASS MAE: 0.0125` or `FAIL MAE: 0.0833`