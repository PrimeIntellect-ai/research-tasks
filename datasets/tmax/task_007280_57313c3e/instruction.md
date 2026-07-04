You are an engineer tasked with investigating a memory and performance issue in a long-running service located at `/home/user/service_repo`. The service periodically scans a directory and processes files using a helper binary. However, it intermittently spawns runaway background processes that eventually crash, leaving behind memory dumps.

Your investigation must cover the following steps:

1. **Git Forensics:** The previous maintainer accidentally committed a debug token, which was later removed. Find this `DEBUG_TOKEN` in the git history of `/home/user/service_repo`.
2. **Memory Dump Analysis:** Inspect the memory dump file located at `/home/user/service_repo/crash_heap.dmp`. Find the fatal error string which takes the format `[FATAL] File parse error on: <filename_fragment>`. Extract this fragment.
3. **Reproduce & Fix the Bug:** The primary script, `/home/user/service_repo/scan.sh`, handles file processing. Read the script and figure out why it is failing intermittently and causing rogue processes—specifically when processing files with certain characters (like spaces) in their names. Fix the script so that it properly handles all filenames without splitting them or skipping files.
4. **Report:** Create a JSON file at `/home/user/debug_report.json` containing your findings. It must have the exact following schema:
   ```json
   {
     "debug_token": "the_token_found_in_git",
     "crash_fragment": "the_filename_fragment_from_dump"
   }
   ```

To be successful, `/home/user/service_repo/scan.sh` must be modified in place to correctly process files with spaces in their names (using safe bash globbing or safe `while read` loops instead of parsing `ls` or unquoted expansions).