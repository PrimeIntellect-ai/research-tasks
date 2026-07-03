You are an IT support technician responding to an escalated ticket (INC-8492). 

**Ticket Description:**
"Our nightly fraud detection script (`/home/user/fraud_check.py`) is failing. It calculates the standard deviation of daily transaction amounts to look for unusual consistency. 
First, the script crashes with a `ValueError: math domain error` for some high-balance corporate accounts. The engineering team mentioned this is likely due to 'catastrophic cancellation' and numerical instability in the naive variance formula used in the script.
Second, the script is only evaluating accounts with an 'active' status. It also needs to evaluate accounts with a 'suspended' status, but should still ignore 'closed' accounts."

**Your Objectives:**
1. Fix the SQL query in `/home/user/fraud_check.py` so it retrieves both 'active' and 'suspended' accounts from `/home/user/transactions.db`.
2. Fix the numerical instability in the standard deviation calculation. Replace the naive implementation with a numerically stable formula (e.g., using Python's built-in robust libraries or a two-pass algorithm).
3. Run the script. The script is configured to write its output to `/home/user/flagged_accounts.txt`. 

**Output Requirements:**
- The final output must be located at `/home/user/flagged_accounts.txt`.
- Each line should be formatted as `account_id,standard_deviation` where the standard deviation is rounded to exactly 4 decimal places.

Fix the code and ensure the output file is generated correctly.