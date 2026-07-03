You are a log analyst investigating a recent security incident. The security team recorded a snippet of the SOC dashboard during the incident, which contains the dynamic alert configuration used by the attackers to bypass normal detection.

Your task is to build a high-performance Rust-based log detector that uses windowed aggregation to identify malicious log sequences based on the hidden configuration in the video, and classify log files as either clean or malicious.

Step 1: Video Analysis
A recording of the dashboard is located at `/app/dashboard.mp4`. Use `ffmpeg` and any available OCR tools (like `tesseract`, which you can install) to extract the frames and read the dashboard text.
Somewhere in the video, a frame displays the critical alert configuration in the exact format: `ALERT_CONFIG: W=<seconds>s, T=<count>`. 
You must find this window size (`W`) and threshold (`T`).

Step 2: Log Parsing and Structured Extraction
Write a Rust program at `/home/user/detector`. 
This program must accept a single command-line argument: the path to a plain-text log file.
The log files contain lines in this format:
`[<unix_timestamp>] WARNING Failed authentication for user <username> from <ip_address>`
(Note: There may be other unrelated log lines. You only care about the "Failed authentication" lines).

Extract the timestamp and the IP address. 

Step 3: Windowed Aggregation & Detection
Implement a sliding window aggregation in your Rust program. For each unique IP address, determine if the number of failed authentications within ANY rolling window of `W` seconds is STRICTLY GREATER THAN `T`.
For example, if W=5 and T=10, then 11 failures from the same IP within a 5-second span is malicious.

Step 4: Classification
Compile your Rust program to a binary at `/home/user/detector`.
- If a log file contains ANY IP address that triggers the alert (failures > T in W seconds), the program must exit with status code `1` (indicating "evil").
- If no IP address triggers the alert, the program must exit with status code `0` (indicating "clean").

To ensure high performance, structure your Rust code to process the file efficiently (e.g., streaming or parallel processing of IP groupings). 

You can test your implementation against the sample log files provided in `/app/corpora/clean/` and `/app/corpora/evil/`. The automated test will run your binary against a similar, larger hidden dataset. Ensure your binary strictly follows the exit code requirements.