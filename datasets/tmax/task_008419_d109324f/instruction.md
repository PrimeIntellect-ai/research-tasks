You are a monitoring specialist tasked with integrating a legacy interactive health-check system into a modern Git-based deployment pipeline. 

Your organization manages service deployments via a Git repository. Before accepting any new deployment configurations, the Git server must verify that the target services are healthy. Unfortunately, the legacy monitoring system only exposes an interactive command-line interface, meaning you must automate interactions with it.

Here are your detailed requirements:

1. **Repository Setup:**
   - Initialize a bare Git repository at `/home/user/deploy_repo.git`.

2. **The Legacy Monitor:**
   - A mock legacy monitoring tool is located at `/home/user/legacy_monitor.py`.
   - When executed (`python3 /home/user/legacy_monitor.py`), it behaves interactively:
     1. It prints: `Enter service name: `
     2. You input a service name (e.g., `web-backend`) and press Enter.
     3. It replies either:
        `Status: OK`
        or
        `Status: DOWN`
        or
        `Status: UNKNOWN`
     4. It then prints: `Check another? (y/n): `
     5. If you input `y`, it loops back to step 1. If `n`, it exits cleanly.

3. **Git Pre-Receive Hook (The Health Check):**
   - Create a Git `pre-receive` hook written in Python at `/home/user/deploy_repo.git/hooks/pre-receive`. Make sure it is executable.
   - You may use the `pexpect` library to interact with the legacy monitor (install it via `pip install pexpect --user` if needed).
   - The hook must read the standard input provided by Git (`<oldrev> <newrev> <refname>`).
   - For the incoming `<newrev>`, the hook must inspect the file named `deploy_targets.txt` in the root of the repository. (Hint: use `git cat-file blob <newrev>:deploy_targets.txt`).
   - `deploy_targets.txt` will contain a list of service names, one per line. Ignore empty lines.
   - The hook must use a *single* spawned `pexpect` session with `/home/user/legacy_monitor.py` to check the health of all services listed in `deploy_targets.txt` sequentially.
   
4. **Alerting and Logging Logic:**
   - If *any* service returns `Status: DOWN` or `Status: UNKNOWN`, the hook must:
     1. Print to stderr exactly: `[ALERT] Service <service_name> is down or unknown!`
     2. Append a JSON object to `/home/user/monitoring_log.json` on a new line. The JSON format must be: 
        `{"ref": "<refname>", "status": "rejected", "failed_services": ["<failed_svc_1>", "<failed_svc_2>"]}` (include all failed services).
     3. Exit with a non-zero exit code to reject the push.
   - If *all* services return `Status: OK`, the hook must:
     1. Print to stdout exactly: `[OK] All services healthy.`
     2. Append a JSON object to `/home/user/monitoring_log.json` on a new line:
        `{"ref": "<refname>", "status": "accepted", "failed_services": []}`
     3. Exit with code `0` to accept the push.

Ensure your Python script is robust, handles potential timeouts (fail the check if it times out), and properly cleans up the `pexpect` process. All outputs must match the requested strings exactly.