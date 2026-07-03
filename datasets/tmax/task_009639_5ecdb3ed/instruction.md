You are tasked with debugging a regression in a custom PRNG (Pseudo-Random Number Generator) library written in Python.

A repository is located at `/home/user/prng_repo`. It contains a script named `prng.py`. Recently, a developer noticed that the generated sequences no longer match the expected legacy system outputs, which historically simulated 31-bit signed integer behavior. 

There are exactly 200 commits in this repository's `main` branch. 
* The first commit (tagged `v1.0`) is known to be GOOD. At `v1.0`, running `python3 -c "import prng; print(prng.generate(42, 3))"` outputs `[1804289383, 846930886, 1681692777]`.
* The latest commit (`HEAD`) is known to be BAD. It produces a different sequence for the same seed.

Your tasks are:
1. Identify the exact commit that introduced the regression. You are highly encouraged to write a test script and use `git bisect run` to automate this across the 200 commits.
2. Save the full, 40-character commit hash of the bad commit to `/home/user/bad_commit_hash.txt`.
3. The regression was caused by an incorrect formula implementation (a bitwise mask was changed incorrectly, breaking the 31-bit signed behavior simulation). Fix the formula in `prng.py` on the `main` branch.
4. Generate a unified diff patch of your fix and save it to `/home/user/fix.patch` (e.g., using `git diff > /home/user/fix.patch`).

Ensure that your fix restores the original mathematical behavior expected by the legacy system, and that the patch applies cleanly to the latest `main` branch.