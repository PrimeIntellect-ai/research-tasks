You are an operations engineer triaging an ongoing billing incident. The billing aggregation pipeline is producing incorrect totals, leading to significant under-billing. 

A scheduled job runs `/home/user/aggregate_billing.py`, which parses transaction logs from `/home/user/billing_logs.txt` and calculates the total billed amount.

Upon initial investigation, two issues have been identified:
1. **Format parsing edge-cases:** The log values occasionally include commas in the numbers (e.g., `1,000.50`), empty strings (`""`), or invalid indicators (`"N/A"`). The current parsing logic silently swallows errors on these lines, treating their amount as `0.0`, skipping legitimate high-value transactions.
2. **Floating-point precision loss:** The script currently uses standard Python `float` for accumulation. Operations on these floats are introducing tiny precision errors (e.g., `0.1 + 0.2` resulting in `0.30000000000000004`), which triggers downstream reconciliation failures.

Your task is to:
1. Fix `/home/user/aggregate_billing.py` so that it handles amounts with commas correctly. Missing or non-numeric values (like `"N/A"` or `""`) should still safely evaluate to `0.0`.
2. Replace the `float` accumulation logic with exact decimal arithmetic (using Python's `decimal` module).
3. Create a regression test file at `/home/user/test_billing.py` that imports your fixed aggregation function, feeds it a synthetic list of test lines (covering commas, valid floats, `"N/A"`, and `""`), and asserts that the exact correct `Decimal` total is returned.
4. Run your fixed script on the `/home/user/billing_logs.txt` file and write the final computed total to `/home/user/final_total.txt` (the file should contain only the final number, e.g., `1050.25`).

Ensure your changes in `aggregate_billing.py` do not change the function signatures, only the internal logic.