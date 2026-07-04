You are an IT support technician investigating a bug report for a billing script. The script is supposed to aggregate transaction amounts into an array of daily totals for a given date range (inclusive of both start and end dates). However, it crashes with an `IndexError` on certain inputs.

You have been provided with:
1. The script: `/home/user/billing_processor.py`
2. A large JSON file of transactions that causes the crash: `/home/user/large_transactions.json`

Your tasks:
1. **Delta Debugging / Minimization:** Before fixing the script, identify the exact transaction causing the crash. Create a new file `/home/user/minimized_transactions.json` containing a valid JSON array with ONLY the single transaction dictionary from `large_transactions.json` that triggers the `IndexError` when using the date range `2023-10-01` to `2023-10-31`.
2. **Bug Fix:** Identify and fix the boundary condition / off-by-one error in `/home/user/billing_processor.py` so that it correctly handles transactions on the end date of the range. The length of the returned array should accurately reflect the inclusive date range.
3. **Regression Test:** Create a regression test using `pytest` in the file `/home/user/test_billing.py`. Write a single test function named `test_end_date_inclusive()` that imports `calculate_daily_aggregates` from `billing_processor`, calls it with `start_date='2023-10-01'`, `end_date='2023-10-03'`, and a mock transactions array containing exactly one transaction on `'2023-10-03'` with an amount of `100`. Assert that the returned array is exactly `[0, 0, 100]`.

Please complete these steps. Ensure that your Python code is correct and that `pytest /home/user/test_billing.py` passes.