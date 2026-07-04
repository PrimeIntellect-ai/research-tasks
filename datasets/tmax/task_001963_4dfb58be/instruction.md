You are acting as a technical compliance officer auditing a suspected money laundering network.

We have intercepted a voicemail from the lead investigator. It is located at `/app/voicemail.wav`.
Listen to (or transcribe) this audio file to understand the specific graph metric and operational constraints required for the audit.

You are provided with an SQLite database at `/app/ledger.db`. The database contains a single table:
`transfers (src INTEGER, dst INTEGER, amount INTEGER)`

Your task is to write a Python script at `/home/user/graph_audit.py` that takes a single command-line argument (`account_id` as an integer) and prints ONLY the computed metric as an integer.

Crucially, the database has a known issue with stale rows due to a corrupted index (the name of the index is mentioned in the voicemail). Your script MUST ensure it operates on the uncorrupted base table data. 

Ensure your script operates efficiently, as it will be heavily fuzzed against thousands of random account IDs to verify its correctness.