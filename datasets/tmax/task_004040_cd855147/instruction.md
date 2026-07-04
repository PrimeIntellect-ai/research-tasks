You are tasked with writing a mock Kubernetes-like operator in Python that manages process dependencies and restart policies. 

In `/home/user`, there are two service scripts: `/home/user/db.py` and `/home/user/app.py`. 
There is also a configuration manifest at `/home/user/manifest.json` which looks like this:

```json
{
  "services": {
    "db": {
      "command": "/usr/bin/python3 /home/user/db.py",
      "ready_marker": "SYSTEM_READY"
    },
    "app": {
      "command": "/usr/bin/python3 /home/user/app.py",
      "depends_on": "db",
      "restart_policy": "Always",
      "max_restarts": 3
    }
  }
}
```

Your objective is to write a Python script at `/home/user/operator.py` that does the following:
1. Parses `/home/user/manifest.json`.
2. Starts the `db` service.
3. Monitors the standard output of the `db` service. It must **wait** until the `db` service prints the exact string `"SYSTEM_READY"` to standard output. You can use the `pexpect` module or standard `subprocess` for this.
4. Once `"SYSTEM_READY"` is detected, the script should start the `app` service.
5. The `app` service is known to be flaky and may crash. Your operator must monitor the `app` process. If it exits with a non-zero exit code, your operator must restart it.
6. The operator must respect the `max_restarts` policy. It should restart the `app` service up to a maximum of 3 times (i.e., 4 total executions).
7. Your operator must maintain a log file at `/home/user/operator.log`. It must append the following exact log lines as the events occur:
   - When starting db: `[EXEC] Starting db`
   - When db is ready: `[STATE] db is ready`
   - When starting app: `[EXEC] Starting app`
   - If app crashes (non-zero exit): `[WARN] app crashed, restarting`
   - If app max restarts are reached: `[ERROR] app max restarts exceeded`

Run your script for long enough to allow `app` to stabilize or hit its restart limit, then exit the operator. `app.py` is designed to succeed eventually or fail cleanly. Make sure your script terminates when the `app` service finishes successfully or hits its restart limit.