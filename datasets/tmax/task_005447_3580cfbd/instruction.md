You are a support engineer tasked with debugging a critical data processing pipeline written in Bash. The pipeline script, `process_metrics.sh`, resides in a Git repository located at `/home/user/metrics_pipeline`. 

Customers have reported that the script randomly crashes on certain edge-case data, throwing an assertion failure. We know the script worked fine in the `v1.0` release, but it is currently broken on the `master` branch.

Your objectives:
1. **Fuzz Testing:** The script takes a single CSV file as an argument. The CSV format is `id,status,value` (e.g., `1,active,100`). Write a Bash fuzzer to generate random data inputs and feed them to `process_metrics.sh` to discover the exact edge case that causes the script to fail with a non-zero exit code. 
2. **Git Bisection:** Once you identify the specific data characteristic causing the crash, create a minimal reproducible test file named `/home/user/failing_input.csv`. Use `git bisect` (between tag `v1.0` and `master`) along with your failing input to find the exact commit that introduced the regression.
3. **Query Result Debugging:** The bug is rooted in a SQL query executed via `sqlite3` inside the script. Analyze the failing commit to understand why the query result violates the script's internal assertions.
4. **Fix the Bug:** Create a fixed version of the script based on the `master` branch and save it to `/home/user/fixed_process_metrics.sh`. The fixed script must successfully process the edge-case data and all normal data, while maintaining the intended business logic (e.g., handling nulls/zeros correctly without crashing).
5. **Reporting:** Write the full commit hash of the first bad commit to `/home/user/bad_commit.txt`.

Ensure `/home/user/bad_commit.txt` contains exactly the 40-character commit hash and nothing else. Ensure `/home/user/fixed_process_metrics.sh` is executable and passes the assertion on your `failing_input.csv`.