You are a support engineer responding to a customer escalation. The customer provided a minimal reproducible example of their data processing pipeline, but they report that it fails to build in their CI environment, and when they run it locally, it crashes midway through processing.

Your goal is to diagnose the build failure, trace the intermediate state to identify the corrupted input, implement error recovery, and write a regression test to prevent future regressions.

Here is what you need to do:

1. **Fix the Build Environment:**
   The customer provided a build script at `/home/user/pipeline_project/build.sh` and a requirements file. Running `./build.sh` fails. Diagnose and fix the build script so that it successfully installs the dependencies.

2. **Trace Intermediate State:**
   The main script is `/home/user/pipeline_project/pipeline.py`. It reads from `/home/user/pipeline_project/data.csv`. When run, it crashes due to a data error.
   Modify `pipeline.py` to trace its progress. Right before it attempts to parse the `value` column of each row into an integer, it should append the `id` of that row to `/home/user/diagnostics/trace.log` (one `id` per line).

3. **Implement Error Recovery:**
   Modify `pipeline.py` so that if a row contains corrupted data (e.g., cannot be parsed as an integer), the script catches the exception, appends the exact raw line (including the newline character) of the corrupted row to `/home/user/diagnostics/corrupted_rows.log`, and continues processing the remaining rows. 
   When the script finishes, it must write the total sum of all valid `value`s to `/home/user/diagnostics/result.txt` (just the integer).

4. **Construct a Regression Test:**
   Create a test file at `/home/user/pipeline_project/test_regression.py`. Use `pytest` to write a test function named `test_corrupted_data_handling`. 
   This test must import the `process_data` function from `pipeline.py`. You should pass a list of strings representing CSV lines to the function (e.g., `["id,value\n", "1,10\n", "2,bad\n", "3,30\n"]`) and assert that the function correctly returns the sum of the valid rows (which would be `40` in this example).

**Constraints & Notes:**
- Create the `/home/user/diagnostics/` directory before writing logs to it.
- Ensure `test_regression.py` passes when run with `pytest /home/user/pipeline_project/test_regression.py`.
- Do not change the overall logic of `pipeline.py` other than adding tracing, error handling, and returning the final sum from `process_data`.