You are managing a configuration tracking system for a large application. Over time, configuration backups have been stored as chunked, nested archives, and changes are recorded in a multi-line log file.

Your objective is to perform a rollback to a specific stable state and activate it using symbolic links.

Here are the details of your workspace under `/home/user/config_manager`:

1. **Find the Target Release:**
   Read the log file located at `/home/user/config_manager/changelog.txt`. This is a multi-line log file where each entry is separated by a blank line. 
   Find the entry where the `Message:` field is exactly `Stable release v2.4`. 
   Extract the `Commit:` hash from this specific multi-line entry.

2. **Extract and Reassemble:**
   Navigate to `/home/user/config_manager/archives/`. You will find several `.tar` files named `backup_<commit_hash>.tar`.
   Extract the `.tar` file that matches the commit hash you found in step 1.
   Inside this tarball, you will find several split chunks of a gzip archive (e.g., `config.tar.gz.aa`, `config.tar.gz.ab`, etc.).
   Merge these chunks back together into a single valid archive and extract its contents. The extracted contents will be a directory containing configuration files.

3. **Deploy via Symbolic Links:**
   Move the extracted configuration directory to `/home/user/config_manager/versions/<commit_hash>/` (create the `versions` directory if it doesn't exist).
   To "activate" this configuration without duplicating files, create a symbolic link at `/home/user/config_manager/live_config` that points directly to `/home/user/config_manager/versions/<commit_hash>/`.

4. **Generate a Verification Report:**
   Inside the newly activated live configuration directory, there is a file named `database.conf`. Read this file and find the value for `max_connections`.
   Create a report file at `/home/user/config_manager/rollback_report.txt` with exactly the following format:
   ```
   Rollback Hash: <commit_hash>
   Max Connections: <value>
   ```

You must use standard bash CLI tools (like `awk`, `grep`, `tar`, `cat`, `ln`, etc.) to complete this task.