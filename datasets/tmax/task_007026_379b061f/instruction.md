You are an engineer tasked with investigating a critical memory leak in a long-running Python background service. The service recently started experiencing Out-Of-Memory (OOM) kills. 

You have access to the service's local Git repository located at `/home/user/app`.

Your investigation must accomplish the following:

1. **Git Forensics & Root Cause Analysis:** 
   Inspect the Git history in `/home/user/app`. Find the exact commit that introduced the race condition causing the memory leak (a thread-safety issue where concurrency controls were removed or improperly implemented).
   
2. **Secret Recovery:** 
   During your forensic investigation of the Git history, identify a highly sensitive API key (`sk-live-...`) that was accidentally committed and subsequently removed in the recent commit churn.

3. **Regression Test Construction:**
   Write a Python regression test at `/home/user/test_race.py` that imports the vulnerable class from the app and demonstrates the race condition. The script should exit with code 1 if the race condition/leak is detected (i.e., state corruption occurs when accessed by multiple threads), and exit with code 0 if the code behaves correctly.

4. **Reporting:**
   Compile your findings into a JSON report located at `/home/user/report.json`. The JSON file must have the exact following schema:
   ```json
   {
     "leak_commit_hash": "<full_40_character_git_commit_hash>",
     "leaked_api_key": "<the_full_api_key_string>"
   }
   ```

Do not modify the source code in `/home/user/app` to fix the bug; your task is purely forensic and diagnostic. Ensure your regression test correctly simulates concurrent access to trigger the failure mode.