You are a Site Reliability Engineer (SRE) tasked with monitoring the uptime and error budgets of a critical microservice. 

Your team uses a Python script located at `/home/user/uptime_monitor/calculator.py` to parse standard health check logs (`/home/user/uptime_monitor/health_logs.txt`) and generate an SLA report. However, the automated cron job has been failing, and your manager reported that even when it ran in the past, the metrics looked highly inaccurate.

You need to debug and fix `calculator.py`. 

Here are the operational rules for the service metrics:
1. **Crash Resolution**: The script currently crashes with a traceback when processing the logs. You must analyze the failure and fix the parsing logic.
2. **Status Code Rules**: The logs contain HTTP status codes. Currently, the script considers any status code `>= 400` as an error. However, per our SLA, 4xx codes are client errors and DO NOT count against our uptime. Only `5xx` server errors count as downtime.
3. **Timeouts**: Occasionally, the log records `TIMEOUT` in the status column. A `TIMEOUT` means the server completely failed to respond. Your script must treat any `TIMEOUT` entry identically to a `503` status code.
4. **Error Budget Burn Rate**: Our Service Level Objective (SLO) is 99.9% uptime. This means our allowed error budget (error rate) is 0.1% (or `0.001`). The script's formula for the Error Budget Burn Rate is currently wrong. The correct formula is: `burn_rate = current_error_rate / allowed_error_budget`.

Your task:
1. Navigate to `/home/user/uptime_monitor/`.
2. Fix the bugs in `calculator.py` based on the operational rules above.
3. Run the script so that it successfully parses `health_logs.txt`.
4. Ensure the script writes its final output to `/home/user/uptime_monitor/final_metrics.json` exactly in the JSON format originally intended by the script.

Do not change the keys in the output JSON; only ensure the logic calculating their values is corrected.