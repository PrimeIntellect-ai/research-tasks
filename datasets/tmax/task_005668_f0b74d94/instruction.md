You are acting as a backup administrator dealing with a batch of raw log files that need to be sanitized and re-archived. 

You have been provided with an archive of raw data at `/home/user/raw_data.tar.gz`.

Perform the following operations using Bash and standard Linux tools:
1. Extract the contents of `/home/user/raw_data.tar.gz` into a new directory located at `/home/user/processing`.
2. Find all files ending in `.log` within the `/home/user/processing` directory (including any subdirectories).
3. In all `.log` files, search for any line containing `API_KEY=` followed by any alphanumeric characters, and replace the entire line with exactly `API_KEY=REDACTED`. Note: Do NOT modify any files that do not end in `.log`, even if they contain `API_KEY=`. Modify the files in-place.
4. Once the sanitization is complete, create a new compressed archive (gzip format) of the `/home/user/processing` directory at `/home/user/sanitized_data.tar.gz`. Ensure the directory structure is preserved.
5. Verify the integrity of the newly created `/home/user/sanitized_data.tar.gz` using standard tools (e.g., `tar -tzf` or `gzip -t`).
6. If the archive is successfully verified as intact, create a file at `/home/user/result.log` containing the exact text `INTEGRITY_VALID`.

Ensure you execute these steps carefully and leave the final sanitized archive and the `result.log` file in the specified locations.