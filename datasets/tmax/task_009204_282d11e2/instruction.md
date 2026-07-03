You are a storage administrator managing disk space for a legacy infrastructure. Several older systems dump storage usage reports and occasional erroneous binary core dumps into a designated directory: `/home/user/reports/`.

Your task is to write a bash script, `/home/user/aggregator.sh`, that processes these files, normalizes their encodings, securely aggregates the data, safely updates a summary file, and cleans up the binary dumps.

Here are the exact requirements for your script:

1. **Clean up Binary Files:**
   The script must find and delete all files with a `.bin` extension in `/home/user/reports/` to free up disk space.

2. **Process and Convert Text Reports:**
   The usage reports are stored as `.dat` files in `/home/user/reports/`. Because they come from various legacy systems, they are saved in different character encodings (e.g., UTF-16LE, ISO-8859-1, UTF-8). 
   - Your script must read each `.dat` file, detect its character encoding, and convert its text to standard UTF-8. 
   - Each file contains a single line of text in the format: `VOLUME:<VolumeName>|USAGE:<UsageInGB>` (e.g., `VOLUME:ALPHA|USAGE:1024`).

3. **Concurrent-Safe Aggregation:**
   - For each `.dat` file processed, extract the Volume Name and the Usage in GB.
   - Append a line in the exact format `<VolumeName>:<UsageInGB>` to `/home/user/master_log.txt`.
   - **Constraint:** Other system cron jobs might try to write to this log simultaneously. You must use `flock` with an exclusive lock on the file `/home/user/master_log.lock` when appending to `/home/user/master_log.txt` to ensure concurrent write safety.

4. **Atomic Summary Update:**
   - Calculate the total usage (sum of all `<UsageInGB>` values from the `.dat` files).
   - Write this single integer total to `/home/user/total_usage.txt`.
   - **Constraint:** This file is read frequently by an active monitoring agent. To prevent the agent from reading a partially written file, you must perform an **atomic write**. Do this by writing the total to a temporary file (e.g., using `mktemp`) and then moving (`mv`) the temporary file over `/home/user/total_usage.txt`.

Ensure your script is executable and performs all these actions when run via `bash /home/user/aggregator.sh`. Once you have created and tested your script, run it one final time to leave the system in the requested state.