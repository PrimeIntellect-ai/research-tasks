You are an operations engineer triaging an incident where a critical C++ background data processing service deadlocked under high contention. The stalled process was manually killed, leaving behind a memory dump, a corrupted write-ahead log (WAL), and a broken recovery tool.

Your goal is to extract the incident details and successfully run the recovery process.

The application files are located in `/home/user/data_processor`.

Perform the following steps:
1. **Secret Recovery**: The background service uses a hardcoded legacy decryption key to process the WAL. A developer recently removed this key from the code and committed the change, but forgot to put it in the new secret manager. Find the deleted decryption key in the git repository's history (`/home/user/data_processor`).
2. **Compiler/Linker Error Interpretation**: The developer provided a recovery tool in `recovery.cpp` to parse the `system.wal` file. However, the build script `build.sh` is broken and produces compiler/linker errors. Diagnose and fix the build process or the code so that `./build.sh` successfully produces an executable named `recovery`.
3. **Database Recovery**: Run the compiled `recovery` executable. It requires two arguments: `./recovery <DECRYPTION_KEY> <WAL_FILE>`. Use the key you found in step 1 and `/home/user/data_processor/system.wal` as the WAL file. Note the "Last Committed TXN_ID" from its output.
4. **Memory Dump Analysis**: A core dump was generated at `/home/user/data_processor/core.dump` when the deadlocked process was killed. Extract the 16-character alphanumeric Transaction Hash of the deadlocked transaction. It is embedded in the dump, formatted precisely as `DEADLOCK_TX_HASH=<16_CHAR_HASH>`.

Finally, write an incident report to `/home/user/incident_report.txt` with exactly the following format (replace the bracketed placeholders with your findings):

```
SECRET_KEY: [Recovered Decryption Key]
LAST_TXN_ID: [Last Committed TXN_ID]
DEADLOCK_HASH: [16-character Deadlock Hash]
```