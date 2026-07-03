You are tasked with debugging a data processing regression in a local Git repository.

A Python-based transaction analyzer tool in `/home/user/tx_analyzer` connects to a local SQLite database to compute user balances. Recently, users have reported that their calculated balances are incorrect. The team suspects that a bug was introduced somewhere in the last 20 commits, likely related to how certain transaction types (e.g., refunds) are queried or transformed during processing.

Your objectives:
1. Navigate to `/home/user/tx_analyzer`.
2. Use git bisection (or manual checking) to identify the exact commit hash that introduced the regression. The very first commit in the repository is known to be GOOD. The latest commit (`HEAD`) is known to be BAD.
3. The script `analyzer.py` calculates the total balance for a given user ID. Use it to verify correctness. The correct logic should subtract "refund" amounts from "purchase" amounts.
4. Once you have identified the bad commit, return to the `main` branch, fix the bug in `analyzer.py`, and run the tool for user `U15`.
5. Create a file named `/home/user/solution.txt` with exactly two lines:
   - Line 1: The full Git commit hash of the *first bad commit* that introduced the bug.
   - Line 2: The correct computed balance for user `U15` after you have fixed the script on the `main` branch.

Ensure the final output file is precisely formatted as requested.