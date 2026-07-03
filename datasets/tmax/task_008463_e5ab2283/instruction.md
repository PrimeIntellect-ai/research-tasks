You are acting as a configuration manager tracking system changes. You need to implement a Python-based snapshot tool that backs up the currently active configuration file while redacting sensitive information and deduplicating backups using hard links.

The system has an active configuration file accessible via a symbolic link at `/home/user/active.conf`. This symlink points to the current version of the configuration inside `/home/user/configs/`. 

Your task is to write and execute a Python script at `/home/user/tracker.py` that performs the following actions:
1. Resolves and reads the configuration file currently pointed to by the symlink `/home/user/active.conf`.
2. Transforms the content to redact sensitive information: any line starting exactly with `password=` or `token=` must be replaced entirely with `password=***` and `token=***` respectively. Keep all other lines exactly as they are.
3. Computes the SHA256 hex digest of the resulting redacted content (encoded as UTF-8).
4. Checks the backup directory `/home/user/backups/`. 
    - If a backup file named `<sha256_hex_digest>.conf` does NOT exist in this directory, create it and write the redacted content into it.
    - If it DOES exist, do not overwrite it.
5. Creates or updates a hard link at `/home/user/backups/latest.conf` to point to the `<sha256_hex_digest>.conf` file. If `/home/user/backups/latest.conf` already exists, you must remove it before creating the new hard link.

After writing the script, execute it once so that the backup is generated based on the current active configuration. 

Ensure that `/home/user/tracker.py` executes successfully without errors and leaves the system in the requested state.