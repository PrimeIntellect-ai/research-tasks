You are an AI assistant helping a compliance officer audit an internal NoSQL database of financial transactions. 

The officer has provided an image at `/app/compliance_rule.png` which contains a screenshot of the compliance requirement, including:
1. The partition key and sort key for the audit.
2. The specific window function / analytical aggregation required.
3. The target field for the aggregation.

Your task is to create a Rust program that acts as our offline compliance auditor.

Requirements:
1. Extract the compliance rule text from `/app/compliance_rule.png`.
2. Write a Rust program. You must compile it to an executable located exactly at `/home/user/audit_checker`.
3. The program must read `stdin` line by line. Each line will be a JSON object representing a transaction. Example: `{"account_id": "acc_123", "tx_time": 1620000000, "amount": 150.5}`
4. Based on the extracted rule, your program must simulate the NoSQL window aggregation. Specifically:
   - Partition the data as specified in the image.
   - Order the data within each partition as specified.
   - Compute the rolling aggregation as specified in the image.
   - *Note: the rolling window size includes the current row and the specified number of preceding rows.*
5. Output format:
   - The **first line** of `stdout` must be a JSON object representing the optimal NoSQL index strategy required to support this query efficiently (e.g., `{"partition_key": 1, "sort_key": 1}`).
   - The **subsequent lines** must be the original JSON objects, enriched with a new key `compliance_metric` containing the calculated rolling value (as a float), outputted in the sorted order of the partition and sort keys.

Ensure your Rust code handles edge cases (like a partition having fewer transactions than the window size) correctly by just aggregating the available rows in the window. Use standard Rust tooling (`cargo`) to build your binary and ensure the final executable is moved/copied to `/home/user/audit_checker`.