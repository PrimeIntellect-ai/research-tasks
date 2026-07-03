You are an observability engineer trying to fix a flaky local metrics stack. The stack consists of two simulated lightweight containers (Python background processes) that fail to start due to race conditions and missing dependencies—similar to a systemd service failing due to a missing `After=` directive. 

Currently, `dashboard-backend.py` crashes because it starts before `metrics-gatherer.py` is ready. Furthermore, `metrics-gatherer.py` crashes because it requires a configuration file that must be restored from a backup archive before it boots.

Your task is to write an orchestration script at `/home/user/start_observability.sh` (make sure it is executable) that correctly manages the lifecycle of these services. 

The script must perform the following actions in order:
1. **Restore Backup:** Extract the contents of `/home/user/backup/metrics_backup.tar.gz` into the directory `/home/user/data/active/`. (This archive contains a `config.json` file required by the gatherer).
2. **Start Gatherer:** Launch `/home/user/metrics-gatherer.py` in the background. 
3. **Monitor Process Readiness:** Wait until `metrics-gatherer.py` creates its socket file at `/home/user/data/active/metrics.sock`. Do not proceed until this file exists.
4. **Start Backend:** Once the socket exists, launch `/home/user/dashboard-backend.py` in the background.
5. **Output PIDs:** Write the Process IDs (PIDs) of both background processes into a JSON file at `/home/user/run/pids.json` exactly in this format:
   `{"gatherer_pid": 1234, "backend_pid": 1235}` (replace 1234 and 1235 with the actual integer PIDs).

Constraints:
- You must use bash or Python to write `/home/user/start_observability.sh`.
- Do not modify `metrics-gatherer.py` or `dashboard-backend.py`.
- Ensure `/home/user/start_observability.sh` exits cleanly (exit code 0) after writing the `pids.json` file, leaving the two processes running in the background.