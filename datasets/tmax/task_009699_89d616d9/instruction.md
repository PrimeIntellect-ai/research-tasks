You are acting as a backup administrator. We need to archive critical configuration state from our database's Write-Ahead Log (WAL) system before performing a system migration.

Your task is to write a Go program at `/home/user/wal_archiver.go` that automates this backup process.

The program must perform the following steps:
1. **Read Configuration**: Read a JSON configuration file located at `/home/user/backup_config.json`. 
   The JSON file has this structure:
   ```json
   {
       "wal_dir": "/path/to/wal/directory",
       "archive_path": "/path/to/output/backup.tar.gz"
   }
   ```
2. **Parse WAL Files**: Scan the directory specified by `wal_dir` for all files ending in `.wal`. Read these files in lexicographical order by filename.
   Our custom WAL files are binary files consisting of a sequence of records. Each record has the following format:
   - **Payload Length**: 4 bytes, Unsigned 32-bit integer, Big-Endian. (This represents the length of the Payload only).
   - **Record Type**: 1 byte, Unsigned 8-bit integer.
   - **Payload**: Raw bytes of length equal to Payload Length.

   There are two record types:
   - Type `0x01`: Configuration Change (Payload is a UTF-8 string)
   - Type `0x02`: Standard Data (Payload is binary data, which should be ignored)

3. **Extract Configurations**: For every `0x01` (Configuration Change) record found, extract the payload string. Write these strings to a text file at `/home/user/extracted_configs.txt`. Each extracted configuration string must be on its own line, in the exact order they were discovered (ordered by filename, then by record appearance in the file).

4. **Create Archive**: After extracting all configuration strings, the Go program must create a gzip-compressed tar archive (`.tar.gz`) at the location specified by `archive_path` in the JSON config. The archive must contain exactly two files at its root (no parent directories):
   - `backup_config.json` (the original config file)
   - `extracted_configs.txt` (the file you just generated)

Once you have written `/home/user/wal_archiver.go`, compile it and run it to produce `/home/user/extracted_configs.txt` and the final archive.