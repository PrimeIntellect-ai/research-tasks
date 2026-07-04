You are a monitoring specialist tasked with setting up an automated alert system. A previous administrator left behind a partial setup, and you need to complete it by building a Python-based process supervisor and log analyzer.

We have an image containing the new alerting parameters located at `/app/alert_config.png`. 

Your objectives are:
1. **Extract Configuration:** Use OCR (e.g., `tesseract`) to read `/app/alert_config.png`. It contains the target Timezone (Region), the Threshold (Max Load), and the target Process name to monitor.
2. **Process Supervision:** Write a Python script at `/home/user/alert_supervisor.py`. This script must act as a process supervisor for our log generator.
   - The log generator is located at `/home/user/generate_logs.py`.
   - **Crucial Dependency:** `generate_logs.py` will immediately crash if its dependency, `/home/user/init_env.sh`, has not been executed successfully first. Your supervisor must execute `init_env.sh` and wait for it to complete *before* launching `generate_logs.py` (resolving the missing dependency issue).
   - If `generate_logs.py` exits with a non-zero status unexpectedly, your supervisor must restart it. (Note: `generate_logs.py` will exit with code 0 when it has finished generating all records).
3. **Log Processing and Alerting:** 
   - `generate_logs.py` writes pipe-separated log lines to stdout in the format: `YYYY-MM-DD HH:MM:SS|PROCESS_NAME|LOAD_VALUE`. The timestamps are in UTC.
   - Your supervisor must capture this output.
   - Filter the output to only process lines where `PROCESS_NAME` exactly matches the one extracted from the image.
   - For matching lines, convert the UTC timestamp to the Timezone specified in the image.
   - If the `LOAD_VALUE` is strictly greater than the Max Load extracted from the image, record an alert.
4. **Output Verification:** Write the alerts to `/home/user/alerts.csv` in exactly this format:
   `YYYY-MM-DD HH:MM:SS,PROCESS_NAME,LOAD_VALUE`
   (Note the comma separators and the localized timestamp format).

Ensure your script processes the entire batch of logs until `generate_logs.py` exits with code 0, then gracefully terminates. Your success will be measured by the F1 score of the generated alerts compared to a hidden ground truth.