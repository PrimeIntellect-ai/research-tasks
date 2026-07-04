You are tasked with bisecting a Git repository to find a regression caused by a floating-point precision loss. 

There is a local Git repository located at `/home/user/orbital_calc`. This repository contains a Python module `calc.py` which computes orbital apogees. 
Recently, a regression was introduced somewhere in the last 200 commits (between the known-good tag `v1.0` and the current `HEAD` on the `main` branch). The bug changed a high-precision calculation into a low-precision one, causing downstream components to fail.

A test script has been provided at `/home/user/orbital_calc/tests/test_apogee.py` that verifies the precision of the `calculate_apogee` function. However, if you try to run it right now, it fails immediately with a stack trace due to a missing environment configuration (an import error).

Your tasks are:
1. Diagnose and fix the environment misconfiguration so the test script can run correctly.
2. Create a minimal reproducible test command (e.g., using a bash one-liner or small script) that wraps this Python test.
3. Use `git bisect` (specifically `git bisect run` is recommended for speed) to automatically find the exact commit that introduced the floating-point precision bug.
4. Once you have identified the 40-character SHA-1 hash of the first bad commit, save it to a file at `/home/user/bad_commit.txt`.

Do not modify the Git history or delete the repository. Just find the commit and write the hash to the specified file.