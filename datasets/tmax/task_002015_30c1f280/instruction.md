A custom logging database used by our legacy application has crashed, leaving behind a partially corrupted Write-Ahead Log (WAL) file. The vendor who provided the database is out of business, but we found a stripped binary `wal_recovery_tool` in `/app/wal_recovery_tool` that supposedly reads these WAL files and outputs recovered JSON records to stdout.

However, the binary has a bug: it fails to converge and loops infinitely on certain edge cases in corrupted WALs, particularly when encountering a corrupted length prefix. We need a clean room implementation of this parser in Python. 

Your task is to:
1. Reverse engineer the WAL format and the logic of `/app/wal_recovery_tool` using system call tracing (`strace`) or binary analysis tools.
2. Resolve any dependency conflicts you might find if you decide to use certain Python parsing libraries.
3. Write a Python script at `/home/user/recover.py` that parses the WAL format *exactly* as the binary does for valid inputs, but properly handles the format parsing edge cases where the binary hangs.
4. The output must be bit-exact equivalent to the original binary on valid WAL records (one JSON object per line).
5. The script must take exactly one argument: the path to the WAL file.

Write the script and ensure it handles random inputs gracefully without looping infinitely.