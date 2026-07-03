You are tasked with finding and fixing a regression in a data processing pipeline. 

A Git repository located at `/home/user/project` contains a Python script named `processor.py`. This script reads a binary file, applies a mathematical transformation to each byte, and outputs a base64-encoded string representing the processed data. 

Recently, a bug was introduced in the transformation formula during a large refactoring effort spanning 200 commits. The first commit in the repository contains the correct implementation, but the latest commit (`HEAD` on the `main` branch) produces incorrect output.

Your tasks:
1. Use Git bisection to identify the exact commit that introduced the bug. Write the full, 40-character commit hash of the bad commit to `/home/user/bad_commit.txt`.
2. Examine the changes in that commit to understand what went wrong (a formula implementation error).
3. Fix the bug in `processor.py` on the latest commit of the `main` branch.
4. Run the fixed `processor.py` on the input file `/home/user/data.bin` and save the exact output to `/home/user/fixed_output.txt`. (Do not include any extra newlines or text in this file other than what the script outputs).

Note: You can run the script from the first commit on `/home/user/data.bin` to determine the expected correct output.