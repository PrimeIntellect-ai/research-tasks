You are a mobile build engineer maintaining a CI/CD pipeline for an Android application. We are migrating our data processing scripts to be dependency-free so they can run in lightweight Alpine containers, which means removing Python dependencies. 

Your workspace is located at `/home/user/pipeline`. 

Currently, our pipeline processes build manifest files (containing key-value pairs of APK metadata) to generate patch notes. We have a broken Bash script `/home/user/pipeline/process.sh` that attempts to do this, but it suffers from a variable scope/lifetime bug (variables leaking between functions and loops, causing it to truncate output) and relies on a legacy Python script `/home/user/pipeline/legacy_filter.py` for data filtering.

Your tasks are:

1. **Code Translation & Data Processing:**
   Read `/home/user/pipeline/legacy_filter.py`. Translate its logic entirely into a Bash function within `/home/user/pipeline/process.sh`. The logic filters out any key-value pairs where the key starts with `DEBUG_` or `TEST_`, and ignores empty lines.

2. **Debugging (Variable Scopes):**
   Fix the variable scope ("lifetime") issues in `/home/user/pipeline/process.sh`. The script currently fails to process multiple files correctly because a helper function uses a global loop variable that overwrites the main loop's variable. Ensure proper use of `local` variables.

3. **Diff and Patch Processing:**
   Modify `process.sh` so that it accepts two manifest files as arguments (e.g., `./process.sh data/v1.txt data/v2.txt`). The script must:
   - Process both files using the translated Bash filtering logic.
   - Sort the filtered outputs alphabetically.
   - Generate a unified diff (`diff -u`) between the sorted, filtered old manifest and the sorted, filtered new manifest.
   - Output the resulting diff to `/home/user/pipeline/build.patch`.

4. **Package Management & Unit Testing:**
   - We need to test the script using BATS (Bash Automated Testing System). Clone the bats-core repository (`https://github.com/bats-core/bats-core.git`) into `/home/user/bats-src`.
   - Install bats locally to `/home/user/local` using its `install.sh` script.
   - Write a BATS test suite at `/home/user/pipeline/test.bats` containing at least one test case that verifies `process.sh` generates the correct unified diff without errors.
   - Run the test suite using the installed BATS executable and redirect the output to `/home/user/test_results.log`.

Run your fixed `process.sh` on `/home/user/pipeline/data/old_build.txt` and `/home/user/pipeline/data/new_build.txt` to generate the final `/home/user/pipeline/build.patch`.