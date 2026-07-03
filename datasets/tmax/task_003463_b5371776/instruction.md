You are tasked with debugging a regression in a data processing pipeline.

In `/home/user/data_processor`, there is a Git repository containing a Python script `process.py` which processes JSON data. A regression was recently discovered: when the script is run on the `/home/user/crash_input.json` file on the `master` branch, it crashes with a `ZeroDivisionError`. The original working version of this script (at the very first commit) did not crash on this file.

Your objectives are:
1. **Find the Regression (Bisection):** 
   Identify the first Git commit in the repository that introduced this `ZeroDivisionError` when processing `/home/user/crash_input.json`. 
   Write the full 40-character commit hash of this first bad commit to `/home/user/first_bad_commit.txt`.

2. **Test Minimization (Delta Debugging):**
   The `/home/user/crash_input.json` file contains a large list of items, but only one specific item is triggering the crash. 
   Minimize this JSON file so that its `"items"` array contains *only* the single dictionary object responsible for the crash. The file should maintain the overall valid JSON structure (e.g., `{"items": [{"val": ..., "id": ...}]}`).
   Save this minimized JSON file to `/home/user/minimized.json`.

Both of your output files will be automatically checked by a verification script.