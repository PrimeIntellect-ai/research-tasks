You are a DevOps engineer troubleshooting a failed mathematical simulation pipeline on a production server. The pipeline recently started failing with out-of-bounds errors, and a memory dump was generated during the crash.

Your objective is to identify the root cause, resolve dependency issues, extract error diagnostics, and provide a final report. 

Here is what you need to do:

1. **Dependency Conflict Resolution:** 
   Navigate to `/home/user/sim_repo`. The project has a `requirements.txt` file, but attempting to create a virtual environment and install the dependencies (`pip install -r requirements.txt`) fails due to a version conflict. Identify the conflicting package versions and fix the `requirements.txt` file so that `pip install` succeeds.

2. **Git Bisection & Regression Tracking:**
   The simulation script is `sim.py`. It runs successfully in older commits but currently crashes with an `IndexError`. The crash is caused by a precision loss bug introduced in a recent commit, which eventually causes an off-by-one error during array indexing. 
   Use Git bisection (`git bisect`) to find the exact commit hash that introduced the bug. The simulation can be tested simply by running `python sim.py`. A successful run exits with code 0; a failure exits with a non-zero code.

3. **Memory Dump Analysis:**
   When the production system crashed, it generated a memory dump file located at `/home/user/logs/dump.bin`. This binary file contains a lot of garbage bytes, but it also contains a specific ASCII panic string formatted as `PANIC_LOG:[DIAGNOSTIC_MESSAGE]`. Extract this complete string.

4. **Reporting:**
   Create a JSON file at `/home/user/resolution.json` with the following structure:
   ```json
   {
     "bad_commit": "<the_full_git_commit_hash_of_the_breaking_change>",
     "panic_string": "<the_extracted_panic_string_from_dump.bin>"
   }
   ```

Note: Ensure your final `resolution.json` is perfectly formatted. You may use any standard Linux CLI tools (like `strings`, `git`, `python`, `grep`) to accomplish these tasks.