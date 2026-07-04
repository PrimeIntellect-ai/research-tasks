You have inherited a data processing pipeline for a financial aggregation system. At the core of this pipeline is a proprietary, compiled command-line tool located at `/app/financial_aggregator`. It takes a CSV file containing transaction records as a positional argument, calculates "Impact Scores" for each row based on an internal formula, and prints the total aggregated sum. 

Recently, the operations team reported that the aggregator occasionally produces wildly incorrect, negative total aggregates. They isolated a large batch of data that reproduces this issue, saved at `/home/user/incidents/batch_99.csv`.

Because `/app/financial_aggregator` is a stripped binary, debugging it directly is difficult. However, you have access to the legacy source code repository at `/home/user/aggregator_src`. The binary is an optimized, compiled version of a specific commit in this repository. Somewhere in the commit history, an "optimization" introduced a signed integer overflow bug.

Your tasks:
1. **Delta Debugging**: Analyze `/home/user/incidents/batch_99.csv` against the `/app/financial_aggregator` binary to isolate the specific records causing the incorrect negative totals.
2. **Git Bisection**: Bisect the repository at `/home/user/aggregator_src` to find the exact commit that introduced the regression. Use the commit diff to understand the internal formula and the exact integer limits causing the overflow.
3. **Data Sanitizer Implementation**: Based on your findings, implement a sanitizer script at `/home/user/sanitizer.sh` (or `.py`). 
   - Your script must read a CSV stream from standard input (`stdin`) and write to standard output (`stdout`).
   - It must perfectly preserve all safe records (unchanged, maintaining order).
   - It must silently drop any record that would trigger the integer overflow in the aggregator's formula.

The CSV format is: `TRANSACTION_ID,USER_ID,AMOUNT,MULTIPLIER`

An automated test suite will evaluate your script against a hidden set of clean and malicious records to ensure it perfectly filters out overflow-triggering data without falsely dropping valid transactions.