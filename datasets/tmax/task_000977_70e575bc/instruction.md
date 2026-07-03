You are an on-call engineer responding to a critical 3 AM page. The data pipeline is down. 

Our upstream services write to custom Write-Ahead Log (WAL) files. These files are processed by a legacy, stripped Go binary called `wal_ingester`. Recently, a serialization bug in an upstream service started injecting corrupted entries into the WALs. When `wal_ingester` encounters these specific malformed entries, it fails to cancel its internal worker context properly, triggering a massive goroutine leak that hangs the process forever and stops all data recovery efforts.

We cannot recompile `wal_ingester` right now. We need you to build a fast detector to identify and quarantine the poisoned WAL files so the pipeline can continue processing the healthy ones.

Your environment contains:
- `/app/wal_ingester`: The stripped binary that hangs on bad files.
- `/app/corpus/clean/`: A directory containing 20 sample WAL files that process successfully.
- `/app/corpus/evil/`: A directory containing 20 sample WAL files that cause the goroutine leak and hang.

**Your Objective:**
1. Reverse-engineer the WAL serialization format and trace the intermediate state of `wal_ingester` to understand exactly which byte pattern or corrupted state causes the convergence failure and hang.
2. Write a Bash script at `/home/user/wal_classifier.sh` that takes a single file path as an argument.
3. The script must analyze the file and exit with code `0` if the file is safe (clean), or exit with code `1` if the file contains the leak-inducing malformation (evil).
4. Your script must be efficient and robust. You may use standard Unix utilities (like `od`, `hexdump`, `awk`) or inline scripts (Python/Perl) within your Bash script to parse the binary serialization.

Do not attempt to patch the binary itself. Focus on accurately classifying the files based on their binary structure. Ensure your script is executable (`chmod +x`).