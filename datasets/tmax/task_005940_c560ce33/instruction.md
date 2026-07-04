You have been assigned to investigate a critical bug in a data processing pipeline located at `/home/user/log_processor`. 

The pipeline processes custom log files. Recently, the operations team reported that the service periodically hangs and consumes all available memory until it is killed by the OOM killer. It appears to be an infinite loop causing a memory leak when parsing a specific edge-case format.

A junior engineer noticed that a specific test file triggered this hang and simply deleted the file from the repository to "fix" the CI pipeline, rather than fixing the underlying parsing logic. 

Your objectives:
1. **Recover the deleted test data**: Inspect the git repository's history to find and restore the recently deleted test file that triggers the bug. Save it back to its original relative path within the repository.
2. **Find the regression**: Use git bisection (or manual investigation of the git history) to identify the exact commit hash that introduced the bug. The bug was introduced in a commit that altered the parsing logic in `process.py`.
3. **Fix the bug**: Repair the parsing logic in `process.py` on the `main` branch so that it correctly handles the edge-case without looping infinitely or leaking memory, while preserving the intended parsing behavior.
4. **Process the data**: Run the fixed `process.py` on the recovered test file. The script takes an input file and an output file argument: `python process.py <input_file> -o /home/user/output.json`.
5. **Create a report**: Write your findings to `/home/user/report.txt`. The file must contain exactly two lines:
   - Line 1: The full (40-character) git commit hash of the commit that *introduced* the infinite loop/memory leak.
   - Line 2: The original relative path of the recovered test file within the repository (e.g., `data/test_file.txt`).

Constraints:
- Do not rewrite the entire `process.py` script. Only fix the specific infinite loop/memory leak bug.
- Ensure the script outputs the correctly parsed JSON format to `/home/user/output.json`.