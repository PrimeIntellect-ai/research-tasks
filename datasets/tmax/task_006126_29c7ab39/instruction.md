Wake up, we have a critical 3 AM page! The legacy payment processor service just OOM-killed itself in production, leaving behind a raw memory dump. Worse, it crashed right in the middle of a high-value transaction, and we need to manually void it before the settlement window closes in 15 minutes.

Here is what we need you to do:
1. **Memory Dump Analysis**: The crash dump is located at `/home/user/payment.dump`. Extract the stranded transaction ID from this binary file. The application always logs the active transaction in memory with the exact prefix `CRITICAL_TXN:` followed immediately by the ID (e.g., `CRITICAL_TXN:12345-XYZ`).
2. **Git Forensics**: We need the legacy voiding API key to cancel the transaction. The key was hardcoded in the `/home/user/payment-service` git repository but was removed in a recent commit for security reasons. Search the git history of that repository to find the deleted key. It was stored as a string assigned to `VOID_API_KEY`.
3. **Reporting**: Write your findings to a file exactly at `/home/user/recovery.log`. The file must contain exactly one line in the following format:
`TXN=[transaction_id], KEY=[api_key]`

For example, if the ID is `999-ABC` and the key is `sk_live_123`, the file should contain:
`TXN=999-ABC, KEY=sk_live_123`

You have access to standard Linux utilities to complete this task. Please create the log file with the correct data.