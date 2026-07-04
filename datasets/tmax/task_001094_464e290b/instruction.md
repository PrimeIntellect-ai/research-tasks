You are a storage administrator managing a legacy server where disk space is at a premium. Your task is to implement an efficient log archival process for a rapidly growing application. 

You have three main objectives:

1. **Fix and Install the Archiver:**
We rely on `pigz` (Parallel GZip) for fast, efficient compression. The source code for `pigz-2.8` has been vendored to the server at `/app/pigz-2.8`. However, a previous administrator accidentally corrupted its `Makefile` while trying to "optimize" it, and it currently fails to compile. 
Find the compilation error in `/app/pigz-2.8/Makefile` (hint: it's failing to link the required compression library), fix it, compile `pigz`, and copy the resulting `pigz` binary to `/home/user/bin/` (create the directory if it doesn't exist).

2. **Parse the Configuration:**
There is an archival configuration file located at `/home/user/archive_config.conf` with the following key-value format:
```
SOURCE_DIR=/var/log/app_logs
EXCLUDE_PATTERN_1=\[DEBUG\]
EXCLUDE_PATTERN_2=\[TRACE\]
COMPRESSION_LEVEL=-9
TARGET_FILE=/home/user/archived_logs.tar.gz
```

3. **Implement the Archival Script:**
Write a Bash script at `/home/user/archive.sh` that does the following:
- Reads the variables from `/home/user/archive_config.conf`.
- Iterates over all `.log` files in the `SOURCE_DIR`.
- Uses streaming text transformation (e.g., `awk` or `sed`) to strip out any log lines matching `EXCLUDE_PATTERN_1` or `EXCLUDE_PATTERN_2`. We do not want to waste disk space archiving debug and trace noise.
- Packages the filtered streams into a single `tar` archive and pipes it directly into your newly compiled `/home/user/bin/pigz`, applying the `COMPRESSION_LEVEL` specified in the config.
- Saves the final compressed output to `TARGET_FILE`.

**Constraints & Notes:**
- You must use Bash as your primary scripting language. Shell built-ins, standard coreutils, `tar`, `awk`, and `sed` are all permitted.
- Do NOT create intermediate uncompressed `.tar` or `.log` files on disk (except memory-mapped/pipes if needed). The filtering and archiving must be done in a streaming fashion to conserve disk I/O.
- Run your script once it's complete to generate `/home/user/archived_logs.tar.gz`. The automated verifier will grade your success based on the final file size of this archive (it must be heavily compressed and stripped of the excluded patterns).