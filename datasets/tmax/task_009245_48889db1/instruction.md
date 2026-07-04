You are acting as a compliance officer auditing a financial system for suspicious activity. Your task is to extract, analyze, and report on high-value transaction hubs using Bash and standard CLI tools (like `jq`, `awk`, `sort`, etc.). 

You have been provided with an export of the system's logs in JSON Lines format at `/home/user/audit_logs.jsonl`. 

Each line is a JSON object representing a system event, which may include logins, settings changes, or financial transfers. For example:
`{"timestamp": "2023-10-01T10:00:00Z", "type": "TRANSFER", "sender_id": "U123", "receiver_id": "U456", "amount": 75000, "status": "COMPLETED"}`

Write a Bash script at `/home/user/analyze_hubs.sh` that performs the following "NoSQL-style" aggregation and graph analytics pipeline:
1. **Filter**: Retain only events where `"type"` is `"TRANSFER"`, `"status"` is `"COMPLETED"`, and the `"amount"` is **strictly greater than** 50000.
2. **Graph Analytics (Degree Centrality)**: For each `sender_id` in the filtered dataset, calculate their "out-degree" (the number of **distinct** `receiver_id`s they successfully sent these high-value transfers to). Do not count multiple transfers to the same receiver twice.
3. **Sort**: Order the senders by their distinct receiver count in DESCENDING order. If there is a tie in the count, sort the tied `sender_id`s in ASCENDING alphabetical order.
4. **Paginate**: We want to ignore the absolute highest hub (assume it is a known internal corporate account). Skip the 1st record, and retrieve only the next 3 records (i.e., offset 1, limit 3).
5. **Output**: Write the final 3 records to `/home/user/suspicious_hubs.csv` in the format `sender_id,distinct_receiver_count`.

Make sure your script is executable and run it to produce the `suspicious_hubs.csv` file. The test will automatically check the contents of `/home/user/suspicious_hubs.csv`.