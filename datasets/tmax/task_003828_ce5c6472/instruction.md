You are a log analyst investigating latency patterns in a time-series dataset of system metrics. 

Your environment contains two critical files:
1. `/app/system_metrics.log`: A time-series log file containing raw system requests. Each line has the format: `[YYYY-MM-DD HH:MM:SS] USER_EMAIL REQ_TYPE LATENCY_MS`.
2. `/app/config_image.png`: An image file containing configuration parameters for your task. 

Your objectives are as follows:
1. Extract the text from `/app/config_image.png` (you may use the preinstalled `tesseract` utility). The image contains two lines: a target `PORT` and a `MASK_REGEX` intended to identify PII (specifically email addresses).
2. Process `/app/system_metrics.log` using standard shell tools (e.g., `awk`, `sed`, `grep`).
3. First, anonymize the log data by replacing any text matching the `MASK_REGEX` with the literal string `[REDACTED]`.
4. Second, calculate the average latency (`LATENCY_MS`) aggregated by hour.
5. Create a Bash-based TCP server that listens on the `PORT` extracted from the image. You may use `nc` (netcat) to handle incoming connections.
6. When a client connects and sends the exact string `FETCH_STATS`, your server must reply with the hourly summary statistics based on the anonymized data. 

The response format sent to the client must strictly be:
`YYYY-MM-DD HH:00 -> AVG_LATENCY` 
where `AVG_LATENCY` is rounded down to the nearest integer. Ensure the server stays running to handle the automated verifier requests.