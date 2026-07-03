You are an engineer tasked with investigating a severe memory leak in a long-running log processing service. The service recently started consuming unbounded memory and crashing when processing certain daily log batches. 

The service's source code is located in a Git repository at `/home/user/log_service`. You have been provided with a representative log file `/home/user/suspicious_logs.txt` that reliably triggers the memory leak when fed into the processor.

Your objectives are:
1. **Dependency Resolution**: The latest commit relies on a specific version of a parsing library, but the environment currently has a conflicting version installed. Inspect the requirements and fix the dependency issue so the application can run.
2. **Git Bisection**: The memory leak is a regression. Use `git bisect` to identify the exact commit hash that introduced the memory leak. A test script `/home/user/log_service/test_leak.py` is provided in the repository to help you detect if the leak is present (it exits with code 1 if a leak is detected, and code 0 if normal).
3. **Delta Debugging / Minimization**: The provided `suspicious_logs.txt` is quite large. Use test minimization / delta debugging techniques to isolate the *single* malformed log line from this file that triggers the memory leak.
4. **Code Fix**: Once you identify the malformed input and the faulty logic introduced in the bad commit, fix the parser (in `log_service/parser.py`) so it gracefully handles the corrupted input without accumulating unbounded state in memory.

After completing the investigation and fixing the code, create a file at `/home/user/solution.json` with exactly the following JSON structure:

```json
{
  "bad_commit_hash": "<the_full_40_character_git_hash_of_the_first_bad_commit>",
  "leaking_line_content": "<the_exact_verbatim_text_of_the_single_log_line_causing_the_leak>",
  "fixed_successfully": true
}
```

Constraints:
- Do not modify `test_leak.py`. You should only modify `parser.py` to fix the bug.
- Ensure your fixed `parser.py` passes the `test_leak.py` check.