You are a Site Reliability Engineer responding to a monitoring outage. A power failure corrupted our primary uptime database, leaving us with only a custom Write-Ahead Log (WAL) file located at `/var/log/monitoring/uptime.wal`. 

We use a third-party, Bash-based package called `bash-uptime-monitor-1.2.0` (vendored at `/app/bash-uptime-monitor-1.2.0`) to process these logs. However, the recovered data is showing severe statistical anomalies—several critical servers are incorrectly reporting near-zero uptime, triggering false alarms.

Your objectives:
1. **Error Diagnosis & Root Cause Analysis:** Investigate `/app/bash-uptime-monitor-1.2.0/recover.sh`. There is a bug in how it parses the WAL file, causing it to silently drop specific valid log entries, leading to the statistical anomalies. Identify and fix this bug in the vendored package.
2. **Minimal Reproducible Example:** Create a small, synthetic WAL file at `/home/user/mre.wal` containing exactly 3 lines. When the broken, original version of `recover.sh` processes this file, it should successfully parse the first line, incorrectly drop the second line, and successfully parse the third. The fixed version should parse all three.
3. **Database Recovery:** Use your fixed `/app/bash-uptime-monitor-1.2.0/recover.sh` to process the full `/var/log/monitoring/uptime.wal` and generate the recovered database file at `/home/user/recovered_db.csv`.
4. **Statistical Analysis:** Write a Bash script at `/home/user/analyze.sh` that reads `/home/user/recovered_db.csv` and calculates the total uptime percentage for each `server_id`. The script must output the results to `/home/user/uptime_results.csv` in the format `server_id,uptime_percentage` (where uptime percentage is a float between 0.0 and 100.0).

Ensure all scripts are executable. Your analysis results will be evaluated against a hidden ground truth dataset using a Mean Absolute Error (MAE) metric.