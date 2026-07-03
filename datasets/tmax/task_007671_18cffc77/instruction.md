You are a DevOps engineer tasked with fixing a broken log processing pipeline. 

The pipeline code is located in a Git repository at `/home/user/log_processor`. When we run `python /home/user/log_processor/process.py`, it simply hangs indefinitely and produces no output. Additionally, the developer who wrote it mentioned that it relies on a secret API token that was accidentally hardcoded in an early commit, then later removed and replaced with an environment variable. We lost the environment variable and need to recover the token.

Your objectives:
1. **Git Forensics**: Inspect the Git history of `/home/user/log_processor` to find the original hardcoded secret token.
2. **System Call Tracing**: Use `strace` or similar tools on `process.py` to figure out why the script is hanging. Fix the code so it no longer hangs (it is waiting on a specific file/pipe that doesn't exist or isn't being written to; just remove or bypass the blocking read).
3. **Query Result Debugging**: Once the script runs, it processes `/home/user/log_processor/server_logs.csv`. However, the current filtering logic is wrong. It is supposed to extract ONLY logs where `level` is `CRITICAL` and `service` is `auth`. Modify `process.py` to correctly filter the dataframe and write the output to `/home/user/processed_logs.csv`.
4. **Execution**: Run the fixed script with the recovered token provided as the `SECRET_TOKEN` environment variable.

Finally, create a JSON report at `/home/user/debug_report.json` with the following exact structure:
```json
{
  "recovered_secret": "the_secret_string_found_in_git",
  "blocking_file": "the_absolute_path_the_script_was_hanging_on",
  "critical_auth_count": 0 // The integer number of rows in the final processed CSV
}
```