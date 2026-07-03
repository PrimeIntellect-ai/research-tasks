You are tasked with debugging a regression in a financial data parsing tool. The repository is located at `/home/user/financial_parser`.

Recently, a regression was introduced somewhere in the last 200 commits. At the known good tag `v1.0`, the script correctly parses the dataset and calculates the total without any precision loss. At the current `HEAD`, running the script crashes due to an edge case in format parsing.

Your objectives:
1. Use `git bisect` to find the exact commit that introduced the crash. The script to run is `python parser.py records.txt`.
2. Write the full 40-character SHA-1 hash of the offending commit to `/home/user/bad_commit_hash.txt`.
3. Analyze the stack trace and the code changes in the bad commit. The bug was introduced as an improper fix for format parsing, which not only causes a crash on some lines (edge cases with spaces/delimiters) but also leads to precision loss if bypassed.
4. Fix `parser.py` at `HEAD` so that it successfully parses `records.txt` and correctly calculates the exact floating-point total without any precision loss. 
5. Run the fixed script and redirect its standard output to `/home/user/final_output.txt`.

Constraints:
- Do not modify `records.txt`.
- Make sure `/home/user/bad_commit_hash.txt` contains *only* the 40-character commit hash.
- Ensure your final fix in `parser.py` is robust against the parsing edge-cases present in `records.txt`.