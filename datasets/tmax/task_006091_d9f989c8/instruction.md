You are an IT Support Technician handling an escalated ticket regarding a failing billing processor.

**Ticket Description:**
"Our daily billing script `/home/user/billing.py` is suddenly failing with a `ChecksumMismatchError`. The input data is supposed to come from an external API, but since the API went down, we only have a network packet capture of the last successful transmission in `/home/user/billing_dump.pcap`. We need you to extract the payload, identify why the script is failing, and fix it."

**Your Tasks:**
1. **Extract the payload:** Analyze `/home/user/billing_dump.pcap` and extract the JSON HTTP response payload into a file named `/home/user/input.json`. 
2. **Isolate the bug:** The `billing.py` script attempts to sum the transaction amounts and compare it against an `expected_total` string. It is currently failing due to floating-point precision loss caused by one abnormally large transaction completely swallowing the precision of subsequent small transactions. Use a delta-debugging or bisection approach to identify the specific transaction ID that causes the precision loss (the abnormally large one). Write this exact transaction ID to `/home/user/bad_tx.txt`.
3. **Fix the script:** Modify `/home/user/billing.py` so that it calculates the sum with exact precision. You must use the built-in `decimal` module to prevent precision loss. Ensure the script writes the final successfully validated total (as a string) to `/home/user/total.txt`.

**Constraints:**
- Do not modify `input.json`. You must fix `billing.py` to handle the data correctly.
- Ensure your fixed `billing.py` exits successfully (exit code 0) when run against the extracted `input.json`.