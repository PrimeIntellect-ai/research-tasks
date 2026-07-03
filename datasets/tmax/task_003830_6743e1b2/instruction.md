You are an operations engineer triaging an incident. Our log processing service crashed in production due to an infinite recursion error. 

You have been provided with the following files:
1. `/home/user/app_memory.dmp` - A raw memory dump captured at the time of the crash.
2. `/home/user/transactions.json` - The dataset the service was processing, which contains corrupted data with circular references.
3. `/home/user/log_parser.py` - The script that processes the transaction chains to reconstruct a timeline.

Your task:
1. **Analyze the memory dump**: Use shell utilities to extract the corrupted transaction ID that triggered the crash from `/home/user/app_memory.dmp`. Look for a string in the format `CRASH_TX_ID: <TX_ID>`. Write the extracted transaction ID to `/home/user/crash_report.txt` exactly in this format: `Crashed at: <TX_ID>`.
2. **Fix the code**: Modify `/home/user/log_parser.py` to handle the corrupted input gracefully. The `resolve_chain` function must be updated to track visited transactions. If it encounters a transaction ID it has already visited in the current chain (a circular reference), it should append the string `[CORRUPTED]` to the `timeline` list and immediately return, preventing infinite recursion.
3. **Execute**: Run the fixed `/home/user/log_parser.py` script. It will generate a `/home/user/reconstructed_timeline.log` file.

Verification will check the exact contents of `/home/user/crash_report.txt` and `/home/user/reconstructed_timeline.log`.