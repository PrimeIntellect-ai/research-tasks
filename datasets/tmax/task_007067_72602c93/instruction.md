You are tasked with implementing a secure configuration update pipeline. We receive configuration updates as split archive files, but we suspect the upstream system has been compromised and might be attempting a "zip slip" directory traversal attack to overwrite system files. 

Your objective is to write and execute a Bash workflow that safely merges, filters, modifies, and repackages these configuration updates.

Follow these specific instructions:
1. Merge the split archive files located in `/home/user/incoming/update.tar.gz.part*` into a single file at `/home/user/update.tar.gz`.
2. Extract the archive into `/home/user/extracted/`. However, you must explicitly prevent any directory traversal attacks. Extract **only** files that fall strictly within the `configs/` directory. Do not extract any files that have absolute paths or use `../` to escape the target directory. 
3. Perform a large-scale text edit on all `.conf` files within `/home/user/extracted/configs/`:
   - Find all lines matching `LOG_LEVEL=<any_value>` and replace them with `LOG_LEVEL=TRACE`.
   - Append the exact string `MANAGED_BY=SECURE_CONF_MANAGER` as a new line at the very end of every `.conf` file.
4. Repackage the modified `configs/` directory into a new archive at `/home/user/safe_update.tar.gz`.
5. Split this new archive into 500-byte chunks located in `/home/user/outgoing/` named `safe_update.tar.gz.chunk-aa`, `safe_update.tar.gz.chunk-ab`, etc.

Ensure the final chunks are cleanly generated and that no malicious files have been written outside the `configs/` hierarchy in `/home/user/extracted/`.