You are tasked with organizing and archiving old project log files for our high-throughput logging system. We use a custom archiving tool, but the current version is suffering from severe performance issues and minor configuration bugs, causing it to fail or race with active logging processes.

Your objectives:
1. **Fix the Vendored Package:**
   Navigate to `/app/bash-log-archiver-1.0`. This package contains our archiving scripts. 
   - The `Makefile` has a typo regarding the environment variable used for the destination directory. It uses `DEST_DIR` but the scripts expect `ARCHIVE_DIR`. Fix this so the Makefile works correctly.
   - The core script, `archive.sh`, performs metadata-based file search (finding `.log` files older than 7 days in a specified directory), filters out `[DEBUG]` lines, and atomically writes the result to the archive directory. Currently, `archive.sh` uses a pure Bash `while read -r line; do ... done` loop to filter and write files, which is extremely slow (taking over 30 seconds for large files) and poorly manages temp files. 
   - Rewrite the filtering and atomic write logic in `archive.sh` using fast, standard shell utilities (like `grep`, `awk`, or `sed`) to achieve a massive speedup, ensuring you still write to a temporary file first and then `mv` it to prevent race conditions with readers.

2. **Run the Archival Process:**
   - The source logs are located in `/data/logs/`.
   - The target archive directory should be `/data/archive/`.
   - Use the fixed `Makefile` (e.g., `make install` or `make run`, depending on the package structure, passing the correct variables) to process the logs.
   - After running, all `.log` files in `/data/logs/` older than 7 days must be filtered (no `[DEBUG]` lines), renamed with a `.archive` extension, and moved to `/data/archive/`.

The automated test will evaluate your solution based on the **execution speed** of your fixed `archive.sh` on a standardized 50MB log file, validating that you achieved the required performance threshold and correctly implemented atomic writes.