You are an operations engineer debugging a configuration drift issue. 

A system process recently dumped the current configuration state of several servers into a CSV file located at `/home/user/config_dumps.csv`. However, this file is notoriously difficult to parse because:
1. It is encoded in `UTF-16LE`.
2. The `retry_policy` column contains embedded newlines (which causes naive shell scripts to silently drop or corrupt rows).

The CSV is currently in a "wide" format: `server_id, max_connections, timeout, retry_policy`.

Your task is to write and execute a Python script that does the following:

1. **Format Reshaping**: Safely read the CSV (preserving embedded newlines and handling the encoding) and reshape it into a "long" format. Save this reshaped data to `/home/user/long_configs.json`. The JSON should be a list of objects, each with three keys: `server`, `key`, and `value`. 
   For example: `[{"server": "srv-001", "key": "max_connections", "value": "100"}, {"server": "srv-001", "key": "retry_policy", "value": "fast\nfallback"}, ...]`

2. **Anomaly Detection**: Analyze the data to find a configuration anomaly. All servers *except one* have the exact same `timeout` value. Identify the anomalous `server_id`, its incorrect `timeout` value, and the expected (majority) `timeout` value.

3. **Template Generation**: Generate a remediation template for the anomalous server. Create a file `/home/user/remediation.conf` with exactly this format:
```
Host: <anomalous_server_id>
Action: FIX_TIMEOUT
Expected: <majority_timeout_value>
Found: <anomalous_timeout_value>
```

Ensure your Python script runs successfully and produces both `/home/user/long_configs.json` and `/home/user/remediation.conf`.