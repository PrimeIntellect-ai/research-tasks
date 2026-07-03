You are an SRE monitoring the uptime of a critical distributed system. The uptime monitoring script, located at `/home/user/uptime_monitor/app.py`, periodically fetches heartbeat data from a local SQLite database (`/home/user/uptime_monitor/metrics.db`) and calculates an uptime score using a weighted moving average.

Recently, the script has been failing with numerical errors and outputting incorrect uptime percentages (e.g., > 100% or NaN). Preliminary investigation suggests:
1. The script's database query is producing duplicate rows for certain heartbeats, which artificially inflates the number of events.
2. The duplicate rows cause two consecutive events to have the exact same timestamp. The weighting algorithm calculates weight as `1.0 / (current_timestamp - previous_timestamp)`. When the timestamps are identical, this results in a `ZeroDivisionError` or numerical explosion.
3. The calculation of the moving average state does not properly handle the first event's initialization, causing intermediate states to be malformed.

Your task:
1. Debug and fix the SQL query in `/home/user/uptime_monitor/app.py` so that it returns exactly one record per heartbeat (no duplicates). Ensure that the heartbeat is correctly matched to its server.
2. Fix the numerical instability in the weighting calculation. If `current_timestamp == previous_timestamp`, the script should handle it gracefully by skipping the duplicate or assigning a safe fallback weight (e.g., `weight = 1.0`).
3. Correct the initialization logic for the intermediate state tracing so the script can process the entire database without crashing.
4. Run the fixed `/home/user/uptime_monitor/app.py` script. It is designed to output a final summary dictionary to stdout.
5. Capture the exact output of the final corrected script and write it to `/home/user/uptime_monitor/fixed_output.txt`.

Ensure your fixes are minimal but correct. The final output file `/home/user/uptime_monitor/fixed_output.txt` should contain the single dictionary string printed by the fixed script.