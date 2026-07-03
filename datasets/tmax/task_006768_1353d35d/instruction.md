You are the on-call engineer for a financial analytics firm. It's 3:00 AM, and you've just been paged because the nightly batch risk calculation job crashed. The container stopped unexpectedly, halting the entire pipeline. 

Here is what we know:
1. The batch processing script ran from `/home/user/app/batch_processor.py` and crashed during execution.
2. The system generated a partial memory dump at `/home/user/crash_reports/memdump.dat` right before the container exited.
3. The application calculates a proprietary "Risk Index" for various transaction portfolios based on lists of V-values and W-values. 
4. The mathematical definition of the Risk Index ($R$) is:
   $$R = \frac{\sum_{i=1}^{n} (V_i \times W_i)}{\sqrt{\left| \sum_{i=1}^{n} V_i^2 - \sum_{i=1}^{n} W_i^2 \right|}}$$
   Notice the absolute value in the denominator!

Your tasks are to:
1. **Analyze the Memory Dump:** Extract the ID of the specific transaction that caused the crash from `/home/user/crash_reports/memdump.dat`. The application always writes `"CURRENT_PROCESSING_TXN: <TXN_ID>"` to memory right before processing a transaction. Transaction IDs are formatted like `TXN-XXXX-0000`.
2. **Correct the Formula:** Inspect `/home/user/app/risk_calc.py` and fix the implementation of the `calculate_risk(v_list, w_list)` function so that it correctly matches the mathematical specification and prevents crashes.
3. **Calculate the Missing Value:** Find the data for the crashed transaction inside `/home/user/app/transactions.json` and calculate its correct Risk Index using your fixed formula.
4. **Generate the Fix Report:** Create a file exactly at `/home/user/fix_report.txt` with exactly two lines:
   - Line 1: The ID of the crashed transaction.
   - Line 2: The mathematically correct Risk Index for that transaction, rounded to exactly 4 decimal places (e.g., `12.3456`).

You must resolve this issue entirely using the terminal. Do not modify `transactions.json`. You may install necessary Python packages if you need them to debug or test.