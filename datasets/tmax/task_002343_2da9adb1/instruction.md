You are tasked with debugging a critical regression in a multithreaded Python synchronization service. 

Recently, the service started deadlocking under high contention. We know the regression was introduced somewhere in the last 200 commits. 

Your objectives are:
1. **Bisect the Repository**: Go to the Git repository located at `/home/user/sync_service`. The commit tagged `v1.0` is known to be good (no deadlock). The current `HEAD` (tagged `v2.0`) is known to be bad (deadlocks). 
   - The application is executed by running `python main.py`. 
   - A "good" commit will exit cleanly within 1 second. 
   - A "bad" commit will deadlock and hang indefinitely. You will need to write a script or command to wrap `python main.py` with a timeout (e.g., 2 seconds) so that you can automate the bisection process to find the *first* bad commit.
   
2. **Memory Dump Analysis**: When the deadlock was first observed in production, the system generated a memory dump, which has been provided at `/home/user/core.dmp`. We suspect a secret token was leaked into memory during the deadlock state. 
   - Analyze the binary memory dump to extract the secret token.
   - The token always matches the format: `SECRET_TOKEN-<16 alphanumeric characters>` (e.g., `SECRET_TOKEN-aB3dE5gH8iJ0kL2m`).

3. **Reporting**: Create a JSON file at `/home/user/investigation.json` with the exact results of your investigation. The JSON must have the following structure:
```json
{
  "first_bad_commit": "<full_40_character_commit_hash>",
  "secret_token": "<extracted_secret_token>"
}
```

Ensure your JSON is valid and the file is written to the exact path specified.