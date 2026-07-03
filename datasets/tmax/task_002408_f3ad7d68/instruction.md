You are a log analyst investigating a recent security incident. 

Our preliminary pipeline was built to process server logs, but we suspect it has been silently dropping crucial log entries because the attacker used embedded newlines in their User-Agent payloads to break naive CSV parsers. 

The previous sysadmin left a voicemail before going on leave. It contains critical parameters about the anomaly signature. The audio file is located at `/app/voicemail.wav`. You will need to transcribe it to understand the specific threshold and conditions that define the attack pattern.

Your tasks:
1. **Transcribe and Analyze:** Listen to or transcribe `/app/voicemail.wav` to find the exact changepoint parameters (a specific rolling average window and a latency threshold).
2. **Robust Log Parsing:** Read `/home/user/server_logs.csv`. This file uses standard comma separation and double-quote text enclosures, but contains embedded newlines in the `user_agent` column. Ensure your parser does not drop or corrupt these multiline rows.
3. **Anomaly Detection:** Apply the criteria from the voicemail to the `response_time` column (which is in milliseconds). Identify the exact log entries that are part of the attack.
4. **Data Enrichment (Join):** Extract the `ip_address` from the anomalous logs. Match these IPs against `/home/user/threat_intel.json` to find the associated `actor_group`. If an IP is not in the threat intel file, label the actor_group as "Unknown".
5. **Template Generation:** Read the template file at `/home/user/report_template.jinja`. Generate a final report text by filling in the template with your enriched anomaly data.
6. **Output Export:** Write the successfully joined and extracted anomalous records to `/home/user/anomalies.json`. The file must be a JSON array of objects, with each object containing exactly: `id`, `timestamp`, `ip_address`, `response_time`, and `actor_group`.

Ensure your Python scripts handle the data robustly and accurately. The final grading will programmatically evaluate `/home/user/anomalies.json` by calculating the F1 score of your detected anomalies against the hidden ground truth.