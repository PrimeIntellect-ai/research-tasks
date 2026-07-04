You are a Site Reliability Engineer (SRE) investigating an ongoing database outage that has caused a service downtime. The monitoring alerts went off recently, and you need to figure out when exactly the issue started and recover the lost credentials.

You have access to two things:
1. The log files located in `/home/user/logs/` (`api.log` and `db.log`).
2. The application's local git repository at `/home/user/service_app`.

Your task:
1. **Reconstruct the timeline:** Analyze `/home/user/logs/db.log` to find the exact timestamp of the *first* time the error message `FATAL: password authentication failed for user 'dbadmin'` appears.
2. **Git Forensics:** Someone accidentally modified the database password in the application's configuration file (`settings.py`) in the git repository and deployed it, causing this outage. Search the git history of `/home/user/service_app` to find the *original* valid password that was used for `dbadmin` before it was broken in a subsequent commit. 
3. **Report:** Create a file at `/home/user/incident_report.txt` containing exactly two lines:
   - Line 1: The exact timestamp of the first database authentication failure (e.g., `2023-11-05T14:22:10Z`).
   - Line 2: The recovered valid password from the git history.

No other text or explanation should be in the file.