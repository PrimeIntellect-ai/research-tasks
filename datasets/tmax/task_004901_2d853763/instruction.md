You are an IT support technician responding to an escalated ticket. 

**Ticket #8831:**
"Our log aggregation script, `process_pcap_logs.py`, is hanging indefinitely when we try to process the latest batch of exported packet capture logs. It worked fine yesterday! It's supposed to read network connection logs and group the connections by the *next* calendar day's midnight, but it never finishes running. We suspect there is a weird statistical anomaly or timestamp edge case in the new logs causing an infinite loop."

**Your Objectives:**
1. Investigate `/home/user/process_pcap_logs.py` and the input data at `/home/user/pcap_logs.csv`.
2. Identify the logical bug causing the script to hang. The script attempts to manually calculate the next midnight by advancing the time, but has a subtle date-rollover bug.
3. Fix the `get_next_midnight` function in `/home/user/process_pcap_logs.py` so that it correctly and efficiently returns the exact next calendar day at `00:00:00` in ISO format, preserving the UTC timezone (e.g., `2024-02-01T00:00:00+00:00`).
4. Run the fixed script to process the CSV.
5. Ensure the script successfully completes and outputs the aggregated data to `/home/user/binned_stats.json`.

**Constraints:**
- Do not change the input CSV file.
- The output JSON file must contain the counts of log entries keyed by their calculated next-midnight ISO timestamp.
- Use Python's built-in `datetime` library for your fixes.