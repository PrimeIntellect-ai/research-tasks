You are a DevOps engineer tasked with performing a post-mortem and forensic debugging on a failed log processing service. The service processes JSON log lines, but it recently crashed in production, leaving behind an incomplete state. 

Your workspace is located at `/home/user/app/`.

Here is the situation:
1. The script `/home/user/app/process_logs.py` is supposed to read `/home/user/app/data/system.log` and output a summary of HTTP 500 errors and specific endpoint hits to `final_summary.json`.
2. The service crashed during the nightly run. The traceback is captured in `/home/user/app/app.log`.
3. Analysts have reported that even when the script completes on smaller batches, the query results for `500_count` are significantly lower than expected.

Your objectives:
1. **Error Diagnosis & Fixing:** Inspect `app.log` to find why the crash occurred. Fix `process_logs.py` so that instead of crashing, if a `ValueError` is raised during the processing of a line, the script catches it, appends the exact raw JSON string (with a newline) to `/home/user/app/skipped.log`, and continues processing the rest of the file.
2. **Query Result Debugging:** Investigate the logic calculating `500_count` in `process_logs.py`. There is a type-handling bug causing many 500 status codes (which appear as both integers and strings in the raw JSON) to be ignored. Fix this so that all 500 status codes are accurately counted.
3. **Fuzz Testing:** There is a suspected *second* edge-case bug in the `process_line` function that hasn't triggered in production yet, related to a combination of HTTP method and payload size. Write a fuzzing script at `/home/user/app/fuzzer.py` that generates random dictionaries and feeds them to `process_line(data)`. Use this fuzzer to discover the hidden exception. Once discovered, patch `process_logs.py` to handle this second exception gracefully (skip the line and append it to `skipped.log` just like the `ValueError`).
4. **Regression Testing:** Write a test file `/home/user/app/test_regression.py` using standard `unittest` that imports `process_line` and asserts that:
   - String `"500"` statuses are correctly identified.
   - The first crash condition correctly raises a `ValueError` (or is handled, depending on how you structure the function, but ensure the logic is tested).
5. **Final Execution:** Run the fixed `process_logs.py`. It must successfully process the entire `data/system.log` and generate `/home/user/app/final_summary.json`.

**Expected Final State:**
- `/home/user/app/process_logs.py` is fixed.
- `/home/user/app/final_summary.json` exists with the correct aggregated counts.
- `/home/user/app/skipped.log` exists containing the raw log lines that triggered exceptions.
- `/home/user/app/fuzzer.py` and `/home/user/app/test_regression.py` exist and are functional.