You are a support engineer tasked with collecting diagnostics and recovering data from a crashed application. 

The application uses a custom Python-based local database. After a recent system crash, the database's Write-Ahead Log (WAL) file (`/home/user/db/transaction.wal`) became partially corrupted. 

We have a recovery script located at `/home/user/recovery.py`. However, when running this script, it crashes with a fatal decoding error (similar to an unhandled panic) on certain edge-case corrupted data within the WAL.

Your task is to:
1. Run and debug `/home/user/recovery.py`.
2. Trace the intermediate states to identify exactly which Transaction ID (TxID) causes the crash due to encoding/serialization issues.
3. Modify `/home/user/recovery.py` so that it handles the corrupted payload gracefully. Specifically, if a payload cannot be decoded as valid UTF-8, the script should catch the error, skip that specific transaction, and continue recovering the rest of the file.
4. Calculate the sum of the `"value"` fields from all successfully recovered valid transactions.
5. Generate a diagnostics report at `/home/user/recovery_report.txt` with exactly the following format:

```
Corrupted TxID: <ID of the transaction that caused the crash>
Recovered Total: <Sum of "value" fields from valid transactions>
```

Note: The script might also be failing due to an outdated serialization package imported at the top of the script (`ujson` vs `json`). Resolve any dependency issues using standard library modules if necessary to keep the recovery self-contained.

The WAL file consists of sequentially packed binary records:
- 4 bytes: Transaction ID (unsigned int, little-endian)
- 4 bytes: Payload Length (unsigned int, little-endian)
- N bytes: JSON Payload (UTF-8 encoded string)

Ensure the final report is strictly formatted as requested.