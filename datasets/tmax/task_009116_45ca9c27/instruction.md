You are acting as a backup administrator. The previous archiving system experienced a race condition and fragmented our server logs into a nested archive structure. We need to reconstruct the log, parse it for critical alerts, and re-archive the critical data properly.

Your task is to write and execute a Python script (you can name it `/home/user/process_backups.py`) that performs the following steps:

1. **Unpack the Nested Archive:** 
   There is a master archive located at `/home/user/backups/master_backup.tar`. 
   Inside this tarball, there are multiple gzip-compressed tarballs (e.g., `part_1.tar.gz`, `part_2.tar.gz`). 
   Extract these, and then extract their contents. Inside, you will find several log chunks named `chunk_00`, `chunk_01`, etc.

2. **Merge and Parse:**
   Merge the chunks in sequential order based on their filename suffix (`00`, `01`, `02`, etc.) to reconstruct the original log data.
   The reconstructed log consists of JSON formatted lines. 
   Parse each line and filter for records where the key `"severity"` exactly matches `"CRITICAL"`.

3. **Output the Filtered Log:**
   Write all the filtered "CRITICAL" JSON lines to a single file at `/home/user/parsed/critical_alerts.log`. Preserve the original JSON line format exactly as it appeared in the chunks.

4. **Split and Link:**
   Split the `critical_alerts.log` file into smaller chunk files containing exactly 10 lines each. 
   Save these files in the directory `/home/user/parsed/split/` with the prefix `crit_part_` and a two-character alphabetical suffix (e.g., `crit_part_aa`, `crit_part_ab`, `crit_part_ac`, etc., matching the standard output of the `split` command). If the last file has fewer than 10 lines, that is fine.
   
5. **Symlink:**
   Finally, create a symbolic link at `/home/user/parsed/latest_alert_part` that points to the *last* split chunk file created in the sequence (e.g., if `crit_part_ad` is the last one alphabetically, the symlink should point to it). The symlink target must be the absolute path.

Ensure your script handles everything end-to-end. Do not leave hardcoded paths that assume manual prior extraction.