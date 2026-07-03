You are an operations engineer triaging an incident for a financial metrics service. The service has been reporting incorrect total balances, and the engineering team suspects a combination of race conditions under high concurrent load and floating-point precision loss during mathematical aggregation.

You have been provided with two files in `/home/user/incident/`:
1. `traffic_dump.txt`: An ASCII representation of a network packet capture (equivalent to `tcpdump -A` output) showing all incoming HTTP POST requests to the `/api/metrics` endpoint. Each request contains a JSON payload like `{"account_id":"ACC-999","amount":X.XX}`.
2. `db_queries.log`: A sequential log of the actual SQL `UPDATE` statements executed by the database. 

Your investigation goals are:
1. **Network Analysis & Precision Repair**: Extract all the `amount` values sent to the `ACC-999` account from the `traffic_dump.txt` file. Calculate the *exact mathematical sum* of all these intended amounts. You must avoid standard IEEE 754 floating-point errors (e.g., standard float addition might yield `1.4200000000000002` instead of `1.42`).
2. **Concurrency & Query Debugging**: Due to an application-level race condition, some network requests were dropped and never resulted in a database query. Compare the network payloads to the executed queries in `db_queries.log` to determine how many updates were lost.

Create a final report file at `/home/user/incident_report.txt` containing exactly four lines in the following format:
```
Total packets received for ACC-999: <integer count of payloads in traffic dump>
Total queries executed for ACC-999: <integer count of queries in db log>
Lost updates: <integer difference between packets and queries>
Correct exact sum: <exact decimal string representation of the sum of ALL amounts in the pcap>
```

Example of correct exact sum format: `1.42` (do not use scientific notation or floating-point artifacts).