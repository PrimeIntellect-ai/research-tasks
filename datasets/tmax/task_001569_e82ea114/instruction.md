You are a Site Reliability Engineer (SRE). Your team uses a custom Python script, `/home/user/monitor/uptime_monitor.py`, to check the health of various internal services and generate an uptime report. 

Recently, the monitor has stopped generating reports. The cronjob executing it is failing and no output is produced. 

A local mock server simulating the internal services is already running on port 8080.

Your task is to debug the system and fix the issues so that the script successfully completes its run and generates the report.

Requirements:
1. Fix any issues preventing `uptime_monitor.py` from parsing its configuration file located at `/home/user/monitor/endpoints.json`.
2. The monitor contains an assertion that currently causes the entire script to crash if a service returns an unexpected status code (like a 500 error). Modify `uptime_monitor.py` so that instead of crashing, it gracefully handles the failure and logs the endpoint as `DOWN`.
3. Valid services (returning 200 or 301) should be logged as `UP`.
4. Run your fixed script. It must generate the final report at `/home/user/monitor/report.txt`.
5. The `report.txt` file must contain exactly one line per endpoint in the exact format: `<url> - <UP/DOWN>` (e.g., `http://localhost:8080/service_a - UP`).

Do not change the paths of the files. You may modify the `endpoints.json` file and `uptime_monitor.py` script as necessary to complete the objective.