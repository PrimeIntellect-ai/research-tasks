As a backup administrator, you are responsible for archiving system data. Part of our legacy archiving pipeline relies on an undocumented, stripped executable located at `/app/backup_wal_parser`. 

This binary processes our custom multi-line Write-Ahead Log (WAL) format from `stdin` and outputs a summarized, single-line CSV format to `stdout` for the archiver to consume. We need to deprecate this black-box binary and replace it with a readable, maintainable script.

Your task is to write an executable script at `/home/user/wal_extractor.sh` (you may write it in Bash, Python, or any standard scripting language available) that perfectly replicates the behavior of `/app/backup_wal_parser`. 

The input WAL logs consist of multi-line records that look generally like this:
```
BEGIN_WAL_RECORD
PATH: <filepath>
OP: <operation_type>
BYTES: <integer>
END_WAL_RECORD
```

You must reverse-engineer the exact transformation rules of `/app/backup_wal_parser` by passing it test data (or using tools like `strings`, `ltrace`, `objdump`, etc.) and observing how it handles different operations, sizes, missing fields, and formatting. 

Requirements:
1. Your script must read from standard input (`stdin`) and write to standard output (`stdout`).
2. Your script must be executable (`chmod +x /home/user/wal_extractor.sh`).
3. Your script's output must be BIT-EXACT equivalent to `/app/backup_wal_parser` for any valid sequence of WAL records.

Create the script and ensure it perfectly mimics the legacy binary's behavior.