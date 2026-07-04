You are an SRE responding to an incident. The background monitoring service that aggregates server uptime metrics has crashed, and a rogue cron job accidentally deleted the current log file before it could be processed. 

Fortunately, the background process that originally wrote the log file is still running and holding the deleted file open. 

Your tasks are:
1. **Recover the deleted log file**: Identify the process holding the deleted metrics log file (it was originally named `uptime_metrics.log`). Recover its full contents and save them to `/home/user/recovered_metrics.log`.
2. **Fix the aggregator script**: There is a Python script at `/home/user/aggregate_uptime.py`. If you run it against the recovered log file, it will crash with a traceback due to an edge-case in the log format (some log lines were corrupted by network glitches and are not valid JSON).
3. **Generate the report**: Modify `/home/user/aggregate_uptime.py` so that it safely catches parsing errors, skips invalid lines, and successfully sums the `uptime_ms` for all valid JSON log entries.
4. Run your fixed script on `/home/user/recovered_metrics.log`. The script should output a file exactly at `/home/user/total_uptime.json` with the following format:
```json
{"total_uptime_ms": 15500}
```

Constraints:
- Do not kill the background process holding the file until you have recovered the data.
- The aggregation script must use the `json` module to parse the lines and must gracefully handle `json.JSONDecodeError` or missing keys without crashing.