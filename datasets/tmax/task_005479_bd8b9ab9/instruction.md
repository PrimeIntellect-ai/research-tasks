You are an IT support technician responding to an urgent escalation ticket. Our legacy payment processing service crashed unexpectedly. 

We need to recover the final transaction payload that was being processed. The service writes the current transaction ID to a log file before processing, but the log file was accidentally deleted by an automated cleanup script shortly after the crash. 

Here is what you have:
1. `/home/user/disk.img`: A raw disk snapshot of the log directory taken right after the deletion. The deleted log file contained a string in the exact format `[DELETED_LOG] TX_ID: <8-character hex string>`. You need to inspect this filesystem image/file to recover that transaction ID.
2. `/home/user/mem.dmp`: A raw memory dump of the crashed process. It contains transaction data in the format: `TX_START|<tx_id>|<payload>|TX_END`.
3. `/home/user/recover_tx.py`: A Python script written by a previous technician to extract the payload from the memory dump given a transaction ID.

However, the ticket notes state that `recover_tx.py` has a bug: it contains an off-by-one boundary condition error causing it to truncate the last byte of the recovered payload, which causes downstream signature validation to fail.

Your tasks:
1. Inspect `/home/user/disk.img` to recover the 8-character hex transaction ID.
2. Debug and fix the boundary condition / off-by-one error in `/home/user/recover_tx.py`.
3. Use the fixed script to extract the payload for the recovered transaction ID from `/home/user/mem.dmp`.
4. Save the EXACT, fully recovered payload (without any surrounding markers or pipes) to a file named `/home/user/recovered_payload.txt`.

Ensure your final payload in `/home/user/recovered_payload.txt` has no missing characters at the end!