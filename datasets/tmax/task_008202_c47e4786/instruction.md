You have recently inherited an unfamiliar, legacy codebase for a custom, multi-language key-value database system called `legacy_kv`. The previous developer left abruptly, and the production database recently crashed and corrupted its primary binary data file.

Your objective is to recover the final, committed value of the key `ADMIN_PASSWORD` and write it to `/home/user/flag.txt`.

Here is what you know:
1. The application directory is located at `/home/user/legacy_kv/`.
2. There is a crash report at `/home/user/legacy_kv/crash.log` containing a stack trace from the Python wrapper and the underlying C engine. It indicates that `data.bin` is completely unreadable.
3. The database uses a Write-Ahead Log (WAL) to ensure atomicity. When the binary file is corrupted, the system is supposed to auto-recover by replaying the text-based WAL file. However, an environment misconfiguration prevented the auto-recovery process from locating the WAL.
4. You must locate the WAL file (its location is referenced somewhere in the environment configuration/codebase), comprehend the custom WAL format by examining the codebase or the log itself, and logically reconstruct the final database state to find the value of `ADMIN_PASSWORD`.

The custom WAL format rules (which you can deduce from the codebase) are:
- Transactions start with `BEGIN`.
- Operations are `SET <key> <value>` or `DELETE <key>`.
- Transactions finish with either `COMMIT` or `ROLLBACK`.
- If a transaction is `COMMIT`ted, its operations are applied.
- If a transaction is `ROLLBACK`ed, or if the file ends before a `COMMIT` is reached (an incomplete transaction due to the crash), its operations must be entirely ignored.

You must rely strictly on standard Bash shell tools (like `awk`, `sed`, `grep`, etc.) or manual inspection to extract the value. Once you have determined the correct, latest committed value for `ADMIN_PASSWORD`, write it exactly as the only content in the file `/home/user/flag.txt`.