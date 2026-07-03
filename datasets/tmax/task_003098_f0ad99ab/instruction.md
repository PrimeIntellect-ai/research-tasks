You are acting as an automated configuration manager. A system daemon continuously writes configuration updates to a Write-Ahead Log (WAL) located at `/home/user/sys_updates.wal`.

The WAL file contains multiple configuration updates in the following format (colon-separated):
`TIMESTAMP:MODULE_NAME:BASE64_ENCODED_PAYLOAD`

Your task is to parse this file and apply the latest configuration for each module using standard bash and coreutils tools.

Follow these exact steps:
1. Identify the latest entry (the one with the highest integer timestamp) for each unique `MODULE_NAME` in `/home/user/sys_updates.wal`.
2. Ensure the directories `/home/user/configs/versions/` and `/home/user/configs/active/` exist.
3. For the latest entry of each module, decode the `BASE64_ENCODED_PAYLOAD` and save the resulting decoded text into a new file named `/home/user/configs/versions/<MODULE_NAME>_<TIMESTAMP>.conf`.
4. Create or update a symbolic link at `/home/user/configs/active/<MODULE_NAME>.conf` that points to the corresponding versioned file you just created.

Ensure that only the latest configuration for each module is extracted and symlinked. Older updates in the WAL should be ignored. You are expected to accomplish this entirely within the terminal using standard Linux tools (e.g., `awk`, `sort`, `base64`, `ln`, etc.).