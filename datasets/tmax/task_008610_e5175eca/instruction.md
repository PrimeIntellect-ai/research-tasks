**IT Support Ticket #4892**
**Subject:** Missing billing script and incorrect calculations
**Priority:** High

**Description:**
Hello Support,

One of our junior analysts accidentally ran an `rm` command and deleted our primary billing script located at `/home/user/scripts/calc_billing.py`. 

Fortunately, we know that a background `tail` process was actively monitoring this script when it was deleted, meaning the file descriptor should still be open and the file contents recoverable from memory/process space.

Before it was deleted, the script was producing incorrect totals due to two known algorithmic bugs:
1. **Boundary condition (Off-by-one):** The script skips the very first item in the data array during its loop.
2. **Formula implementation:** The cost calculation calculates the discount amount itself, rather than the final price after the discount. (i.e., it applies `cost = (base_price * qty) * discount_fraction` instead of multiplying by `(1 - discount_fraction)`).

**Your tasks:**
1. **Recover the file:** Inspect the background processes, recover the deleted file contents from the open file descriptor, and save it back to `/home/user/scripts/calc_billing.py`.
2. **Fix the bugs:** Edit the recovered Python script to fix both the off-by-one loop error and the incorrect discount formula.
3. **Run the script:** Execute the fixed script against the provided data file at `/home/user/data/january_usage.json`.
4. **Log the output:** Save the standard output of the corrected script exactly to `/home/user/billing_result.txt`.

Please complete these steps entirely from the terminal. The final output must be just the corrected total numerical value written to `billing_result.txt`.