You are an on-call engineer responding to a PagerDuty alert at 3:00 AM. The internal metrics aggregation system has frozen. The dashboard shows that the server stops accepting new metric updates entirely during high load, leading to cascading timeouts in upstream services.

The system consists of two parts:
1. An upstream dispatcher (which has already been stopped, but its last logs are available).
2. The aggregation server written in C.

Your investigation has narrowed the issue down to `/home/user/app/server.c`. Under normal conditions, the server processes metrics fine. However, the system occasionally receives anomalous statistical values which trigger a heavy "convergence" algorithm to smooth the data. It appears that when this algorithm fails to converge, the server deadlocks shortly after.

You have access to the source code and the historical logs from right before the system crashed:
- Code: `/home/user/app/server.c`
- Dispatcher logs: `/home/user/logs/dispatcher.log`
- Server logs: `/home/user/logs/server.log`

Your task is to:
1. **Analyze the Logs**: Reconstruct the timeline across both log files to identify the exact event that triggered the crash. Correlate the dispatched requests with the server's processing logs. 
2. **Identify the Bug**: Analyze `/home/user/app/server.c` to understand why the convergence failure causes a deadlock.
3. **Fix the Code**: Correct the bug in the C code so that it handles convergence failures gracefully without freezing the server. Save your fixed code to `/home/user/app/server_fixed.c` and compile it to an executable at `/home/user/app/server_fixed` using `gcc -pthread /home/user/app/server_fixed.c -o /home/user/app/server_fixed`.
4. **Document the RCA (Root Cause Analysis)**: Create a JSON file at `/home/user/rca.json` with the exact details of the incident based on your log analysis. It must strictly follow this format:
```json
{
  "bug_function": "<name of the C function containing the deadlock bug>",
  "first_anomaly_timestamp": "<exact timestamp of the anomalous request from dispatcher.log, e.g., 2024-05-10T03:14:22>",
  "failed_metric_id": <integer ID of the metric that caused the convergence failure>
}
```

Ensure your fixed server does not deadlock when a convergence failure occurs.