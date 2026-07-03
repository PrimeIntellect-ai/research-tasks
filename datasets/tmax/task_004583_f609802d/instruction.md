You are an artifact manager tasked with curating a raw binary repository. We recently experienced disk corruption, and many of our release artifacts might be damaged. Additionally, we need to rebuild our central artifact registry by parsing unstructured multi-line log files.

Your task is to write and execute a Bash script at `/home/user/curate_artifacts.sh` that processes the raw repository. 

The raw repository is located at `/home/user/repo_raw/`. It contains a nested directory structure. Inside these directories are various release archives (`*.tar.gz`) and a multi-line log file named `publish.log` in each subdirectory.

Your script must perform the following:
1. **Recursive Traversal**: Find all `.tar.gz` files anywhere within `/home/user/repo_raw/`.
2. **Concurrency and File Locking**: To speed up processing, your script MUST process the archives concurrently (e.g., using background jobs `&` or `xargs -P`). Because multiple processes will be writing to the exact same output files simultaneously, you MUST use `flock` to ensure thread-safe appending.
3. **Archive Integrity Verification**: For each `.tar.gz` file, verify its integrity without extracting it (e.g., using `tar -tzf`).
    * If the archive is corrupt or invalid, append its absolute file path to `/home/user/corrupt.list` (one path per line).
4. **Multi-line Log Parsing**: If the archive is completely valid, look for `publish.log` in the *same* directory as the archive. The log contains multi-line records separated by `---`. You need to find the record for the specific valid archive and extract its `Team` and `Stage` values.
    Example `publish.log` format:
    ```
    ---
    Archive: service-a-v1.tar.gz
    Team: backend
    Stage: production
    Notes: Deployed successfully.
    ---
    Archive: service-b-v2.tar.gz
    Team: frontend
    Stage: staging
    Notes: Needs review.
    ---
    ```
5. **Transformation**: For each valid archive, securely append a comma-separated line to `/home/user/registry.csv` in the exact format: `Absolute_Archive_Path,Team,Stage`.

Requirements:
- Ensure the script waits for all concurrent background jobs to finish before exiting.
- Both `/home/user/corrupt.list` and `/home/user/registry.csv` must be generated accurately, safely avoiding race conditions.
- Run your script once it's created to generate the final output files.