You are tasked with investigating a memory leak in a critical long-running Bash service called `sensor_aggregator.sh`. The service aggregates telemetry data but has been OOM-killed in production after running for several days.

System State:
- The service script is located at `/home/user/app/sensor_aggregator.sh`.
- A core dump (simulated as a raw memory dump file) was captured right before the last crash, located at `/home/user/dumps/mem_core.dump`.
- Logs from various components (sensor ingestion, aggregator, and system monitor) are in `/home/user/logs/`.

Your objective is to:
1. **Memory Dump Analysis**: Extract strings from `/home/user/dumps/mem_core.dump` to determine what data is accumulating in memory. Look for an obvious repeating pattern or large strings being hoarded.
2. **Log Timeline Reconstruction**: Correlate the leaked data with the logs in `/home/user/logs/` to find the exact timestamp and `TRACE_ID` when the leak started (the first time the anomalous data pattern was logged).
3. **Fix the Leak**: Identify the Bash variable causing the leak in `/home/user/app/sensor_aggregator.sh` and fix the code. The service must still function but without accumulating memory indefinitely. (Do not change the output format of the service, just fix the leak).
4. **Assertion-Based Validation**: Write a test script at `/home/user/app/verify_fix.sh` that starts `sensor_aggregator.sh` in the background, sends 500 lines of fake sensor data to its input pipe `/home/user/app/sensor_pipe`, and asserts (using a Bash `[[ ]]` check) that the RSS memory of the process does not exceed 10MB. The script should exit 0 if the test passes and 1 if it fails.

Finally, write your findings to `/home/user/investigation_report.txt` exactly in this format:
```
LEAKING_VARIABLE: <name_of_the_bash_variable_causing_the_leak>
FIRST_LEAK_TRACE_ID: <the_trace_id_from_the_logs_when_it_started>
```