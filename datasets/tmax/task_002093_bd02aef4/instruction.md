You are tasked with debugging a data processing pipeline that has recently started failing intermittently.

The pipeline is managed in a Git repository located at `/home/user/data_pipeline`. It contains a script named `transform.sh` which reads from `input.csv` (located in the same directory) and outputs a transformed summary to stdout.

There are exactly 200 commits in this repository. 
- The oldest commit (`HEAD~199`) is known to be **GOOD**. 
- The newest commit (`HEAD`) is known to be **BAD**.

The regression introduces an intermittent bug: occasionally, `transform.sh` silently drops a specific aggregate row from its output. 

Your objectives are:
1. **Analyze the Data Transformation Diff:** Run the script against `input.csv` multiple times to capture both the correct output and the corrupted output. Compare them to determine exactly which output line is intermittently missing.
2. **Reproduce the Intermittent Failure Reliably:** Write a test wrapper script that repeatedly runs `transform.sh` to confidently determine whether a given version of the script is functioning perfectly or exhibiting the intermittent bug.
3. **Bisect the Regression:** Use your robust test script alongside `git bisect` (or manual bisection) to find the *first bad commit* that introduced the intermittent bug.

**Deliverables:**
1. Find the exact full 40-character Git commit SHA of the first bad commit and save it to a file named `/home/user/bad_commit_sha.txt`.
2. Save the exact line of text that is intermittently missing from the output (the dropped data row) to a file named `/home/user/dropped_data.txt`. Ensure the file contains exactly this line and nothing else.